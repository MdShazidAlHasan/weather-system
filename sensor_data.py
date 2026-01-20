# sensor_data.py
import serial
import time
import threading

# Global Arduino reader instance
arduino_reader = None

class ArduinoSensorReader:
    def __init__(self, port='COM5', baudrate=9600):
        """Initialize Arduino connection"""
        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.latest_data = {
            'temperature': 25.0,
            'humidity': 75.0,
            'flame_status': 'No Flame',
            'gas_status': 'No gas detected.',
            'window_status': 'Closed'
        }
        self.lock = threading.Lock()
        self.connected = False
        print(f"ArduinoSensorReader object created for port {port}")
        
    def connect(self):
        """Connect to Arduino"""
        try:
            print(f"Opening serial connection to {self.port}...")
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Serial port opened, waiting 2 seconds for Arduino reset...")
            time.sleep(2)  # Wait for Arduino to reset
            # Flush any initial data
            self.ser.reset_input_buffer()
            self.connected = True
            print(f"✅ Connected to Arduino on {self.port}")
            return True
        except serial.SerialException as e:
            print(f"❌ Error connecting to Arduino: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from Arduino"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.connected = False
            print("Disconnected from Arduino")
    
    def send_command(self, command):
        """Send command to Arduino"""
        if not self.connected or not self.ser:
            print("Cannot send command: Not connected")
            return False
        try:
            self.ser.write(f"{command}\n".encode())
            print(f"Sent command: {command}")
            time.sleep(0.1)
            return True
        except Exception as e:
            print(f"Error sending command: {e}")
            return False
    
    def read_line(self):
        """Read a line from Arduino"""
        if not self.connected or not self.ser:
            return None
        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                return line
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
        return None
    
    def parse_sensor_data(self, line):
        """Parse sensor data from Arduino"""
        if line and line.startswith("DATA|"):
            try:
                parts = line.split("|")
                if len(parts) >= 6:
                    with self.lock:
                        self.latest_data = {
                            'temperature': float(parts[1]),
                            'humidity': float(parts[2]),
                            'flame_status': parts[3],
                            'gas_status': parts[4],
                            'window_status': parts[5]
                        }
                    return True
            except Exception as e:
                print(f"Error parsing data: {e}")
        return False
    
    def get_latest_data(self):
        """Get the latest sensor data"""
        with self.lock:
            return self.latest_data.copy()
    
    def open_window(self):
        """Send command to open window"""
        return self.send_command("OPEN")
    
    def close_window(self):
        """Send command to close window"""
        return self.send_command("CLOSE")



def initialize_arduino(port='COM5'):
    """Initialize the Arduino connection"""
    global arduino_reader
    print(f"initialize_arduino() called with port={port}")
    
    arduino_reader = ArduinoSensorReader(port=port)
    success = arduino_reader.connect()
    
    if not success:
        print("Connection failed, setting arduino_reader to None")
        arduino_reader = None
    else:
        print(f"Connection successful, arduino_reader is set")
    
    return success

def read_temperature_and_humidity():
    """Read temperature and humidity from Arduino"""
    if arduino_reader and arduino_reader.connected:
        data = arduino_reader.get_latest_data()
        return data['temperature'], data['humidity']
    return None, None

def read_flame_status():
    """Read flame status from Arduino"""
    if arduino_reader and arduino_reader.connected:
        data = arduino_reader.get_latest_data()
        return data['flame_status']
    return "No Flame"

def read_gas_status():
    """Read gas status from Arduino"""
    if arduino_reader and arduino_reader.connected:
        data = arduino_reader.get_latest_data()
        return data['gas_status']
    return "No gas detected."

def get_window_status():
    """Get current window status"""
    if arduino_reader and arduino_reader.connected:
        data = arduino_reader.get_latest_data()
        return data['window_status']
    return "Closed"