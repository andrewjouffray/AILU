#include<Servo.h>
int servoPin = 9;
int Index;
String inByte;
String command;
int pos;
int first = 0;
Servo Servo1;

void setup(){

  // servo is attached to pin 9, you can use a different pin on your arduino, but remeber to update the code if you do
  // The yellow cable is the one to get attached to that pin
  Servo1.attach(servoPin);


  // stepper motor 1 has 3 oins to control it:
  pinMode(10, OUTPUT); //Enable (enables the motor when set to LOW)
  pinMode(5, OUTPUT); //Step (this is set to high and low in regular intervals to actually move the stepper motor )
  pinMode(4, OUTPUT); //Direction (seting tis to high or low will change the direction of the stepper)


  // Stepper motor 2
  pinMode(8, OUTPUT); //Enable
  pinMode(7, OUTPUT); //Direction
  pinMode(2, OUTPUT); //Step


  // those two are the limit switches, 
  pinMode(6, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);


  // enables the two stepper motors
  digitalWrite(10,LOW);
  digitalWrite(8,LOW);

  // this opens the connection with the PC, notice the baud-rate (9600) needs to be the same in the python code.
  Serial.begin(9600);
}


// zero the vertical axis 
void zeroZ(){
  bool done = LOW;
  while (done == LOW){
   if (digitalRead(6) == LOW){ // limit switch is open
        digitalWrite(4,HIGH);
        
          digitalWrite(5,HIGH);
          // this deplay defines the speed that the motor will run at, the longer the delay, 
          // the slower the motor (fastest would be about 300 milliseconds)
          delayMicroseconds(1000);
          digitalWrite(5,LOW);
          delayMicroseconds(1000);

    // this is what happens when the limit switch is closed 
    }else{
      Serial.println("it was high");
      done = HIGH;
    }

    }
    
    }

   
void zeroX(){
  bool done = LOW;
  while (done == LOW){
   if (digitalRead(11) == LOW){ // limit switch is open
        digitalWrite(7,HIGH);
        
          digitalWrite(2,HIGH);
          delayMicroseconds(2000);
          digitalWrite(2,LOW);
          delayMicroseconds(2000);
      
    }else{
      Serial.println("it was high");
      done = HIGH;
    }

    }
}


// moves the vertical stepper up or down depending on the direction
void stepper(int steps, bool zDirection){
      for (int j = 0; j <= steps; j++) {
      
      for (int i = 0; i <= 79; i++) {
    
        digitalWrite(4,zDirection);
        
          digitalWrite(5,HIGH);
          delayMicroseconds(500);
          digitalWrite(5,LOW);
          delayMicroseconds(500);
          
        
        }
     }
}



void stepper2(int steps, bool xDirection){


      for (int j = 0; j <= steps; j++) { // then takes all the nessesary steps in the desired direction at full speed
        // notice that this technique of accelerating slowly the mototr is not great because you need to at least make 6 steps.
      
      for (int i = 0; i <= 25; i++) {
    
        digitalWrite(7,xDirection);
        
          digitalWrite(2,HIGH);
          delayMicroseconds(500);
          digitalWrite(2,LOW);
          delayMicroseconds(500);
          
        
        }
     }

//     delay(2000);
}


// this will simply move the servo to a new angle
void servoPos(int angle){

    int val1 = map(angle,0,270,0,180);
    Servo1.write(val1);
    delay(2000);
  
  }

void loop()
{    
  stepper2(0, LOW);
  if(Serial.available())  // if data available in serial port
    { 
    inByte = Serial.readStringUntil('\n'); // read data until newline
    command = inByte.charAt(0); // takes the first character and saves it.
    Serial.println(inByte);
    Serial.println(command);
    inByte.remove(0,1); // now remove the letter at the begining, leaving the value.
    pos = inByte.toInt();// take the value and make it in an int.
    Serial.println(inByte);
    // send the commands 
    if (command == "w"){
      stepper(pos, LOW);
    }else if (command == "s"){
      stepper(pos, HIGH);
    }else if (command == "o"){
      servoPos(pos);
    }else if (command == "a"){
      stepper2(pos, LOW);
    }
    else if (command == "d"){
      stepper2(pos, HIGH);
    }
    else if (command == "t"){
      Serial.println("ok");
      zeroX();
    }
    else if (command == "g"){
      zeroZ();
    }
    }
}
