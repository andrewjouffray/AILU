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


void startMotors(double speedH, double speedV, double dir){
  stepper1.setMaxSpeed(speedH);
  stepper1.moveTo(437);

//  stepper2.setMaxSpeed(speedV);
//  stepper2.moveTo(1000000 * dir);
  
}


int loops = 0;
void loop(){
loops ++;
if(Serial.available())  // if data available in serial port
      { 
      
      inByte = Serial.readStringUntil('\n'); // read data until newline
      
      command = inByte.charAt(0); // takes the first character and saves it.

      inByte.remove(0,1); // now remove the letter at the begining, leaving the value.
      
      if(inByte.length() > 6){
        splitInByte = inByte.charAt(3);
        mSpeed2 = splitInByte.toInt();
        mSpeed2 = mSpeed2 * 100;
        inByte.remove(3, 5);
        }
        
      
      int mSpeed = inByte.toInt();// take the value and make it in an int.
      double dSpeed = (double) mSpeed;

      // send the commands 
      if (command == "s"){
        startMotors(500.0, dSpeed, 1.0);
      }else if(command == "w"){
        startMotors(500.0, dSpeed, -1.0);

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

  if (stepper1.distanceToGo() == 0){
      stepper1.moveTo(-stepper1.currentPosition());
  }
    
  if(loops > 5000){    
      digitalWrite(RelayLeft, RELAY_ON);
    }
  if(loops > 10000){
      loops = 0;
      digitalWrite(RelayLeft, RELAY_OFF);
    }

  

  stepper1.run();
  stepper2.run();


  }
