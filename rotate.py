import RPi.GPIO as GPIO
import time
from gpiozero import Servo
servo = Servo(21)  # GPIO pin connected to the servo
# Function to rotate servo 360° clockwise for 0.2 seconds
def rotate_360_clockwise():
    servo.value = 1  # Full clockwise rotation
    time.sleep(.3)
    servo.value = 0  # Stop the servo


# Function to rotate servo 360° counterclockwise for 0.2 seconds
def rotate_360_counterclockwise():
      # Clean up GPIO settings
    servo.value = -1  # Full counterclockwise rotation
    time.sleep(.3)
    servo.value = 0 