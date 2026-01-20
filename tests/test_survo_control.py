# test_servo_control.py
import sensor_data
from rotate import rotate_360_clockwise, rotate_360_counterclockwise
import time

print("=" * 60)
print("SERVO CONTROL TEST")
print("=" * 60)

# Step 1: Initialize Arduino connection
print("\n1. Connecting to Arduino on COM5...")
if sensor_data.initialize_arduino('COM5'):
    print("✅ Arduino connected successfully!")
else:
    print("❌ Failed to connect to Arduino")
    exit()

time.sleep(2)

# Step 2: Start reading thread to see Arduino responses
print("\n2. Starting to listen to Arduino...")
def listen_arduino():
    for i in range(5):
        line = sensor_data.arduino_reader.read_line()
        if line:
            print(f"   Arduino says: {line}")
        time.sleep(0.2)

listen_arduino()

# Step 3: Test OPEN command
print("\n3. Testing OPEN command (counterclockwise)...")
print("-" * 60)
result = rotate_360_counterclockwise()
print(f"   Command sent: {result}")
time.sleep(1)
listen_arduino()

# Wait before next command
print("\n   Waiting 3 seconds...")
time.sleep(3)

# Step 4: Test CLOSE command
print("\n4. Testing CLOSE command (clockwise)...")
print("-" * 60)
result = rotate_360_clockwise()
print(f"   Command sent: {result}")
time.sleep(1)
listen_arduino()

# Wait before next command
print("\n   Waiting 3 seconds...")
time.sleep(3)

# Step 5: Test multiple times
print("\n5. Rapid test - Opening and closing 3 times...")
print("-" * 60)
for i in range(3):
    print(f"\n   Round {i+1}:")
    
    print("   → Opening...")
    rotate_360_counterclockwise()
    time.sleep(2)
    
    print("   → Closing...")
    rotate_360_clockwise()
    time.sleep(2)

print("\n" + "=" * 60)
print("TEST COMPLETE!")
print("=" * 60)

# Step 6: Disconnect
print("\nDisconnecting from Arduino...")
sensor_data.arduino_reader.disconnect()
print("Done!")