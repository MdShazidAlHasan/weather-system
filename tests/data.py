import serial
import time

# Change COM3 to your actual port
ARDUINO_PORT = 'COM5'

print(f"Connecting to Arduino on {ARDUINO_PORT}...")
ser = serial.Serial(ARDUINO_PORT, 9600, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

print("Listening for data from Arduino...")
print("=" * 50)

for i in range(20):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"Received: {line}")
    else:
        print("No data available")
    time.sleep(0.5)

ser.close()
print("\nTest complete")