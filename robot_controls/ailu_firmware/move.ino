

void updateServoAngle(){
 
  // the height is used to calculate the angle that the servos need to be at 
  // in order to track the object
  double currentPos = stepperV.currentPosition() - minBottomPosition;
  double height = currentPos * 0.0100878;
  double intHeight = height *-1.0;
  double distanceFromCenter = 356.0; //mm

  double tangeant = distanceFromCenter / intHeight;
  double rad = atan(tangeant);
  double invDeg =  round( atan(tangeant) * 180/3.14159265 );
//  Serial.println("invDeg " + String(invDeg) + "tan: " + String(tangeant));
  double fDeg = 180 - invDeg;
  int degreeToRotate = (int) fDeg;
  moveServos(degreeToRotate);

  
}

void moveServos(int servoPosition){
//   Serial.println("updating servo position to " + String(servoPosition));

  int mappedDeg = map(angle, 0, 270, 500, 2500);
  servoLeft.writeMicroseconds(map(angle, 0, 270, 500, 2500));
  servoRight.writeMicroseconds(map(180 - angle, 0, 270, 500, 2500));
  
  //servoLeft.writeMicroseconds(mappedDeg);
  //servoRight.writeMicrosecondste(180 - mappedDeg);
  }
  
void checkRotateLimit()
{
    if (stepperH.currentPosition() == angle)
        angle = angle * -1;
        stepperH.moveTo(angle);
}

bool limitReached()
{
  // Check if the top or bottom limits have been reached
  long pos = abs(stepperV.currentPosition());

  switch(up){
    case(true):
      if((digitalRead(limitSwitchTop) == HIGH) || (pos >= abs(maxTopPosition)))
      {
        return true;
      }
      return false;
      break;
    case(false):
      if((digitalRead(limitSwitchBottom) == HIGH) || (pos <= minBottomPosition))
      {
        return true;
      }
      return false;
      break;
    
    }

  
}

void zeroV()
{
  Serial.println("ZeroV");
  // Zero the vertical axis
  Serial.println("Zeroing vertical axis");
  stepperV.moveTo(1000000);
  while(digitalRead(limitSwitchBottom) != HIGH)
  stepperV.run();
    
  stepperV.stop();
  stepperV.runToPosition();
  stepperV.setCurrentPosition(0);
  
}

void runLights()
{
  if(toggleLights)
  {
//    switch(lighting)
//    {
//      case 0: // lights off
//        digitalWrite(LIGHT_LEFT, RELAY_OFF);
//        digitalWrite(LIGHT_RIGHT, RELAY_OFF);
//        break;
//       case 1: // both lights on
//        digitalWrite(LIGHT_LEFT, RELAY_ON);
//        digitalWrite(LIGHT_RIGHT, RELAY_ON);
//        toggleLights = false;
//        break;
//       case 2: // alternate between lights
//        alternateLighting();
//        break;
//       case 3: // both on, one off pattern
//        
//        break;
//    }
    lightCount++;
    if (lighting == 0)
    {
      digitalWrite(LIGHT_LEFT, RELAY_OFF);
      digitalWrite(LIGHT_RIGHT, RELAY_OFF);
      toggleLights = false;
    }
    else if(lighting == 1) // both lights on
    {
      digitalWrite(LIGHT_LEFT, RELAY_ON);
      digitalWrite(LIGHT_RIGHT, RELAY_ON);
      toggleLights = false;
    }
    else if(lighting == 2) // alternate between lights
    {
      if(lightCount > alternateCount)
      {
        if(lightsOn == 1)   // check which light to alternate
        {
          digitalWrite(LIGHT_LEFT, RELAY_OFF);
          digitalWrite(LIGHT_RIGHT, RELAY_ON);
        }
        else
        {
          digitalWrite(LIGHT_LEFT, RELAY_OFF);
          digitalWrite(LIGHT_RIGHT, RELAY_ON);
        }
        lightCount = 0;
        leftLight = !leftLight;
      }
    }
    else if(lighting == 3)
    {
//      if(lightCount > alternateCount)
//      {
//        if(ligh == 1 || lastLighting == 2)
//        {
//          digitalWrite(LIGHT_LEFT, RELAY_ON);
//          digitalWrite(LIGHT_RIGHT, RELAY_ON);
//        }
//        else if(lastLighting == 
//        if(lightsOn == 1)
//        if(lightCount > 2*alternateCount) // 
//        {
//          digitalWrite(LIGHT_LEFT, RELAY_ON);
//          digitalWrite(LIGHT_RIGHT, RELAY_ON);
//          lightCount = 0;
//        }
//        else if(leftLight)
//        {
//          digitalWrite(LIGHT_LEFT, RELAY_OFF);
//          digitalWrite(LIGHT_RIGHT, RELAY_ON);
//          leftLight = !leftLight;
//        }
//        else
//        {
//          digitalWrite(LIGHT_LEFT, RELAY_ON);
//          digitalWrite(LIGHT_RIGHT, RELAY_OFF);
//          leftLight = !leftLight;
//        }
//      }
    }
  }
  
}

void flush(){

  Serial.flush();
}

/************** OLD FUNCTIONS ************
void getHeight(){
  double currentPos = stepperV.currentPosition();
  float height = currentPos * 0.0097378;
  Serial.println("Height: " + String(height));
  }

  // stops the base plate from rotating
void stopRotate(){
    stepperH.setMaxSpeed(1.0);
    stepperH.moveTo(stepperH.currentPosition());
  }

  // allows the base plate to rotate 
void rotate(double angle){

  if(angle == 360){
      angle = 100000;
    }
   else{
      angle = angle * 9.7;
      //fullRotate = false;
    }
  
  stepperH.setMaxSpeed(1000.0);
  stepperH.moveTo(angle);
}

******************************************/
