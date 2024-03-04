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

//const int TFT_DC = 2;
//const int TFT_CS = 5;
//DIN <- MOSI 23
//CLK <- SCK 18

const char* ssid = "XXX";
const char* password = "XXX";

OV7670 *camera;

WiFiMulti wifiMulti;
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
  camera->oneFrame();
  serve();
}

void serve()
{
  // Serial.println("Inside serve function");
  WiFiClient client = server.available();
  if (client) 
  {
    // Serial.println("New Client connected");
    String currentLine = "";
    while (client.connected()) 
    {
      if (client.available()) 
      {
        char c = client.read();
        Serial.println(c);
        if (c == '\n') 
        {
          if (currentLine.length() == 0) 
          {
            // client.println("HTTP/1.1 200 OK");
            // client.println("Content-type:text/html");
            // client.println();
            // client.print(
            //   "<style>body{margin: 0}\nimg{height: 100%; width: auto}</style>"
            //   "<img id='a' src='/camera' onload='this.style.display=\"initial\"; var b = document.getElementById(\"b\"); b.style.display=\"none\"; b.src=\"camera?\"+Date.now(); '>"
            //   "<img id='b' style='display: none' src='/camera' onload='this.style.display=\"initial\"; var a = document.getElementById(\"a\"); a.style.display=\"none\"; a.src=\"camera?\"+Date.now(); '>");
            // client.println();
            break;
          } 
          else 
          {
            currentLine = "";
          }
        } 
        else if (c != '\r') 
        {
          currentLine += c;
        }

        // client.println("HTTP/1.1 200 OK");
        // client.println("Content-type:image/bmp");
        // client.println();
        
        // client.write(bmpHeader, BMP::headerSize);
        // client.write(camera->frame, camera->xres * camera->yres * 2);
        // delay(100);
        
        if (currentLine.endsWith("GET /camera"))
        {
            Serial.println(currentLine);
            client.println("HTTP/1.1 200 OK\r\n");
            delay(10);
            // if (currentLine.endsWith("ack")){
            //   client.println("Content-type:image/bmp");
            //   delay(10);
            // }
            client.println("Content-type:image/bmp\r\n");
            delay(10);
            client.println("Connection: close\r\n");
            delay(10);
            client.println();
            delay(10);
            client.println("donesetup\r\n");
            delay(10);
            
            // client.write(bmpHeader, BMP::headerSize);
            client.write(camera->frame, camera->xres * camera->yres * 2);
            // client.write("<!DOCTYPE html><head><title>Page</title></head><body><h1>Hello world</h1></body></html>");
            delay(10);
            client.write("sent");
            delay(10);
            // client.stop();
        }
      }
      // delay(10);
    }
    // close the connection:
    if (client) {
      client.stop();
      Serial.println("Client Disconnected.");
    }
  }  
}



