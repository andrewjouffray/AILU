#include <AccelStepper.h>
//#include <MultiStepper.h>
#include <Servo.h>
#include <math.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define MOTOR_A_ENABLE_PIN 6
#define MOTOR_A_STEP_PIN 5
#define MOTOR_A_DIR_PIN 8

#define MOTOR_B_ENABLE_PIN 1
#define MOTOR_B_STEP_PIN 3
#define MOTOR_B_DIR_PIN 2

#define RELAY_ON 1      // Define relay on pin state
#define RELAY_OFF 0     // Define relay off pin state

#define SERVO_PIN_LEFT 9
#define SERVO_PIN_RIGHT 10
#define LIGHT_LEFT 11
#define LIGHT_RIGHT 12

#define STEPPER_H 0
#define STEPPER_V 1

#define RelayLeft  8

//MultiStepper steppers;

AccelStepper stepperH(MOTOR_A_ENABLE_PIN, MOTOR_A_STEP_PIN, MOTOR_A_DIR_PIN); // Turntable motor
AccelStepper stepperV(MOTOR_B_ENABLE_PIN, MOTOR_B_STEP_PIN, MOTOR_B_DIR_PIN); // Vertical motor

Servo servoLeft;
Servo servoRight;

// limit switches for vertical stepper motor
const int limitSwitchTop = 0;
const int limitSwitchBottom = 7;

const long hZeroPosition = 40000; // default position of stepperH (it can't go into negative positions)
const long oneRotation = 20920; // position to do one full rotation
const double convertionMultiplication = oneRotation / 360; // multiply degrees by this number to get position

String command;
String param;
long angle = 2000000;
long hLimitMin = 0;
long hLimitPlus = 0;

long maxTopPosition = -38407;
int minBottomPosition = 0;
long lightCount = 0;
bool toggleLights = true;
int lighting = 1;
double speedV = 2000.0;
double speedH = 1000.0;
int tracking = 1;
long positions[2] = {100000, 0};
bool startRun = false;
bool fullRotate = true;
bool up = false;
bool down = false;
bool zeroHAtEnd = false;
long lastPos = 0;
long Hpos = 0;

// Commands enum
enum cmd {
  eQ,
  eSettings,
  eGetP,
  eSetLighting,
  eSetVLimit,
  eSetHLimit,
  eSetVSpeed,
  eSetHSpeed,
  eSetMotor,
  eSetTracking,
  eRunD,
  eRunU,
  eMoveH,
  eMoveV,
  eEnd,
  eSetZero,
  eServo,
  eReset,
  eUnknown  
};

// function prototypes
void handleSerial();
void updateServoAngle();
void rotate();
bool limitReached();
void endRun();
void runLights();

void setup()
{
    pinMode(limitSwitchTop, INPUT);
    pinMode(limitSwitchBottom, INPUT);

    pinMode(LIGHT_LEFT, OUTPUT);
    pinMode(LIGHT_RIGHT, OUTPUT);
    digitalWrite(LIGHT_LEFT, RELAY_OFF);
    digitalWrite(LIGHT_RIGHT, RELAY_OFF);
    
    delay(1000);

    Serial.begin(9600);

    stepperH.setAcceleration(2000.0); 
    stepperV.setAcceleration(5000.0);
    stepperH.setMaxSpeed(speedH);
    stepperV.setMaxSpeed(speedV);
    stepperH.setCurrentPosition(hZeroPosition);

    servoLeft.attach(SERVO_PIN_LEFT);
    servoRight.attach(SERVO_PIN_RIGHT);

    moveServos(95);

    Serial.println("setting up AILU");
    zeroV();
    Serial.println("AILU Robot 0001 Ready");
}

int countToServoUpdate = 0;
void loop()
{
  
  if(Serial.available()) //checks if there is data coming from the python script
  { 
    handleSerial();
  }

  if(startRun)
  
  { 
    runLights();
    countToServoUpdate++;
    if(countToServoUpdate > 500)  // update camera servo every once in a while
    {
      if(tracking)
      {
        countToServoUpdate = 0;
        updateServoAngle();
        
      }
      
    }

    if(!fullRotate)
      {
        Hpos = stepperH.currentPosition();
            if(Hpos == hLimitPlus){
              if(lastPos != Hpos){
               stepperH.moveTo(hLimitMin);
               lastPos = Hpos;
              }
            }

            if(Hpos == hLimitMin){
              if(lastPos != Hpos){
                stepperH.moveTo(hLimitPlus);
                lastPos = Hpos;
            }
          }
        }

    stepperV.run();
    stepperH.run();

    if(limitReached())
    {
      endRun();
    }

  }
}
