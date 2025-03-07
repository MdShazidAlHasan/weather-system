import RPi.GPIO as GPIO
import time

#close
def rotate_360_clockwise():
    servo_pin = 21  # GPIO pin connected to servo
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm = GPIO.PWM(servo_pin, 50)  # 50Hz frequency
    pwm.start(0)  # Start with a duty cycle of 0
    pwm.ChangeDutyCycle(9)  # Adjust duty cycle for clockwise rotation
    time.sleep(0.3)  # Rotate for 0.2 seconds
    pwm.ChangeDutyCycle(0)  # Stop servo
    pwm.stop()
    


#open 
def rotate_360_counterclockwise():
    servo_pin = 21  # GPIO pin connected to servo
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm = GPIO.PWM(servo_pin, 50)  # 50Hz frequency
    pwm.start(0)  # Start with a duty cycle of 0
    pwm.ChangeDutyCycle(5)  # Adjust duty cycle for counterclockwise rotation
    time.sleep(.3)  # Rotate for 0.2 seconds
    pwm.ChangeDutyCycle(0)  # Stop servo
    pwm.stop()
