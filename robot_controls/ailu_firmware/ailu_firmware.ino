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

#define LIGHT_LEFT 11
#define LIGHT_RIGHT 12
#define RELAY_ON 1      // Define relay on pin state
#define RELAY_OFF 0     // Define relay off pin state

#define SERVO_PIN_LEFT 9
#define SERVO_PIN_RIGHT A3

// Vertical stepper
AccelStepper stepperH(MOTOR_A_ENABLE_PIN, MOTOR_A_STEP_PIN, MOTOR_A_DIR_PIN); 
const long maxTopPosition = -38407;
long minBottomPosition = 0;
double speedV = 2000.0;
bool startRun = false;
bool up = false;
// limit switches for vertical stepper motor
const int limitSwitchTop = 0;
const int limitSwitchBottom = 7;

// Horizontal stepper (turntable)
AccelStepper stepperV(MOTOR_B_ENABLE_PIN, MOTOR_B_STEP_PIN, MOTOR_B_DIR_PIN); 
const long hZeroPosition = 40000; // default position of stepperH (it can't go into negative positions)
const long oneRotation = 20920; // position to do one full rotation
const double convertionMultiplication = oneRotation / 360; // multiply degrees by this number to get position
bool zeroHAtEnd = false;
long angle = 2000000;
long hLimitMin = 0;
long hLimitMax = 0;
long lastPos = 0;
long Hpos = 0;
double speedH = 1000.0;
bool fullRotate = true;

// Servos
Servo servoLeft;
Servo servoRight;
int tracking = 1;

//lights
long lightCount = 0;
long alternateCount = 6000;
bool toggleLights = true;
int lightState = 0; 
int lighting = 1;

String command;
String param;

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
  eSetTracking,
  eRunD,
  eRunU,
  eMoveH,
  eMoveV,
  eEnd,
  eSetZero,
  eMoveS,
  eReset,
  eZeroV,
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

    servoLeft.attach(SERVO_PIN_LEFT, 500, 2500);
    servoRight.attach(SERVO_PIN_RIGHT, 500, 2500);

    moveServos(95);
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
        if(Hpos == hLimitMax){
          if(lastPos != Hpos){
            stepperH.moveTo(hLimitMin);
            lastPos = Hpos;
          }
        }
        else if(Hpos == hLimitMin){
          if(lastPos != Hpos){
            stepperH.moveTo(hLimitMax);
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
