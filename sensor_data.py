# sensor_data.py
import RPi.GPIO as GPIO  # For reading flame sensor data
import adafruit_dht
import board

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
    # Set the sensor type to DHT11
    dht_device = adafruit_dht.DHT11(board.D14)
    temperature = 25
    humidity = 75
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
    except RuntimeError as error:
        print("error reading data")
    finally:
        dht_device.exit()

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

