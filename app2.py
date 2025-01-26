# app.py
from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from sensor_data import read_temperature_and_humidity, read_flame_status, read_gas_status  # Import sensor functions
from rotate import rotate_360_clockwise, rotate_360_counterclockwise
from mailer import send_email
import asyncio

app = FastAPI()

# Serve static files (like CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 Templates
templates = Jinja2Templates(directory="templates")

class SensorData(BaseModel):
    temperature: float
    humidity: float
    flame_status: str
    gas_status: str
not_open = 0
# Simulated Sensor Data
async def monitor_sensors(websocket: WebSocket):
    global not_open
    await websocket.accept()
    email_sent = False  # To avoid sending duplicate emails
    while True:
        # Read sensor data
        temperature, humidity = read_temperature_and_humidity()
        flame_status = read_flame_status()
        gas_status = read_gas_status()
        if temperature is None or humidity is None:
            await websocket.send_json({"error": "Failed to read sensor data"})
            await asyncio.sleep(1)
            continue

        data = {
            "temperature": temperature,
            "humidity":humidity,
            "flame_status": flame_status,
            "gas_status": gas_status
        }

        # Send data to WebSocket client
        await websocket.send_json(data)

        # Send email alert if flame is detected
        if flame_status != "No Flame" and not email_sent:
            await send_email("mdshazid121@gmail.com", "Flame Detected", "There is a serious issue")
            email_sent = True
        # Reset email_sent flag if flame is no longer detected
        if flame_status == "No Flame":
            email_sent = False

        if gas_status == "Gas detected!" and not not_open :
            rotate_360_counterclockwise()
            not_open = 1
            await asyncio.sleep(2)
        await asyncio.sleep(1)  # Update every 1 second

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await monitor_sensors(websocket)

# Home Route (Shows HTML page)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})


# Control Route (Shows HTML page)
# Control Route (GET method to render the control page)
@app.get("/control", response_class=HTMLResponse)
async def control(request: Request):
    return templates.TemplateResponse("control.html", {"request": request})

@app.post("/control/open")
async def open_control():
    global not_open
    try:
        if not not_open:
            not_open = 1
            await rotate_360_counterclockwise()  # Call the rotation function for "Open"
        return {"status": "success", "message": "Rotated counterclockwise (Open)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/control/close")
async def close_control():
    global not_open 
    try:
        if not_open:
            not_open = 0
            await rotate_360_clockwise()  # Call the rotation function for "Close"
        return {"status": "success", "message": "Rotated clockwise (Close)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@app.get("/control/status")
async def control_status():
    global not_open
    try:
        status = "Open" if not_open else "Closed"
        return {"status": "success", "window_status": status}
    except Exception as e:
        return {"status": "error", "message": str(e)}