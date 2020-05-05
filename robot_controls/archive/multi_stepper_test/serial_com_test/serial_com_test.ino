#include <AccelStepper.h>
#include <MultiStepper.h>

#define MOTOR_A_ENABLE_PIN 6
#define MOTOR_A_STEP_PIN 4
#define MOTOR_A_DIR_PIN 5

#define MOTOR_B_ENABLE_PIN 1
#define MOTOR_B_STEP_PIN 3
#define MOTOR_B_DIR_PIN 2

#define RELAY_ON 1      // Define relay on pin state
#define RELAY_OFF 0     // Define relay off pin state

#define RelayLeft  8

AccelStepper stepper1(1, MOTOR_A_STEP_PIN, MOTOR_A_DIR_PIN);
AccelStepper stepper2(1, MOTOR_B_STEP_PIN, MOTOR_B_DIR_PIN);

const int limitSwitchTop = 0;
const int limitSwitchBottom = 7;

String inByte;
String splitInByte;
String command;
int pos;
int mSpeed2;
int lastLimSwitch = 1;



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
//    stepper2.moveTo(-10000.0);
}




void loop(){

  
  if(Serial.available())  // if data available in serial port
        { 
        
        inByte = Serial.readStringUntil('\n'); // read data until newline


        String vSpeedByte = inByte;
        String hAngleByte = inByte;
        String trackObjectByte = inByte;
        String lighting = inByte;

        lighting = lighting.charAt(7);
        trackObjectByte = trackObjectByte.charAt(6);
        hAngleByte.remove(6,7);
        hAngleByte.remove(0,3);
        vSpeedByte.remove(3,7);
          
        Serial.println(vSpeedByte + "|" + hAngleByte + "|" + trackObjectByte+ "|" + lighting);
          
       
  
    }


  }
