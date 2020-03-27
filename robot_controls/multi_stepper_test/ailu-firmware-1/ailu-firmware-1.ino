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

bool fullRotate = true;



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

// allows the base plate to rotate 
void rotate(int angle){

  if(angle == 360){
      angle = 100000;
    }
   else{
      angle = angle * 9.7
    }
  
  stepper1.setMaxSpeed(500.0);
  stepper1.moveTo(angle);
}

// stops the base plate from rotating
void stop rotate(){
    stepper1.setMaxSpeed(1.0);
    stepper1.moveTo(stepper1.currentPosition());
  }

// allows the linear actuator to go up
void goUp(double speedV){
  stepper2.setMaxSpeed(speedV);
  stepper2.moveTo(-38407);
  
}

// allows the linear actuator to go down
void goDown(double speedV){
  stepper2.setMaxSpeed(speedV);
  stepper2.moveTo(0);
}


// gets the current height of the linear actuator
void getCurrentHeight(){

  double currentPos = stepper2.currentPosition();
  float height = currentPos * 0.0097378;
  Serial.println(height);
  
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

int loops = 0;
void loop(){
loops ++;
  if(Serial.available()){ //checks if there is data coming from the python script
        
        inByte = Serial.readStringUntil('\n'); // read data until newline

        // parses the data into strings
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

  if(loops > 5000){    
      digitalWrite(RelayLeft, RELAY_ON);
    }
  if(loops > 10000){
      loops = 0;
      digitalWrite(RelayLeft, RELAY_OFF);
    }

  // makes the base plate oscilate between two angles
  if(fullRotate == false){
    if (stepper1.distanceToGo() == 0){
        stepper1.moveTo(-stepper1.currentPosition());
    }  
  }

  stepper1.run();
  stepper2.run();


  }
