#include <SoftwareSerial.h>

SoftwareSerial espSerial(2,3);

int testcounter = 0;

#define ssid "XXX"
#define PASSWORD "XXX"

String fmsg;
String msg;
String response;
String cmd;

void setup() {
  espSerial.begin(115200);
  Serial.begin(115200);
  espSetup();
}

void loop() { 
  String msg;
  
  // Receive messages from the client
  while(espSerial.available()){
      fmsg += (char)espSerial.read();
      delay(2);
  }
    
  msg = getString(fmsg);
  
  if (msg == "scramble"){
    Serial.println("GOT MSG:");
    Serial.println(msg);
  }
  else if (msg == "solve"){
    Serial.println("GOT MSG:");
    Serial.println(msg);
  }
  else if (msg == "GET /time\r\n"){
    int connectionId = 0;
    if (espSerial.find("+IPD,")){
      connectionId = espSerial.read()-48;
    }
    String cipSend = "AT+CIPSEND=";
    cipSend += connectionId;
    cipSend += ",";
    testcounter += 1;
    String msg = String(testcounter);
    cipSend += msg.length();
    cipSend += "\r\n";

    sendData(cipSend, 50, true);
    sendData(msg, 50, true);
  }
  else{
    if(msg != NULL){
      Serial.println(msg);
      delay(250);
    }
  }
}

// setup the esp as a server for receiving commands + serial communication to arduino
void espSetup() {
    int counter=0;
    Serial.println("-----------BEGIN ESP SETUP------------");
    
    // Reset ESP8266 to prepare for new connection using RST
    espSerial.println("AT+RST");
    delay(2000);
    getResponse();
    
    // Test AT setup
    Serial.println("-------------TEST AT----------");
    while(1){
       espSerial.println("AT");
       delay(250);
       if(espSerial.find("OK")){
        counter+=1;
        } 
       if(counter == 10){
        Serial.println("Test OK");
        counter=0;
        break;
        }
       else{
        Serial.println("Waiting...");
        }
      }

    // Prepare to establish connection through ssid,pass by setting station mode
    Serial.println("-------------SET STATION MODE----------");
    while(1){
      espSerial.println("AT+CWMODE=1");
      delay(250);
      if(espSerial.find("OK")){
        counter+=1;
        }
      if(counter == 10){
        Serial.println("Station Mode Setted 1");
        counter=0;
        break;
        }
      else{
        Serial.println("Waiting...");
        }
      }
    delay(1000);
    // Connect to Wi-Fi network
    Serial.println("-------------CONNECT TO WIFI----------");
    while(1){
      cmd = "AT+CWJAP=\"";
      cmd += ssid;
      cmd += "\",\"";
      cmd += PASSWORD;
      cmd += "\"";
      espSerial.println(cmd);
      if(espSerial.find("OK")){
        counter+=1;
        }
      if(counter == 3){
        Serial.println("Connection Established");
        counter=0;
        break;
        }
      else{
        Serial.println("Waiting...");
        }
      }
      
    // Set static IP and verify
    Serial.println("-------------SET AND VERIFY IP----------");
    espSerial.println("AT+CIPSTA=\"172.20.10.6\"");
    delay(250);
    getResponse();
    delay(2000);
    espSerial.println("AT+CIFSR");
    delay(250);
    getResponse();

    // Testing multiple connections
    Serial.println("-------------TEST MULTIPLE CONNECTIONS----------");
    while(1){
      espSerial.println("AT+CIPMUX=1");
      delay(250);
      if(espSerial.find("OK")){
        counter+=1;
        }
      if(counter == 10){
        Serial.println("Multiple Connections Enabled");
        counter = 0;
        break;
        }
      else{
        Serial.println("Waiting...");
        }
      }

    // Set arbitrary port 8080
    Serial.println("-------------SET PORT 8080----------");
    while(1){
     espSerial.println("AT+CIPSERVER=1,8080");
     delay(500);
     if(espSerial.find("OK")){
       counter+=1;
       }
     if(counter == 10){
       Serial.println("Setting Port 8080");
       counter = 0;
       break;
       }
     else{
       Serial.println("Waiting...");
       }
     }

    Serial.println("---------SETUP DONE--------");
    delay(250);
}

//get response from esp serial
void getResponse() {
  while(espSerial.available()){
      char c = espSerial.read();
      response += c;
      }
  Serial.println(response);
  response = "";
}

//helper to clean up message from esp serial
String getString(String flmsg) { 
  int lng = 0,delimiter = 0;
  String lmsg;
  lng = flmsg.length();  
  for(int i=0;i<lng;i++){
     if(flmsg[i] == ':'){
      delimiter = i;
      }
     if(i > delimiter && delimiter != 0){
      lmsg += flmsg[i];
      }
    }
  fmsg = ""; 
  return lmsg;
}

String sendData(String command, const int timeout, boolean debug)
{
    String response = "";                                             
    espSerial.print(command);                                          
    long int time = millis();                                      
    while( (time+timeout) > millis())                                 
    {      
      while(espSerial.available())                                      
      {
        char c = espSerial.read();                                     
        response+=c;                                                  
      }  
    }    
    if(debug)                                                        
    {
      Serial.print(response);
    }    
    return response;                                                  
}



