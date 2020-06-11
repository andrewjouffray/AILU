

void updateServoAngle()
{
  // the height is used to calculate the angle that the servos need to be at 
  // in order to track the object
  double currentPos = stepperV.currentPosition() - minBottomPosition;
  double height = currentPos * 0.0100878;
  double intHeight = height *-1.0;
  double distanceFromCenter = 356.0; //mm

  double tangent = distanceFromCenter / intHeight;
  double rad = atan(tangent);
  double invDeg =   rad * 180/3.14159265;
  //Serial.println("invDeg " + String(invDeg) + "tan: " + String(tangent));
  double fDeg = 180 - invDeg;
  moveServos(fDeg);

  
}

void moveServos(double servoPosition)
{
  servoLeft.writeMicroseconds(map(servoPosition, 0, 270, 500, 2500));
  servoRight.writeMicroseconds(map(180 - servoPosition, 0, 270, 500, 2500));
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
  // Zero the vertical axis
  Serial.println("Zeroing vertical axis");
  stepperV.moveTo(1000000);
  while(digitalRead(limitSwitchBottom) != HIGH)
  stepperV.run();
    
  stepperV.stop();
  stepperV.runToPosition();
  stepperV.setCurrentPosition(0);
  
}

void alternateLighting()
{
  if(lightCount > alternateCount)
  {
    if(lightState == 0)   // check which light to alternate
    {
      Serial.println("Left off right on");
      digitalWrite(LIGHT_LEFT, RELAY_OFF);
      digitalWrite(LIGHT_RIGHT, RELAY_ON);
      lightState++;
    }
    else
    {
      Serial.println("Left on right off");
      digitalWrite(LIGHT_LEFT, RELAY_ON);
      digitalWrite(LIGHT_RIGHT, RELAY_OFF);
      lightState--;
    }
    lightCount = 0;
  }
}

void alternateLighting2()
{
  if(lightCount > alternateCount)
  {
    switch(lightState)
    {
      case 0:   // both on
        digitalWrite(LIGHT_LEFT, RELAY_ON);
        digitalWrite(LIGHT_RIGHT, RELAY_ON);
        lightState++;
        break;
      case 1: // left on right off
        digitalWrite(LIGHT_LEFT, RELAY_ON);
        digitalWrite(LIGHT_RIGHT, RELAY_OFF);
        lightState++;
        break;
      case 2: // both on
        digitalWrite(LIGHT_LEFT, RELAY_ON);
        digitalWrite(LIGHT_RIGHT, RELAY_ON);
        lightState++;
        break;
      case 3: // left off right on
        digitalWrite(LIGHT_LEFT, RELAY_OFF);
        digitalWrite(LIGHT_RIGHT, RELAY_ON);
        lightState = 0;
        break;
    }
    lightCount = 0;
  }
}

void runLights()
{
  if(toggleLights)
  {
    switch(lighting)
    {
      case 0: // lights off
        digitalWrite(LIGHT_LEFT, RELAY_OFF);
        digitalWrite(LIGHT_RIGHT, RELAY_OFF);
        break;
       case 1: // both lights on
        digitalWrite(LIGHT_LEFT, RELAY_ON);
        digitalWrite(LIGHT_RIGHT, RELAY_ON);
        toggleLights = false;
        break;
       case 2: // alternate between lights
        alternateLighting();
        break;
       case 3: // both on, one off pattern
        alternateLighting2();
        break;
    }
    lightCount++;
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
