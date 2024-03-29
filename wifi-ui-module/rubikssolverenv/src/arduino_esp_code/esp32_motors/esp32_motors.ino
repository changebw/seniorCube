#include <WiFi.h>
#include <WiFiClient.h>
#include <string>

// Wi-Fi stuff
WiFiServer server(80);

const char* ssid = "XXX";
const char* password = "XXX";

// Static IP setup
IPAddress local_IP(172,20,10,9);
IPAddress gateway(172,20,10,1);
IPAddress subnet(255, 255, 255, 240);
IPAddress primaryDNS(8, 8, 8, 8);
IPAddress secondaryDNS(8, 8, 4, 4);

// Stepper Motor stuff
const int stepPins[] = {22,26, 30, 34, 38};
const int dirPins[] = {23, 27, 31, 35, 39};
const int stepsPerRevolution = 200; // Number of steps per revolution for all motors

// MOTORS
// Motor 1: Left
// Motor 2: Right
// Motor 3: Front
// Motor 4: Back
// Motor 5: Bottom

void setup() {

  // Setup wifi server
  espSetup();

  // Sets the pins as Outputs
  for (int i = 0; i < 5; i++) {
    pinMode(stepPins[i], OUTPUT);
    pinMode(dirPins[i], OUTPUT);
    // Set all motor control pins to a known state (LOW)
    digitalWrite(dirPins[i], LOW);
    digitalWrite(stepPins[i], LOW);
  }
}

void espSetup() {
  Serial.begin(115200);

  Serial.println("Setting STA mode...");
  WiFi.mode(WIFI_STA);
  delay(100);
  Serial.println("Done");

  Serial.println("Setting static IP address...");

  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)){
    Serial.println("STA Static IP failed to configure.");
  }
  else {
    Serial.println("STA Static IP configured successfully.");
  }

  Serial.println("Connecting to WiFi network...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED){
    delay(100);
    Serial.println("Connecting...");
  }

  Serial.println("Successfully Connected to WiFi with IP:");
  Serial.println(WiFi.localIP());
  delay(100);
  
  Serial.println("Starting server...");
  server.begin();
  Serial.println("Done.");
}

// Function to rotate a motor by a specified angle
void rotateMotor(int motorNumber, int angle) {
  int steps = angle * stepsPerRevolution / 360; // Convert angle to steps
  int stepPin = stepPins[motorNumber - 1]; // Adjust motor number to array index
  int dirPin = dirPins[motorNumber - 1]; // Adjust motor number to array index
  digitalWrite(dirPin, steps > 0 ? HIGH : LOW); // Set direction
  for (int x = 0; x < abs(steps); x++) { // Number of pulses
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }
}

void loop() {
  serve();
}

void serve() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New Client connected");
    String currentLine = "";
    bool sent = false;
    while (client.connected()) 
    {
      if (client.available()) 
      {
        char c = client.read();
        if (c != '\r' && c != '\n'){
          currentLine += c;
        }
        else {
          currentLine = "";
        }
        int msg_size = 0;

        // Serial.println(currentLine);

        if (currentLine.endsWith("POST /scramble HTTP/1.1")) {
          Serial.println(currentLine);
            
          msg_size = strlen("HTTP/1.1 200 OK");
          client.println(msg_size);
          client.println("HTTP/1.1 200 OK");
        }

        if (currentLine.endsWith("SENTSCRAMBLE")) {
          std::string moves = std::string(currentLine.c_str());
          int startIdx = moves.find_first_of("S");
          moves.erase(startIdx,12);
          String moveString = "";
          for (char c : moves){
            moveString += c;
          }
          Serial.println("MOVES ARE: " + moveString);

          //RUuBLlR

          // for i in string
          // rotate motor based on move
          for (int i = 0; i < moveString.length(); i++){
            if (moveString[i] == "L"){
              rotateMotor(1, 90);
            }
            else if (moveString[i] == "l"){
              rotateMotor(1, -90);
            }
            else if (moveString[i] == "R"){
              rotateMotor(2, 90);
            }
            else if (moveString[i] == "r"){
              rotateMotor(2, -90);
            }
            else if (moveString[i] == "F"){
              rotateMotor(3, 90);
            }
            else if (moveString[i] == "f"){
              rotateMotor(3, -90);
            }
            else if (moveString[i] == "B"){
              rotateMotor(4, 90);
            }
            else if (moveString[i] == "b"){
              rotateMotor(4, -90);
            }
            else if (moveString[i] == "D"){
              rotateMotor(5, 90);
            }
            else if (moveString[i] == "d"){
              rotateMotor(5, -90);
            }
          }
        }
      }
    }
    // close the connection:
    if (client && sent) {
      client.stop();
    }
    Serial.println("Client Disconnected.");
  }  
}


// rotateMotor(1, 90);  // Turn motor 1 by 90 degrees
//   delay(2000);
//   rotateMotor(3, 180); // Turn motor 3 by 180 degrees
//   delay(2000);
//   rotateMotor(1, -90);  // Turn motor 1 by -90 degrees
//   delay(2000);
//   rotateMotor(2, 180); // Turn motor 2 by 180 degrees
//   delay(2000);
//   rotateMotor(4, 90);  // Turn motor 4 by 90 degrees
//   delay(2000);
//   rotateMotor(2, -90); // Turn motor 2 by -90 degrees
//   delay(2000);

