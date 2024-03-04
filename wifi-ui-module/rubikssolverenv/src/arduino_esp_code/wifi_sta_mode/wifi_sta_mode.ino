// Load Wi-Fi library
#include <WiFi.h>

const char* ssid = "XXX";
const char* password = "XXXXX";

// Set web server port number to 80
WiFiServer server(80);

bool messageReceived = false;

void setup() {
  Serial.begin(115200);

  Serial.println("Setting STA mode…");

  WiFi.mode(WIFI_STA);
  Serial.println("done setting STA mode");
  delay(3000);

  WiFi.begin(ssid, password);

  delay(1000);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("connecting..");
  }

  Serial.println("Connected to network.");

  delay(1000);
  Serial.println("Got IP: ");  
  Serial.println(WiFi.localIP());
  delay(1000);
  
  server.begin();
}

void loop(){
  Serial.println("hello..");
  delay(500);
  WiFiClient client = server.available();
  
  if (client){
    Serial.println("Got new client");
    String msg = "";
    bool gotMsg = false;

    while (client.connected()){
      if (client.available()) {
        char c = client.read();
        if (c != '\0'){
          msg += c;
        }
        else {
          gotMsg = true;
          Serial.println(msg);
        }
      }
      if (gotMsg == true){
        msg = "";
        gotMsg = false;
      }
      server.write("hello world");
      delay(500);
    }
    
    Serial.println("Client disconnected");
  }
}