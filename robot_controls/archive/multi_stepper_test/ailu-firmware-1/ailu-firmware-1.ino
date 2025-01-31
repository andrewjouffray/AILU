#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>

#define MOTOR_A_ENABLE_PIN 6
#define MOTOR_A_STEP_PIN 4
#define MOTOR_A_DIR_PIN 5

#define MOTOR_B_ENABLE_PIN 1
#define MOTOR_B_STEP_PIN 3
#define MOTOR_B_DIR_PIN 2

#define RELAY_ON 1      // Define relay on pin state
#define RELAY_OFF 0     // Define relay off pin state

#define SERVO_PIN_LEFT 10
#define SERVO_PIN_RIGHT 11

#define RelayLeft  8

AccelStepper stepper1(1, MOTOR_A_STEP_PIN, MOTOR_A_DIR_PIN);
AccelStepper stepper2(1, MOTOR_B_STEP_PIN, MOTOR_B_DIR_PIN);

Servo servoLeft;
Servo servoRight;

const int limitSwitchTop = 0;
const int limitSwitchBottom = 7;

String inByte;
String splitInByte;
String command;
int pos;
int mSpeed2;
int lastLimSwitch = 1;
double maxTopPosition = -38407;
double minBottomPosition = 0;
double actualMaxTopPosition = -38407;
bool fullRotate = true;

// ============================================SETUP=======================================================

void setup()
{
    stepper1.setAcceleration(500.0); 
    stepper2.setAcceleration(5000.0);
    
    pinMode(limitSwitchTop, INPUT);
    pinMode(limitSwitchBottom, INPUT);

    

    digitalWrite(RelayLeft, RELAY_OFF);
    pinMode(RelayLeft, OUTPUT);
    delay(1000);

    Serial.begin(9600);
    stepper2.setMaxSpeed(300);

    servoLeft.attach(SERVO_PIN_LEFT);
    servoRight.attach(SERVO_PIN_RIGHT);
}

//========================================= HELPER FUNCTIONS ===========================================

// allows the base plate to rotate 
void rotate(double angle){

  if(angle == 360){
      angle = 100000;
    }
   else{
      angle = angle * 9.7;
      fullRotate = false;
    }
  
  stepper1.setMaxSpeed(500.0);
  stepper1.moveTo(angle);
}

// stops the base plate from rotating
void stopRotate(){
    stepper1.setMaxSpeed(1.0);
    stepper1.moveTo(stepper1.currentPosition());
  }

// allows the linear actuator to go up
void goUp(double speedV){
  stepper2.setMaxSpeed(speedV);
  stepper2.moveTo(actualMaxTopPosition);
  
}

// allows the linear actuator to go down
void goDown(double speedV){
  stepper2.setMaxSpeed(speedV);
  stepper2.moveTo(minBottomPosition);
}


void getHeight(){
  double currentPos = stepper2.currentPosition();
  float height = currentPos * 0.0097378;
  Serial.println("Height: " + String(height));
  }


// gets the current height of the linear actuator
void UpdateServoAngle(){
  // the hight is used to calculate the angle that the servos need to be at 
  // in order to track the object
  double currentPos = stepper2.currentPosition() - minBottomPosition;
  float height = currentPos * 0.0097378;
  int intHeight = (int) height;
  int distanceFromCenter = 356; //mm
  float rad = 1/(distanceFromCenter / intHeight);
  float invDeg = rad * (180 / 3.1415);
  float fDeg = 180 - invDeg;
  int degreeToRotate = (int) fDeg;
  int mappedDeg = map(degreeToRotate, 0, 270, 0, 180);
  servoLeft.write(mappedDeg);
  servoRight.write(180 - mappedDeg);
  
}


// pulses the linear actuator, allowing user to move it up or down in real time 
void pulse(bool value){

  digitalWrite(MOTOR_B_DIR_PIN,value); // Enables the motor to move in a particular direction

  digitalWrite(MOTOR_B_STEP_PIN,HIGH); 
  delayMicroseconds(200); 
  digitalWrite(MOTOR_B_STEP_PIN,LOW);
  delayMicroseconds(200);
  
}

// zeroes the linear actuator down to the base 
void zeroX(){
  stepper2.setMaxSpeed(2000.0);
  stepper2.moveTo(1000000);

  while(true){
      if (digitalRead(limitSwitchBottom) == HIGH){
        Serial.println("zero complete");
        stepper2.stop();
        stepper2.setCurrentPosition(0);
        break;

    }
    
  }
}


// ======================================================= MAIN LOOP ==============================================

int loops = 0;
void loop(){
loops ++;
  if(Serial.available()){ //checks if there is data coming from the python script
        
        inByte = Serial.readStringUntil('\n'); // read data until newline

        if(inByte.length() >= 8){

          // parses the data into strings
          String vSpeedByte = inByte;
          String hAngleByte = inByte;
          String trackObjectByte = inByte;
          String lightingByte = inByte;
          String directionByte = inByte;
    
          lightingByte = lightingByte.charAt(7);
          trackObjectByte = trackObjectByte.charAt(6);
          hAngleByte.remove(6,7);
          hAngleByte.remove(0,3);
          vSpeedByte.remove(3,7);
          directionByte = directionByte.charAt(8);
            
          Serial.println(vSpeedByte + "|" + hAngleByte + "|" + trackObjectByte+ "|" + lightingByte);
    
          double vSpeed = vSpeedByte.toInt();
          double hAngle = hAngleByte.toInt();
          double trackObject = trackObjectByte.toInt();
          double lighting = lightingByte.toInt();
          int dir = directionByte.toInt();

        
          rotate(hAngle);

          if(dir == 1){
              goUp(vSpeed);
            }
          else{
              goDown(vSpeed);
            }

        // for one string commands 
        }else{

          // zero x axis to bottom
          if(inByte == "z"){
              zeroX();
            }

          // set the z axis to zero regardless of where he is.

          // TODO: add some sort of method to allow the robot to know it's height even when the user enters a custom zero so that the 
          // robot doesn't ram into the top of the linear actuator.
          else if(inByte == "q"){    
              minBottomPosition = stepper2.currentPosition();
            }
        }

  }


  if (digitalRead(limitSwitchTop) == HIGH){

      if(lastLimSwitch == 2){
        Serial.println("position: "+ String(stepper2.currentPosition()));
        Serial.println("top limit switch reached");
        lastLimSwitch = 1;
      }


  }
  if (digitalRead(limitSwitchBottom) == HIGH){

      if(lastLimSwitch == 1){
        Serial.println("position: " + String(stepper2.currentPosition()));
        Serial.println("bottom limit switch reached");
        stepper2.stop();
        lastLimSwitch = 2;
      }

  }

// use somethings like this to update the servo position from time to time.
//  if(loops > 5000){    
//      digitalWrite(RelayLeft, RELAY_ON);
//    }
//  if(loops > 10000){
//      loops = 0;
//      digitalWrite(RelayLeft, RELAY_OFF);
//    }

  // makes the base plate oscilate between two angles
  if(fullRotate == false){
    if (stepper1.distanceToGo() == 0){
        stepper1.moveTo(-stepper1.currentPosition());
    }  
  }

  stepper1.run();
  stepper2.run();


  }
