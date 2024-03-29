#include <TM1637Display.h>

// Pins for TM1637 display module
#define CLK_PIN 5
#define DIO_PIN 6

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


    while (digitalRead(left) == LOW || digitalRead(right) == LOW) {
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

    String secondString = "";

    if (seconds < 10) {
      secondString = "0" + String(seconds);
    }
    else {
      secondString = String(seconds);
    }

    // Serial.println(minutes);
    Serial.println(String(minutes) + ":" + secondString + "." + String(milliseconds));

    // Update the display to show elapsed time in MM:SS.ss format
    int displayValue = minutes * 100 + seconds;
    int hundredths = milliseconds / 10;

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