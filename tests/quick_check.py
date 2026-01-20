# quick_check.py
import serial
import time

ser = serial.Serial('COM5', 9600, timeout=1)
print("Connected on COM5 (even though FastAPI is also connected)")
time.sleep(0.5)

for i in range(5):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print(f"Received: {line}")
    time.sleep(1)

ser.close()