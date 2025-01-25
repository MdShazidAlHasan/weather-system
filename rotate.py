import RPi.GPIO as GPIO
import time

# Initialize GPIO
servo_pin = 21  # GPIO pin connected to servo
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)


# Function to rotate servo 360° clockwise
def rotate_360_clockwise():
    servo_pin = 21  # GPIO pin connected to servo
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm = GPIO.PWM(servo_pin, 50)  # 50Hz frequency
    pwm.start(0)  # Start with a duty cycle of 0
    print("Rotating 360° clockwise...")
    pwm.ChangeDutyCycle(10)  # Adjust duty cycle for clockwise rotation
    time.sleep(1)  # Adjust sleep duration based on servo speed
    pwm.ChangeDutyCycle(0)  # Stop servo
    pwm.stop()

# Function to rotate servo 360° counterclockwise
def rotate_360_counterclockwise():
    servo_pin = 21  # GPIO pin connected to servo
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm = GPIO.PWM(servo_pin, 50)  # 50Hz frequency
    pwm.start(0)  # Start with a duty cycle of 0
    print("Rotating 360° counterclockwise...")
    pwm.ChangeDutyCycle(5)  # Adjust duty cycle for counterclockwise rotation
    time.sleep(1)  # Adjust sleep duration based on servo speed
    pwm.ChangeDutyCycle(0)  # Stop servo
    pwm.stop()

