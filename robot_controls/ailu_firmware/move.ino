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

void rotate()
{
  if(!fullRotate)
  {
    // makes the base plate oscillate between two angles
    if(stepperH.distanceToGo() == 0)
    {
      // positions[STEPPER_H] = -stepperH.currentPosition(); // do we need this instead of just updating the one?
      // steppers.moveTo(positions);
      stepperH.moveTo(-stepperH.currentPosition());
    }
  }
}

bool limitReached()
{
  // Check if the top or bottom limits have been reached
  int pos = stepperV.currentPosition();
  if((digitalRead(limitSwitchTop) == HIGH) || (pos >= maxTopPosition))
  {
    Serial.println("Top limit reached");
    return true;
  }
  else if((digitalRead(limitSwitchBottom) == HIGH) || (pos <= minBottomPosition))
  {
    Serial.println("Bottom limit reached");
    return true;
  }
  return false;
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
