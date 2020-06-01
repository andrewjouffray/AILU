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
*  setMotor <h | v> <0 | 1>
*   toggles motor on or off
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
*  setLighting
*   both always on, alternating between the two, "both on, this one off"

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



void setLighting(){
  // TODO
  Serial.println("Lighting set");
  String param = Serial.readStringUntil('\n');
  lighting = param.toInt();

  flush();
}

void setZero()
{
  Serial.readStringUntil('\n');
  stepperV.setCurrentPosition(0);

  flush();
}

void reset()
{
  // reset speed and limits
  Serial.readStringUntil('\n');
  endRun();

  // Reset all default values
  angle = 100000;  // Set horizontal motor to rotate without stopping
  fullRotate = true;
  maxTopPosition = -38407;
  minBottomPosition = 0;
  lighting = 1;
  speedV = 2000.0;
  speedH = 1000.0;
  tracking = 0;
  startRun = false;
  fullRotate = true;
  up = false;
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
  hLimitPlus = hZeroPosition + hLimit * convertionMultiplication; // converts degrees to motor position
  hLimitMin = hZeroPosition - hLimit * convertionMultiplication;
  if (hLimitPlus >= hZeroPosition + oneRotation)
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

void servo(){
  param = Serial.readStringUntil('\n');
  long pos = param.toInt();
  Serial.println("moving servos");
  moveServos(pos);
  flush();
  }

// TODO: Finish (or scrap) this
// Possibly have setHSpeed and setVSpeed
// Do we only care about vertical speed? Is horizontal speed always the same?
void setVSpeed()
{
  param = Serial.readStringUntil('\n');
  long speed = param.toInt();
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

//TODO: Add setMotor
void setMotor()
{

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
  positions[STEPPER_V] = minBottomPosition;
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
  positions[STEPPER_V] = maxTopPosition;
  stepperH.moveTo(angle);
  stepperV.moveTo(maxTopPosition);
  up = true;
  startRun = true;
  flush();
}

void moveH()
{
  fullRotate = true;
  Serial.println("MoveH");
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

void zeroH(){


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
