# app.py
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

import sensor_data
from sensor_data import initialize_arduino
from rotate import rotate_360_clockwise, rotate_360_counterclockwise
from mailer import send_email
import asyncio
import threading
import time

import cv2
from fastapi.responses import StreamingResponse
import threading
import requests
from io import BytesIO
from PIL import Image
import numpy as np

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 Templates
templates = Jinja2Templates(directory="templates")

# Global flags for auto-actions
gas_window_opened = False
email_sent = False

# Global video configuration
PHONE_CAMERA_URL = "http://192.168.191.64:8080/video"  # CHANGE THIS to your phone's IP
USE_PHONE_CAMERA = True  # Set to True for phone, False for USB webcam
VIDEO_ROTATION = 90  # 0, 90, 180, or 270 degrees

video_capture = None
video_lock = threading.Lock()

class SensorData(BaseModel):
    temperature: float
    humidity: float
    flame_status: str
    gas_status: str

# Background thread to read Arduino data
def arduino_reader_thread():
    """Background thread to continuously read from Arduino"""
    print("Arduino reader thread started")
 
    
    loop_count = 0
    while True:
        try:
            loop_count += 1
            
            
            if sensor_data.arduino_reader and sensor_data.arduino_reader.connected:
                # Check if data is waiting
                if sensor_data.arduino_reader.ser and sensor_data.arduino_reader.ser.in_waiting > 0:
                    line = sensor_data.arduino_reader.read_line()
                    if line:
                        success = sensor_data.arduino_reader.parse_sensor_data(line)
                            
            time.sleep(0.01)
            
        except Exception as e:
            print(f"❌ Error in reader thread: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(1)

# NEW: Background thread for automatic safety actions
def safety_monitor_thread():
    """Monitor sensors and take automatic safety actions"""
    global gas_window_opened, email_sent
    
    print("Safety monitor thread started")
    
    while True:
        try:
            if sensor_data.arduino_reader and sensor_data.arduino_reader.connected:
                # Get current sensor readings
                flame_status = sensor_data.read_flame_status()
                gas_status = sensor_data.read_gas_status()
                
                # AUTO-OPEN WINDOW IF GAS DETECTED
                if gas_status == "Gas detected!" and not gas_window_opened:
                    rotate_360_counterclockwise()
                    gas_window_opened = True
                
                # Reset flag when gas clears
                if gas_status == "No gas detected." and gas_window_opened:
                    gas_window_opened = False
                
                # SEND EMAIL IF FLAME DETECTED
                if flame_status != "No Flame" and not email_sent:
                    try:
                        # Using asyncio.run to call async function from sync thread
                        asyncio.run(send_email(
                            "mdshazid121@gmail.com",
                            "Fire Detected",
                            "I wanted to let you know that there's a fire at my house right now. Please contact the fire department and rescue team. I'll update you soon."
                        ))
                        email_sent = True
                        print("✅ Email alert sent")
                    except Exception as e:
                        print(f"❌ Failed to send email: {e}")
                
                # Reset flag when flame is gone
                if flame_status == "No Flame" and email_sent:
                    print("✓ Flame cleared, resetting email flag")
                    email_sent = False
            
            # Check every second
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error in safety monitor: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(5)

@app.on_event("startup")
async def startup_event():
    """Initialize Arduino connection on startup"""
    print("\n" + "=" * 60)
    print("STARTING UP APPLICATION")
    print("=" * 60)
    
    print(f"Attempting to connect to Arduino on COM5...")
    
    try:
        if initialize_arduino(port='COM5'):
            print("✅ Arduino initialization returned True")
            
            if sensor_data.arduino_reader is None:
                print("❌ ERROR: arduino_reader is None despite successful initialization!")
                return
            
            # Start background thread to read Arduino data
            print("Starting Arduino reader thread...")
            reader_thread = threading.Thread(target=arduino_reader_thread, daemon=True)
            reader_thread.start()
            print(f"Reader thread started and alive: {reader_thread.is_alive()}")
            
            # Start safety monitor thread
            print("Starting safety monitor thread...")
            safety_thread = threading.Thread(target=safety_monitor_thread, daemon=True)
            safety_thread.start()
            print(f"Safety thread started and alive: {safety_thread.is_alive()}")
            
            print("=" * 60 + "\n")
        else:
            print("❌ Failed to connect to Arduino")
            print("=" * 60 + "\n")
    except Exception as e:
        print(f"❌ Exception during startup: {e}")
        import traceback
        traceback.print_exc()

@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect Arduino on shutdown"""
    if sensor_data.arduino_reader:
        sensor_data.arduino_reader.disconnect()

# Monitor sensors via WebSocket (simplified - no auto-actions here)
async def monitor_sensors(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        try:
            # Read sensor data
            temperature, humidity = sensor_data.read_temperature_and_humidity()
            flame_status = sensor_data.read_flame_status()
            gas_status = sensor_data.read_gas_status()
            window_status = sensor_data.get_window_status()
            
            if temperature is None or humidity is None:
                await websocket.send_json({"error": "Failed to read sensor data"})
                await asyncio.sleep(1)
                continue

            data = {
                "temperature": temperature,
                "humidity": humidity,
                "flame_status": flame_status,
                "gas_status": gas_status,
                "window_status": window_status
            }

            # Send data to WebSocket client
            await websocket.send_json(data)
            
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"WebSocket error: {e}")
            break

#video section

def rotate_frame(frame, angle):
    """Rotate frame by specified angle"""
    if angle == 90:
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(frame, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        return frame
    
def get_video_capture():
    """Initialize video capture"""
    global video_capture
    with video_lock:
        if video_capture is None or not video_capture.isOpened():
            if USE_PHONE_CAMERA:
                video_capture = cv2.VideoCapture(PHONE_CAMERA_URL)
            else:
                video_capture = cv2.VideoCapture(0)
            
            video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            video_capture.set(cv2.CAP_PROP_FPS, 30)
        return video_capture

def generate_frames():
    """Generate video frames from camera"""
    camera = get_video_capture()
    
    while True:
        with video_lock:
            success, frame = camera.read()
            
        if not success:
            print("Failed to read frame from camera")
            time.sleep(1)
            camera = get_video_capture()
            continue
        else:
            # Apply rotation
            frame = rotate_frame(frame, VIDEO_ROTATION)
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            
            if not ret:
                continue
                
            frame = buffer.tobytes()
            
            # Yield frame in multipart format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await monitor_sensors(websocket)

# Home Route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})

# Control Route
@app.get("/control", response_class=HTMLResponse)
async def control(request: Request):
    return templates.TemplateResponse("control.html", {"request": request})

@app.post("/control/open")
async def open_control():
    try:
        window_status = sensor_data.get_window_status()
        if window_status == "Closed":
            rotate_360_counterclockwise()
            await asyncio.sleep(0.5)
            return {"status": "success", "message": "Window opened"}
        return {"status": "success", "message": "Window already open"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/control/close")
async def close_control():
    try:
        window_status = sensor_data.get_window_status()
        if window_status == "Open":
            rotate_360_clockwise()
            await asyncio.sleep(0.5)
            return {"status": "success", "message": "Window closed"}
        return {"status": "success", "message": "Window already closed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/control/status")
async def control_status():
    try:
        window_status = sensor_data.get_window_status()
        return {"status": "success", "window_status": window_status}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Add this to app.py after the existing control endpoints

@app.post("/control/buzzer/on")
async def buzzer_on():
    try:
        if sensor_data.arduino_reader and sensor_data.arduino_reader.connected:
            sensor_data.arduino_reader.send_command("BUZZER_ON")
            await asyncio.sleep(0.5)
            return {"status": "success", "message": "Buzzer activated"}
        return {"status": "error", "message": "Arduino not connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/control/buzzer/off")
async def buzzer_off():
    try:
        if sensor_data.arduino_reader and sensor_data.arduino_reader.connected:
            sensor_data.arduino_reader.send_command("BUZZER_OFF")
            await asyncio.sleep(0.5)
            return {"status": "success", "message": "Buzzer deactivated"}
        return {"status": "error", "message": "Arduino not connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@app.get("/video_feed")
async def video_feed():
    """Video streaming route"""
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/video", response_class=HTMLResponse)
async def video_page(request: Request):
    """Video page route"""
    return templates.TemplateResponse("video.html", {"request": request})

@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect Arduino and release camera on shutdown"""
    global video_capture
    
    if sensor_data.arduino_reader:
        sensor_data.arduino_reader.disconnect()
    
    # Release camera
    if video_capture is not None:
        video_capture.release()
        print("Camera released")