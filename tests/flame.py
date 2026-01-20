import serial
import time


ARDUINO_PORT = 'COM5'  # CHANGE THIS TO YOUR PORT
BAUD_RATE = 9600

def read_flame_sensor():
    try:
        # Open serial connection
        print(f"Connecting to Arduino on {ARDUINO_PORT}...")
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        
        # Wait for Arduino to reset (important!)
        time.sleep(2)
        print("Connected! Reading flame sensor data...\n")
        
        # Read data continuously
        while True:
            if ser.in_waiting > 0:
                # Read a line from Arduino
                line = ser.readline().decode('utf-8').strip()
                
                # Print the data
                print(line)
                
    except serial.SerialException as e:
        print(f"Error: Could not connect to Arduino on {ARDUINO_PORT}")
        print(f"Details: {e}")
        print("\nTroubleshooting:")
        print("1. Check if Arduino is connected via USB")
        print("2. Verify the correct COM port")
        print("3. Close Arduino IDE Serial Monitor if open")
        
    except KeyboardInterrupt:
        print("\n\nStopping... Goodbye!")
        
    finally:
        # Close the serial connection
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    read_flame_sensor()