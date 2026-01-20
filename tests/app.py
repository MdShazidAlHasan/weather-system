# app.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from sensor_data import read_temperature_and_humidity, read_flame_status, read_gas_status  # Import sensor functions
from mailer import send_email


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

# Simulated Sensor Data Route (Now reads real sensor data)
@app.get("/data")
async def get_sensor_data():
    # Get temperature and humidity from DHT11
    temperature, humidity = read_temperature_and_humidity()
    flame_status = read_flame_status()
    gas_status = read_gas_status()

    if temperature is None or humidity is None:
        return {"error": "Failed to read sensor data"}

    data = SensorData(
        temperature=temperature,
        humidity=humidity,
        flame_status=flame_status,
        gas_status=gas_status 
    )
    return data

# Home Route (Shows HTML page)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Get sensor data
    data = await get_sensor_data()
    # Create an example message payload
    if not data.flame_status == "No Flame":
        await send_email("mdshazid121@gmail.com", "Flame Detected", "There is an serious issue")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "flame_status": data.flame_status
    })

