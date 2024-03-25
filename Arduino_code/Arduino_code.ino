#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Servo-specific settings
#define NUM_SERVOS 8
#define SERVO_MIN_PULSE 102 // Minimum pulse length for one extreme position
#define SERVO_MAX_PULSE 1024 // Maximum pulse length for the other extreme position

// Midpoint between min and max pulse lengths for return to original position
#define SERVO_MID_PULSE ((SERVO_MIN_PULSE + SERVO_MAX_PULSE) / 2)

// Function declaration
void moveServo(uint8_t servoIndex, uint16_t pulse);
void moveAllServosToMidPosition();
void moveServosByCommand(const String& command);

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pwm.begin();
  pwm.setPWMFreq(60);  // Set the PWM frequency to 60 Hz

  // Move all servos to the midpoint position at the beginning
  moveAllServosToMidPosition();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readString(); // Read the string from the serial monitor

    // Trim unwanted characters (e.g., line endings)
    command.trim();

    // Move the servos based on the received command
    moveServosByCommand(command);

    // Move all servos back to the midpoint position after each move
    moveAllServosToMidPosition();

    delay(1000); // Delay for stability
  }
}

// Function definition to move a specific servo to a position
void moveServo(uint8_t servoIndex, uint16_t pulse) {
  if (servoIndex < NUM_SERVOS) {
    pwm.setPWM(servoIndex, 0, pulse);
  }
}

// Function to move all servos to the midpoint position
void moveAllServosToMidPosition() {
  for (uint8_t i = 0; i < NUM_SERVOS; ++i) {
    moveServo(i, SERVO_MID_PULSE);
  }
}

void moveServosByCommand(const String& command) {
  if (command.equals("كام")) {
    moveServo(0, SERVO_MIN_PULSE);
    moveServo(1, SERVO_MIN_PULSE);
    moveServo(2, SERVO_MIN_PULSE);
    moveServo(3, SERVO_MIN_PULSE);
    moveServo(7, SERVO_MIN_PULSE);
    delay(5000); // Delay for stability
    moveServo(0, SERVO_MID_PULSE);
    moveServo(1, SERVO_MID_PULSE);
    moveServo(2, SERVO_MID_PULSE);
    moveServo(3, SERVO_MID_PULSE);
    moveServo(7, SERVO_MID_PULSE);
  } else if (command.equals("كيف حالك")) {
    moveServo(0, SERVO_MID_PULSE);
    moveServo(1, SERVO_MIN_PULSE);
    moveServo(2, SERVO_MIN_PULSE);
    moveServo(3, SERVO_MIN_PULSE);
    moveServo(7, SERVO_MIN_PULSE);
    delay(5000); // Delay for stability
    moveServo(0, SERVO_MID_PULSE);
    moveServo(1, SERVO_MID_PULSE);
    moveServo(2, SERVO_MID_PULSE);
    moveServo(3, SERVO_MID_PULSE);
    moveServo(7, SERVO_MID_PULSE);
  } else if (command.equals("فين")) {
    moveServo(0, SERVO_MIN_PULSE);
    moveServo(1, SERVO_MIN_PULSE);
    moveServo(2, SERVO_MID_PULSE);
    moveServo(3, SERVO_MID_PULSE);
    moveServo(7, SERVO_MID_PULSE);
    delay(5000); // Delay for stability
    moveServo(0, SERVO_MID_PULSE);
    moveServo(1, SERVO_MID_PULSE);
    moveServo(2, SERVO_MID_PULSE);
    moveServo(3, SERVO_MID_PULSE);
    moveServo(7, SERVO_MID_PULSE);
  } else if (command.equals("مين")) {
    moveServo(0, SERVO_MIN_PULSE);
    moveServo(1, SERVO_MID_PULSE);
    moveServo(2, SERVO_MID_PULSE);
    moveServo(3, SERVO_MIN_PULSE);
    moveServo(7, SERVO_MIN_PULSE);
    delay(5000); // Delay for stability
    moveServo(0, SERVO_MID_PULSE);
    moveServo(1, SERVO_MID_PULSE);
    moveServo(2, SERVO_MID_PULSE);
    moveServo(3, SERVO_MID_PULSE);
    moveServo(7, SERVO_MID_PULSE);
  } else if (command.equals("شركه")) {
    moveServo(0, SERVO_MIN_PULSE);
    moveServo(1, SERVO_MID_PULSE);
    moveServo(2, SERVO_MID_PULSE);
    moveServo(3, SERVO_MID_PULSE);
    moveServo(7, SERVO_MID_PULSE);
    delay(5000); // Delay for stability
    moveServo(0, SERVO_MID_PULSE);
    moveServo(1, SERVO_MID_PULSE);
    moveServo(2, SERVO_MID_PULSE);
    moveServo(3, SERVO_MID_PULSE);
    moveServo(7, SERVO_MID_PULSE);
  } else {
    Serial.println("Invalid Command");
  }
}