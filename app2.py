# app.py
from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from sensor_data import read_temperature_and_humidity, read_flame_status, read_gas_status  # Import sensor functions
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

# Simulated Sensor Data
async def monitor_sensors(websocket: WebSocket):
    await websocket.accept()
    email_sent = False  # To avoid sending duplicate emails
    while True:
        # Read sensor data
        temperature, humidity = read_temperature_and_humidity()
        flame_status = read_flame_status()
        gas_status = read_gas_status()
        print(temperature, humidity, flame_status, gas_status)
        if temperature is None or humidity is None:
            await websocket.send_json({"error": "Failed to read sensor data"})
            await asyncio.sleep(1)
            continue

        data = {
            "temperature": 25.5,
            "humidity": 60,
            "flame_status": "No Flame",
            "gas_status": "Safe"
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

        await asyncio.sleep(1)  # Update every 1 second

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("how")
    await monitor_sensors(websocket)

# Home Route (Shows HTML page)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})

