#include <VL53L0X.h>
#include <Wire.h>
#include <Servo.h>
#include <Stepper.h>

VL53L0X lox;

Servo servo;
Stepper stepper(2048, 2, 4, 3, 5);

char user = 0;
char currentMode = '1';

float phi = 0;
float theta = 0;
float precisionDeg = 10;

int stepDirection = 1;

void setup() {
  Wire.begin();
  Serial.begin(9600);

  servo.attach(9);
  stepper.setSpeed(10);

  lox.setTimeout(50);
  lox.init();
  lox.startContinuous();

  servo.write(90);

  Serial.println("READY");
}

// ---- distance ----
int getDistance() {
  int d = lox.readRangeContinuousMillimeters();
  if (lox.timeoutOccurred()) return -1;
  return d;
}

// ---- reset ----
void goHome() {
  phi = 0;
  theta = 0;
  stepDirection = 1;
  servo.write(90);
  stepper.step(0);
}

void loop() {

  if (Serial.available()) {

    user = Serial.read();

    // -------- MODE --------
    if (user == '1' || user == '2' || user == '3') {
      currentMode = user;
      goHome();
    }

    // -------- PRECISION --------
    if (user == 'P') {
      precisionDeg = Serial.parseFloat();   // e.g. P10
    }

    // -------- STEP --------
    if (user == 'S') {

      int stepSize = (2048 * precisionDeg) / 360.0;
      if (stepSize < 1) stepSize = 1;

      int d = getDistance();

      // ---- 1D ----
      if (currentMode == '1') {
        Serial.print("1D,");
        Serial.println(d);
      }

      // ---- 2D ----
      else if (currentMode == '2') {

        stepper.step(stepDirection * stepSize);
        phi += precisionDeg * stepDirection;

        if (phi >= 360 || phi <= 0) {
          stepDirection *= -1;
        }

        Serial.print("2D,");
        Serial.print(phi);
        Serial.print(",");
        Serial.println(d);
      }

      // ---- 3D ----
      else if (currentMode == '3') {

        servo.write(90 - theta);

        Serial.print("3D,");
        Serial.print(90 - theta);
        Serial.print(",");
        Serial.print(phi);
        Serial.print(",");
        Serial.println(d);

        theta += precisionDeg;

        if (theta >= 45) {
          theta = 0;

          stepper.step(stepDirection * stepSize);
          phi += precisionDeg * stepDirection;

          if (phi >= 360 || phi <= 0) {
            stepDirection *= -1;
          }
        }
      }
    }
  }
}
