# debug_commands.py
import serial
import time

ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)
print("Connected to Arduino")

# Clear any initial messages
time.sleep(1)
while ser.in_waiting > 0:
    print(f"Initial: {ser.readline().decode('utf-8', errors='ignore').strip()}")

print("\n" + "="*50)
print("Sending OPEN command...")
print("="*50)
ser.write(b"OPEN\n")
ser.flush()

# Wait and read ALL responses for 3 seconds
start_time = time.time()
while time.time() - start_time < 3:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f">>> {line}")
    time.sleep(0.1)

print("\n" + "="*50)
print("Sending CLOSE command...")
print("="*50)
ser.write(b"CLOSE\n")
ser.flush()

# Wait and read ALL responses for 3 seconds
start_time = time.time()
while time.time() - start_time < 3:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f">>> {line}")
    time.sleep(0.1)

ser.close()
print("\nTest complete")