#include <LiquidCrystal_I2C.h>

//create integers to represent pins for the left and right hand sensor
const int left=0;
const int right=1;
unsigned long starttime = 0;
unsigned long elapsedtime = 0;
bool timing = false;

//LCD display
LiquidCrystal_I2C lcd(0x27,16,2);

//setup

void setup() {

  //Left hand sensor
  pinMode(left, INPUT_PULLUP);

  //Right hand sensor
  //pinMode(right, INPUT_PULLUP);

  Serial.begin(9600);

  //Welcome message
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("PLACE YOUR HANDS ON");
  lcd.setCursor(0,1);
  lcd.print("THE BUTTONS TO START");
}

void loop() {

  if (!timing && (digitalRead(left) == LOW /*|| digitalRead(right) == LOW*/)) {
      lcd.clear();
      lcd.print("REMOVE YOUR HANDS");
      lcd.setCursor(0, 1);
      lcd.print("TO START TIMER");

      while (digitalRead(left) == LOW/* || digitalRead(right) == LOW*/) {
        // Wait for hands to be removed
        delay(100);
      }

      lcd.clear();

      starttime = millis();
      timing = true;
  }

    if (timing) {

      lcd.clear();
      
     elapsedtime = millis() - starttime;

    int seconds = elapsedtime / 1000;
    int milliseconds = (elapsedtime % 1000) / 10;

    lcd.clear();
    lcd.print("Time: ");
    lcd.setCursor(0,1);
    lcd.print(seconds);
    lcd.print(".");
    if (milliseconds < 10) {
      lcd.print("0");
    }
    lcd.print(milliseconds);

    delay(50);

    // Check if hands are back on the buttons to stop the timer
    if (digitalRead(left) == LOW /*|| digitalRead(right) == LOW*/) {

      while (digitalRead(left) == LOW /*|| digitalRead(right) == LOW*/) {
        // Wait for hands to be back
        delay(100);
      }
      timing = false;

      lcd.clear();
      lcd.print("Final Time: ");
      lcd.setCursor(0, 1);
      lcd.print(seconds);
      lcd.print(".");
      if (milliseconds < 10) {
        lcd.print("0");
      }
      lcd.print(milliseconds);
      lcd.print("s");
    }
  }
}
