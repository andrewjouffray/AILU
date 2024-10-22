/********************************* COMMANDS *************************************
*
*  ? Return available commands
*  . Return current settings
*  getP
*   Return current motor position
*  setVLimit [<position>]
*   sets bottom limit, default 0 (0, -38407)
*  setHLimit [<position>]
*   sets rotation limit, default 0 (0, 3492)
*  setSpeed [<h | v> <speed>]
*   set speed of stepper motors,
*   h: [300-2000], default
*  setTracking <0 | 1>
*   toggles camera servo to track object
*  runD
*   runs both motors down with the current settings
*  runU
*   runs both motors up with current settings
*  moveH <position>
*   move to a relative position (0, 3492)
*  moveV <position>
*   move to a vertical position (0,-38407)
*  end
*   stops both motors
*  setLighting <0 | 1 | 2 | 3>
*   0 - both off
*   1 - both on
*   2 - alternate between the two
*   3 - both on, left off right on, both on, right off left on
********************************************************************************/

void printCommands() 
{
  /*
    String commands = R"(? Return available commands
    . Return current settings
    @ Return current motor position
    setVLimit <position>
    sets bottom limit, default 0 (0, -38407)
    setHLimit <position>
    sets rotation limit, default 0 (0, 3492)
    setSpeed [<h | v> <speed>]
    set speed of stepper motors,
    h: [300-2000], default
    setMotor <h | v> <0 | 1>
    toggles motor on or off
    setTracking <0 | 1>
    toggles camera servo to track object
    runD
    runs both motors up with the current settings
    runU
    runs both motors up with current settings
    moveH <position>
    move to a relative position (0, 3492)
    moveV <position>
    move to a vertical position (0,-38407)
    end
    stops both motors)";

    Serial.println(commands);
  */
}

void resetGlobals()
{
  
}

void getPosition()
{
  Serial.readStringUntil('\n'); // flush the buffer
//  Serial.print("Current position: ");
  Serial.println(stepperV.currentPosition());
//  return stepperV.currentPosition();

flush();
}


// TODO: finish this
void printSettings() 
{
//  getPosition();
  Serial.readStringUntil('\n'); // flush the buffer
  Serial.println("Settings");

  flush();
}



void setLighting()
{
  Serial.println("Lighting set");
  param = Serial.readStringUntil('\n');
  lighting = param.toInt();

  flush();
}

void setZero()
{
  // Serial.readStringUntil('\n');
  stepperV.setCurrentPosition(0);

  flush();
}

void reset()
{
  // reset speed and limits
  // Serial.readStringUntil('\n');
  endRun();

  // Reset all default values
  // zeroHAtEnd = false;
  angle = 2000000;
  // hLimitMin = 0;
  // hLimitMax = 0;
  // lastPos = 0;
  // Hpos = 0;
  speedH = 1000.0;
  fullRotate = true;
  speedH = 1000.0;

  //lights
  lightCount = 0;
  alternateCount = 6000;
  toggleLights = true;
  lightState = 0; 
  lighting = 1;

  // Vertical stepper
  minBottomPosition = 0;
  speedV = 2000.0;
  startRun = false;
  up = false;
  speedV = 2000.0;

  tracking = 1;
  startRun = false;
  stepperH.setMaxSpeed(speedH);
  stepperV.setMaxSpeed(speedV);
  zeroV();

  flush();
}

void setVLimit()
{
  param = Serial.readStringUntil('\n');
  int vLimit = param.toInt();
  if (vLimit >= 0)
  {
    minBottomPosition = vLimit;
    Serial.println("vertical limit set");
  }
  else
  {
    Serial.println("Error: Invalid vertical limit");
  }

  flush();
}

void setHLimit()
{
  param = Serial.readStringUntil('\n');
  long hLimit = param.toInt();
  hLimitMax = hZeroPosition + hLimit * convertionMultiplication; // converts degrees to motor position
  hLimitMin = hZeroPosition - hLimit * convertionMultiplication;
  if (hLimitMax >= hZeroPosition + oneRotation)
  {
    angle = hZeroPosition + 10000000;	// Set horizontal motor to rotate without stopping
    fullRotate = true;
    Serial.println("horizontal limit set to infinity");
  }
  else
  {
    angle = hLimit;
    fullRotate = false;
    Serial.println("horizontal limit set");
  }
  flush();
}

void moveS(){
  param = Serial.readStringUntil('\n');
  long pos = param.toInt();
  Serial.println("moving servos");
  moveServos(pos);
  flush();
}

void setVSpeed()
{
  param = Serial.readStringUntil('\n');
  long speed = param.toInt();
  alternateCount = 12000000/speed;
  Serial.println("vert speed set");
  stepperV.setMaxSpeed(speed);
  flush();
}

void setHSpeed()
{
  param = Serial.readStringUntil('\n');
  long speed = param.toInt();
  Serial.println("horizontal speed set");
  stepperH.setMaxSpeed(speed);
  flush();
}

void setTracking()
{
  param = Serial.readStringUntil('\n');
  Serial.println("tracking set");
  tracking = param.toInt();
  flush();
}

void runD()
{
  zeroHAtEnd = true;
  Serial.println("runD");
  stepperH.moveTo(angle);
  stepperV.moveTo(minBottomPosition);
  up = false;
  startRun = true;
  flush();
}

void runU()
{
  zeroHAtEnd = true;
  Serial.println("runU");
  stepperH.moveTo(angle);
  stepperV.moveTo(maxTopPosition);
  up = true;
  startRun = true;
  flush();
}

void moveH()
{
  fullRotate = true;
  Serial.println("moveH");
  param = Serial.readStringUntil(' ');	// get speed
  int speed = param.toInt();
  stepperH.setMaxSpeed(speed);
  param = Serial.readStringUntil('\n');	// get position
  long dest = param.toInt();
  dest =  hZeroPosition + dest * convertionMultiplication; // converts from degrees to motor position
  stepperH.moveTo(dest);
  startRun = true;
  flush();
}

void moveV()
{
  
  param = Serial.readStringUntil(' ');	// get speed
  int speed = param.toInt();
  stepperV.setMaxSpeed(speed);
  param = Serial.readStringUntil('\n');	// get position
  Serial.println("Moving V");
  long dest = param.toInt();
  up = abs(dest) > abs(stepperV.currentPosition()) ? true : false;  // set direction to up or down
  stepperV.moveTo(dest);
  startRun = true;
  flush();
}

void zeroH()
{
  long currentPosH = stepperH.currentPosition();
  double timesAround = currentPosH / oneRotation;
  double closestPos = oneRotation * timesAround;
  double difference = currentPosH - closestPos;
  if(difference > oneRotation / 2){
    closestPos = closestPos + oneRotation;
    }
  closestPos -= 1600;
  stepperH.setMaxSpeed(2000);
  if(!fullRotate){
    stepperH.moveTo(hZeroPosition);
      while(stepperH.currentPosition() != hZeroPosition){
        stepperH.run();
      }
    }
  else{
    stepperH.moveTo(closestPos);
      while(stepperH.currentPosition() != closestPos){
        stepperH.run();
      }
    }

  stepperH.setCurrentPosition(hZeroPosition);
  zeroHAtEnd = false;
  digitalWrite(LIGHT_LEFT, RELAY_OFF);
  digitalWrite(LIGHT_RIGHT, RELAY_OFF);
}

void endRun()
{
  //Serial.println("endRun");
  // Turn off lights so you don't get blinded
  digitalWrite(LIGHT_LEFT, RELAY_OFF);
  digitalWrite(LIGHT_RIGHT, RELAY_OFF);
  toggleLights = true;
  lightCount = 0;
  lightState = 0;
  // Stop both motors
  up = false;
  startRun = false;
  stepperH.stop();
  stepperH.runToPosition();
  stepperV.stop();
  stepperV.runToPosition();
  if(zeroHAtEnd){
    zeroH();
  }
  
}
