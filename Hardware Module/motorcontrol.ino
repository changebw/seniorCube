// defines pins numbers
const int stepPin = 0;
const int dirPin = 3;

void setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop() {
  // Turn 180 degrees
  digitalWrite(dirPin, HIGH); // Enables the motor to move in a particular direction
  // Makes 100 pulses for making one half cycle rotation (adjust as needed)
  for (int x = 0; x < 100; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }
  delay(5000); // 5-second delay

  // Turn 90 degrees
  digitalWrite(dirPin, LOW); // Changes the rotation direction
  // Makes 50 pulses for making quarter-cycle rotation (adjust as needed)
  for (int x = 0; x < 50; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }
  delay(5000); // 5-second delay
}
