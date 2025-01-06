# sensor_data.py
import adafruit_dht
import RPi.GPIO as GPIO  # For reading flame sensor data

# Setup the GPIO pin for the flame sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN)  # Flame sensor connected to pin 17
# GPIO pin for the MQ2 digital output

MQ2_PIN = 23  # Use GPIO17 (Pin 11 on the Raspberry Pi)
# Setup GPIO
GPIO.setup(MQ2_PIN, GPIO.IN)

# Define the GPIO pin where the DHT11 data pin is connected



# Function to read temperature and humidity from DHT11 sensor
def read_temperature_and_humidity():
    # Initialize the DHT11 sensor
    dht_sensor = adafruit_dht.DHT11(14)

    temperature = dht_sensor.temperature
    humidity = dht_sensor.humidity
    dht_sensor.exit()

    if humidity is not None and temperature is not None:
        return round(temperature, 2), round(humidity, 2)
    else:
        return None, None
    

# Function to read flame status from the Flame sensor
def read_flame_status():
    # Flame sensor reading (pin 17)
    if GPIO.input(15):
        return "No Flame"
    else:
        return "Flame Detected"

def read_gas_status():
    gas_detected = GPIO.input(MQ2_PIN)
    if not gas_detected:
        return "Gas detected!"
    else:
        return "No gas detected."

