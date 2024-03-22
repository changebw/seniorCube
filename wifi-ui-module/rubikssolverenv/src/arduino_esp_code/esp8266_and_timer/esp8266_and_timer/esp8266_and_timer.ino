#include <TM1637Display.h>
#include <SoftwareSerial.h>

SoftwareSerial espSerial(5,6);

// Pins for TM1637 display module
#define CLK_PIN 2
#define DIO_PIN 3

// SSID AND PASS FOR WIFI
#define ssid "XXX"
#define PASSWORD "XXX"

String fmsg;
String msg;
String response;
String cmd;

TM1637Display display(CLK_PIN, DIO_PIN);

//create integers to represent pins for the left and right hand sensor
const int left = 7;
const int right = 8;
unsigned long starttime = 0;
unsigned long elapsedtime = 0;
bool timing = false;

void setup() {
  //Left hand sensor
  pinMode(left, INPUT_PULLUP);

  //Right hand sensor
  pinMode(right, INPUT_PULLUP);

  Serial.begin(9600);
  espSerial.begin(115200);
  espSetup();

  //Welcome message
  display.setBrightness(7); // Set the brightness of the display (0-7)
  display.clear(); // Clear the display
  display.showNumberDecEx(0, 0b01000000, true); // Display "00:00"

  Serial.println("PLACE HANDS ON BUTTONS TO START");
}

void loop() {
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
  }

  if (timing) {
    elapsedtime = millis() - starttime;

    int milliseconds = elapsedtime % 1000;
    int seconds = (elapsedtime / 1000) % 60;
    int minutes = (elapsedtime / 1000) / 60;

    // Update the display to show elapsed time in MM:SS.ss format
    int displayValue = minutes * 100 + seconds;
    int hundredths = milliseconds / 10;

    float sendValue = displayValue * 100 + hundredths;

    if (espSerial.available()){
      if (espSerial.find("+IPD,")){
        delay(1000);
        int connectionId = espSerial.read()-48;
        String val = String(sendValue);
        String cipSend = "AT+CIPSEND=";
        cipSend += connectionId;
        cipSend += ",";
        cipSend += sizeof(val);
        cipSend += "\r\n";

        sendData(cipSend,1000,true);
        sendData(val,1000,true);

      }
    }


    display.showNumberDecEx(displayValue * 100 + hundredths, 0b01000000, true); // Display elapsed time with hundredths of a second

    // Check if hands are back on the buttons to stop the timer
    if (digitalRead(left) == LOW && digitalRead(right) == LOW) {
      while (digitalRead(left) == LOW || digitalRead(right) == LOW) {
        // Wait for hands to be back
        delay(100);
      }
      timing = false;

      display.showNumberDecEx(displayValue * 100 + hundredths, 0b01000000, true); // Display final time with hundredths of a second
      delay(3000); // Wait for 4 seconds
      // Reset the display to zero
      display.showNumberDecEx(0, 0b01000000, true);
    }
  }
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

void getResponse() {
  while(espSerial.available()){
      char c = espSerial.read();
      response += c;
      }
  Serial.println(response);
  response = "";
}

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

