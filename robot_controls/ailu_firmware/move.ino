void updateServoAngle(){
  // the height is used to calculate the angle that the servos need to be at 
  // in order to track the object
  double currentPos = stepperV.currentPosition() - minBottomPosition;
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

void checkRotateLimit()
{
    if (stepperH.currentPosition() == angle)
        Serial.println("stopped: "+String(stepperH.currentPosition()) + " Hlimit: " + String(angle));
        angle = angle * -1;
        stepperH.moveTo(angle);
}

bool limitReached()
{
  // Check if the top or bottom limits have been reached
  long pos = abs(stepperV.currentPosition());
  if(up) // check direction
  {
//    if((digitalRead(limitSwitchTop) == HIGH))
//    {
//      Serial.println("Top limit switch reached");
//      return true;
//    }
//    if((pos >= abs(maxTopPosition)))
//    {
//      Serial.println("Max Top position reached");
//      return true;
//    }
    if((digitalRead(limitSwitchTop) == HIGH) || (pos >= abs(maxTopPosition)))
    {
      Serial.println("Top limit reached");
      return true;
    }
  }
  else if((digitalRead(limitSwitchBottom) == HIGH) || (pos <= minBottomPosition))
  {
    Serial.println("Bottom limit reached");
    return true;
  }
  return false;
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
    if(lighting == 1) // both lights on
    {
      digitalWrite(LIGHT_LEFT, RELAY_ON);
      digitalWrite(LIGHT_RIGHT, RELAY_ON);
      toggleLights = false;
    }
    else if(lighting == 2) // alternate between lights
    {
      lightCount++;
      if(lightCount > 6000)
      {
        if(lightCount > 12000)
        {
          digitalWrite(LIGHT_LEFT, RELAY_OFF);
          digitalWrite(LIGHT_RIGHT, RELAY_ON);
          lightCount = 0;
        }
        else
        {
          digitalWrite(LIGHT_LEFT, RELAY_ON);
          digitalWrite(LIGHT_RIGHT, RELAY_OFF);
        }
      }
      
    }
  }
  
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
