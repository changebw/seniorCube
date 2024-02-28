// Load Wi-Fi library
#include <WiFi.h>

// Replace with your network credentials
const char* ssid     = "XXXXX";
const char* password = "XXXXX";

// Set web server port number to 80
WiFiServer server(80);

IPAddress local_IP(192, 168, 1, 215);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);

void setup() {
  Serial.begin(115200);

  Serial.print("Setting AP (Access Point)…");

  WiFi.mode(WIFI_AP);
  Serial.println("set AP mode");
  delay(3000);

  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure");
    delay(1000);
  }

  Serial.println("Set static IP");
  delay(2000);

  WiFi.softAP(ssid, password);

  Serial.print("created AP");
  IPAddress IP = WiFi.softAPIP();

  Serial.print("AP IP address: ");
  delay(5000);
  Serial.println(IP);
  delay(5000);
  
  server.begin();
}

void loop(){
  Serial.println("hello..");
  delay(500);
  WiFiClient client = server.available();
  if (client){
    Serial.println("Got new client");
    String msg = "";

    while (client.connected()){
      while (client.available()) {
        char c = client.read();
        msg += c;
      }
      Serial.println(msg);
    }
    
    Serial.println("Client disconnected");
  }
}