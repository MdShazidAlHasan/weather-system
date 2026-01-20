# rotate.py
import sensor_data
import time

def rotate_360_clockwise():
    """Close window"""
    print("Attempting to close window...")
    
    # Use sensor_data.arduino_reader (not just arduino_reader)
    if sensor_data.arduino_reader and sensor_data.arduino_reader.connected:
        success = sensor_data.arduino_reader.close_window()
        time.sleep(0.5)
        print(f"Close command sent: {success}")
        return success
    
    print("Cannot close: Arduino not connected")
    print(f"Arduino reader exists: {sensor_data.arduino_reader is not None}")
    if sensor_data.arduino_reader:
        print(f"Arduino connected status: {sensor_data.arduino_reader.connected}")
    return False

def rotate_360_counterclockwise():
    """Open window"""
    print("Attempting to open window...")
    
    # Use sensor_data.arduino_reader (not just arduino_reader)
    if sensor_data.arduino_reader and sensor_data.arduino_reader.connected:
        success = sensor_data.arduino_reader.open_window()
        time.sleep(0.5)
        print(f"Open command sent: {success}")
        return success
    
    print("Cannot open: Arduino not connected")
    print(f"Arduino reader exists: {sensor_data.arduino_reader is not None}")
    if sensor_data.arduino_reader:
        print(f"Arduino connected status: {sensor_data.arduino_reader.connected}")
    return False