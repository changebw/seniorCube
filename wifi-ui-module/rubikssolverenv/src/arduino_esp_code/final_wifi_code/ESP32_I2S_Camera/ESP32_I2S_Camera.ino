/*
 Modified code from https://github.com/bitluni/ESP32CameraI2S
 Which was originally modified from https://github.com/igrr/esp32-cam-demo
*/

#include <base64.hpp>

#include "OV7670.h"

#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClient.h>
#include "BMP.h"

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
const char* password = "XXXXX";

OV7670 *camera;

WiFiServer server(80);

unsigned char bmpHeader[BMP::headerSize];

void setup() 
{
  Serial.begin(115200);

  Serial.println("setting STA mode");

  WiFi.mode(WIFI_STA);
  Serial.println("done setting STA mode");
  delay(1000);

  WiFi.begin(ssid, password);
  delay(1000);

  while (WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.println("waiting...");
  }

  Serial.println("connected");

  delay(1000);
  Serial.println(WiFi.localIP());
  delay(1000);
  
  camera = new OV7670(OV7670::Mode::QQVGA_RGB565, SIOD, SIOC, VSYNC, HREF, XCLK, PCLK, D0, D1, D2, D3, D4, D5, D6, D7);

  BMP::construct16BitHeader(bmpHeader, camera->xres, camera->yres);
  
  server.begin();
}


void loop()
{
  serve();
}

void serve()
{
  WiFiClient client = server.available();
  if (client) 
  {
    Serial.println("New Client connected");
    String currentLine = "";
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
        }
      }
    }
    // close the connection:
    if (client) {
      client.stop();
    }
    Serial.println("Client Disconnected.");
  }  
}



