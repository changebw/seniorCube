#include <WiFi.h>
#include <WiFiClient.h>
#include <TM1637Display.h>

#define CLK_PIN  22 // The ESP32 pin GPIO22 connected to CLK
#define DIO_PIN  23 // The ESP32 pin GPIO23 connected to DIO

const char* ssid = "XXX";
const char* password = "XXX";

WiFiServer server(80);

// Static IP setup
IPAddress local_IP(172,20,10,6);
IPAddress gateway(172,20,10,1);
IPAddress subnet(255, 255, 255, 240);
IPAddress primaryDNS(8, 8, 8, 8);
IPAddress secondaryDNS(8, 8, 4, 4);

String sendString = "00:00";
const int left = 32;
const int right = 33;
unsigned long starttime = 0;
unsigned long elapsedtime = 0;
bool timing = false;

TM1637Display display(CLK_PIN, DIO_PIN);

void setup() {
  //hand sensor pins
  pinMode(left, INPUT_PULLUP);
  pinMode(right, INPUT_PULLUP);

  Serial.begin(115200);

  // clear display and send welcome msg
  display.setBrightness(7);
  display.clear();
  display.showNumberDecEx(0, 0b01000000, true); // Display "00:00"

  Serial.println("PLACE HANDS ON BUTTONS TO START");
  espSetup();
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

void loop() {

  WiFiClient client = server.available();
  if (client){
    Serial.println("New Client connected");
    String currentLine = "";
    while (client.connected()){
      if (client.available()){
        char c = client.read();
        if (c != '\r' && c != '\n'){
          currentLine += c;
        }
        else {
          currentLine = "";
        }
        int msg_size = 0;

        if (!timing && (digitalRead(left) == LOW && digitalRead(right) == LOW)) {
          display.clear();
          display.showNumberDecEx(0, 0b01000000, true); // Display "00:00"
          Serial.println("REMOVE YOUR HANDS TO START TIMER");

          while (digitalRead(left) == LOW && digitalRead(right) == LOW) {
            // Wait for hands to be removed
            delay(100);
          }

          starttime = millis();
          timing = true;
          sendString = "00:00";
        }

        if (timing) {
          elapsedtime = millis() - starttime;

          int milliseconds = elapsedtime % 1000;
          int seconds = (elapsedtime / 1000) % 60;
          int minutes = (elapsedtime / 1000) / 60;

          // Update the display to show elapsed time in MM:SS.ss format
          int displayValue = minutes * 100 + seconds;
          int hundredths = milliseconds / 10;

          String secondString = "";
          String minuteString = "";

          if (seconds < 10) {
            secondString = "0" + String(seconds);
          }
          else {
            secondString = String(seconds);
          }
          if (minutes < 10) {
            minuteString = "0" + String(minutes);
          }
          else {
            minuteString = String(minutes);
          }

          // float sendValue = displayValue * 100 + hundredths;
          sendString = String(minutes) + ":" + secondString + "." + String(milliseconds);

          display.showNumberDecEx(displayValue * 100 + hundredths, 0b01000000, true); // Display elapsed time with hundredths of a second

          // Check if hands are back on the buttons to stop the timer
          if (digitalRead(left) == LOW && digitalRead(right) == LOW) {
            while (digitalRead(left) == LOW || digitalRead(right) == LOW) {
              // Wait for hands to be back
              delay(100);
            }
            timing = false;

            display.showNumberDecEx(displayValue * 100 + hundredths, 0b01000000, true); // Display final time with hundredths of a second
            delay(1000); // 
            // Reset the display to zero
            display.showNumberDecEx(0, 0b01000000, true);
          }
        }

        if (currentLine.endsWith("GET /time")){
          Serial.println(currentLine);
          // msg_size = sendString.length();
          // client.println(msg_size);
          client.println(sendString);
        }
      }
    }
    if (client){
      client.stop();
    }
    Serial.println("Client Disconnected.");
  }

  

  // while(espSerial.available()){
  //     fmsg += (char)espSerial.read();
  //     delay(2);
  // }
  // msg = getString(fmsg);
  // fmsg = "";

  // if (msg == "GET /time\r\n" || msg == "GET /timd\r\n" || msg == "GET /tile\r\n" || msg == "GET /thme\r\n" || msg == "GDT /time\r\n") {
  //     Serial.println("RECEIVED FROM WEBPAGE: " + msg);
  //     int connectionId = 0;
  //     if (espSerial.find("+IPD,")){
  //       connectionId = espSerial.read()-48;
  //     }
  //     String cipSend = "AT+CIPSEND=";
  //     cipSend += connectionId;
  //     cipSend += ",";
  //     cipSend += sendString.length();
  //     cipSend += "\r\n";

  //     Serial.println("CIPSEND IS: " + cipSend);
  //     Serial.println("SEND STRING IS: " + sendString);

  //     sendData(cipSend, 50, true);
  //     sendData(sendString, 50, true);
  //   }
}
