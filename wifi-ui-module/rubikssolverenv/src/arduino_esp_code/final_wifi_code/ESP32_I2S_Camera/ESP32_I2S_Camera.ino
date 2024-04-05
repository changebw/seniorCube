/*
 Modified code from https://github.com/bitluni/ESP32CameraI2S
 Which was originally modified from https://github.com/igrr/esp32-cam-demo
*/

#include "OV7670.h"
#include <WiFi.h>
#include <WiFiClient.h>
#include "BMP.h"
#include <string>

const int SIOD = 21; //SDA
const int SIOC = 22; //SCL

const int VSYNC = 34;
const int HREF = 35;

const int XCLK = 32;
const int PCLK = 33;

const int D0 = 27;
const int D1 = 17;
const int D2 = 16;
const int D3 = 15;
const int D4 = 14;
const int D5 = 13;
const int D6 = 12;
const int D7 = 4;

const char* ssid = "XXX";
const char* password = "XXX";

OV7670 *camera;

WiFiServer server(80);

// Static IP setup
IPAddress local_IP(172,20,10,9);
IPAddress gateway(172,20,10,1);
IPAddress subnet(255, 255, 255, 240);
IPAddress primaryDNS(8, 8, 8, 8);
IPAddress secondaryDNS(8, 8, 4, 4);

unsigned char bmpHeader[BMP::headerSize];

void setup() {
  espAndCameraSetup();
}

void espAndCameraSetup() {
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
  
  Serial.println("Initializing OV7670 and BMP Header...");
  camera = new OV7670(OV7670::Mode::QQVGA_RGB565, SIOD, SIOC, VSYNC, HREF, XCLK, PCLK, D0, D1, D2, D3, D4, D5, D6, D7);
  BMP::construct16BitHeader(bmpHeader, camera->xres, camera->yres);
  Serial.println("Done.");
  
  Serial.println("Starting server...");
  server.begin();
  Serial.println("Done.");
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

        // PASS TO ESP32_MOTORS code, keeping here for reference if needed
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
        }
        if (currentLine.endsWith("POST /solve HTTP/1.1")) {
          Serial.println(currentLine);
            
          msg_size = strlen("HTTP/1.1 200 OK");
          client.println(msg_size);
          client.println("HTTP/1.1 200 OK");
        }

        if (currentLine.endsWith("SENTSOLVE")) {
          std::string moves = std::string(currentLine.c_str());
          int startIdx = moves.find_first_of("S");
          moves.erase(startIdx,9);
          String moveString = "";
          for (char c : moves){
            moveString += c;
          }
          Serial.println("MOVES ARE: " + moveString);
        }

        if (currentLine.endsWith("POST /move HTTP/1.1")) {
          Serial.println(currentLine);
            
          msg_size = strlen("HTTP/1.1 200 OK");
          client.println(msg_size);
          client.println("HTTP/1.1 200 OK");
        }

        if (currentLine.endsWith("SENTMOVE")) {
          std::string moves = std::string(currentLine.c_str());
          int startIdx = moves.find_first_of("S");
          moves.erase(startIdx,8);
          String moveString = "";
          for (char c : moves){
            moveString += c;
          }
          Serial.println("MOVE IS: " + moveString);
        }

        if (currentLine.endsWith("GET /camera HTTP/1.1"))
        {
            Serial.println(currentLine);
            
            msg_size = strlen("HTTP/1.1 200 OK");
            client.println(msg_size);
            client.println("HTTP/1.1 200 OK");
        }

        if (currentLine.endsWith("ackResponse")) {
          Serial.println(currentLine);
          msg_size = strlen("Content-type:image/bmp");
          client.println(msg_size);
          client.println("Content-type:image/bmp");
        }

        if (currentLine.endsWith("ackContentType")) {
          Serial.println(currentLine);
          msg_size = strlen("SETUPDONE");
          client.println(msg_size);
          client.println("SETUPDONE");
        }

        if (currentLine.endsWith("ackSetupDone")) {
          Serial.println(currentLine);
          msg_size = BMP::headerSize;
          camera->oneFrame();
          delay(100);
          client.write(bmpHeader,BMP::headerSize);
          client.write(camera->frame, camera->xres * camera->yres*2);
          client.write("sent");
          sent = true;
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



