// home_monitoring_system.ino
#include <DHT.h>
#include <Servo.h>

// Pin definitions
#define DHT_PIN 2          // DHT11 data pin
#define DHT_TYPE DHT22
#define FLAME_PIN 3        // Flame sensor digital pin
#define GAS_PIN 4          // MQ2 digital pin
#define SERVO_PIN 9        // Servo control pin

// Initialize sensors
DHT dht(DHT_PIN, DHT_TYPE);
Servo windowServo;

// Variables
int servoPosition = 0;  // 0 = closed, 1 = open
unsigned long lastSensorRead = 0;
const long sensorInterval = 1000;  // Read sensors every 1 second

void setup() {
  Serial.begin(9600);
  
  // Initialize DHT11
  dht.begin();
  
  // Initialize flame sensor
  pinMode(FLAME_PIN, INPUT);
  
  // Initialize gas sensor
  pinMode(GAS_PIN, INPUT);
  
  // Initialize servo
  windowServo.attach(SERVO_PIN);
  windowServo.write(90);  // Start at neutral position
  
  Serial.println("Arduino Home Monitoring System Ready");
}

void loop() {
  // Check for commands from laptop
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    handleCommand(command);
  }
  
  // Read and send sensor data periodically
  unsigned long currentMillis = millis();
  if (currentMillis - lastSensorRead >= sensorInterval) {
    lastSensorRead = currentMillis;
    sendSensorData();
  }
}

void handleCommand(String command) {
  if (command == "OPEN") {
    openWindow();
    Serial.println("ACK:OPEN");
  } else if (command == "CLOSE") {
    closeWindow();
    Serial.println("ACK:CLOSE");
  } else if (command == "STATUS") {
    sendSensorData();
  }
}

void openWindow() {
  if (servoPosition == 0) {
    // Rotate counterclockwise (adjust angles based on your servo)
    windowServo.write(180);  // Full counterclockwise
    delay(300);
    windowServo.write(90);   // Stop
    servoPosition = 1;
  }
}

void closeWindow() {
  if (servoPosition == 1) {
    // Rotate clockwise
    windowServo.write(0);    // Full clockwise
    delay(300);
    windowServo.write(90);   // Stop
    servoPosition = 0;
  }
}

void sendSensorData() {
  // Read temperature and humidity
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  
  // Read flame sensor (assuming LOW = flame detected)
  int flameValue = digitalRead(FLAME_PIN);
  String flameStatus = (flameValue == LOW) ? "Flame Detected" : "No Flame";
  
  // Read gas sensor (assuming LOW = gas detected)
  int gasValue = digitalRead(GAS_PIN);
  String gasStatus = (gasValue == LOW) ? "Gas detected!" : "No gas detected.";
  
  // Check if DHT reading failed
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("ERROR:DHT_READ_FAILED");
    return;
  }
  
  // Send data in a structured format
  // Format: DATA|temperature|humidity|flame_status|gas_status|window_status
  Serial.print("DATA|");
  Serial.print(temperature, 2);
  Serial.print("|");
  Serial.print(humidity, 2);
  Serial.print("|");
  Serial.print(flameStatus);
  Serial.print("|");
  Serial.print(gasStatus);
  Serial.print("|");
  Serial.println(servoPosition == 1 ? "Open" : "Closed");
}