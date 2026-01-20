# simple_servo_test.py
import serial
import time

print("Simple Servo Test")
print("-" * 40)

# Connect to Arduino
ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)
print("Connected to COM5")

# Clear buffer
while ser.in_waiting > 0:
    ser.readline()

# Test OPEN
print("\nSending OPEN command...")
ser.write(b"OPEN\n")
ser.flush()
time.sleep(2)

# Read responses
print("Arduino responses:")
for i in range(10):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"  {line}")
    time.sleep(0.2)

# Test CLOSE
print("\nSending CLOSE command...")
ser.write(b"CLOSE\n")
ser.flush()
time.sleep(2)

# Read responses
print("Arduino responses:")
for i in range(10):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"  {line}")
    time.sleep(0.2)

ser.close()
print("\nDone!")