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
}


// TODO: finish this
void printSettings() 
{
//  getPosition();
  Serial.readStringUntil('\n'); // flush the buffer
  Serial.println("Settings");
}



void setLighting(){
  // TODO
  String param = Serial.readStringUntil('\n');
  lighting = param.toInt();
}

void setZero()
{
  Serial.readStringUntil('\n');
  stepperV.setCurrentPosition(0);
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
}

void setVLimit()
{
  param = Serial.readStringUntil('\n');
  int vLimit = param.toInt();
  if (vLimit >= 0)
  {
    minBottomPosition = vLimit;
  }
  else
  {
    Serial.println("Error: Invalid vertical limit");
  }
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
  }
  else
  {
    angle = hLimit;
    fullRotate = false;
  }
}


// TODO: Finish (or scrap) this
// Possibly have setHSpeed and setVSpeed
// Do we only care about vertical speed? Is horizontal speed always the same?
void setVSpeed()
{
  param = Serial.readStringUntil('\n');
  long speed = param.toInt();
  stepperV.setMaxSpeed(speed);
}

void setHSpeed()
{
  param = Serial.readStringUntil('\n');
  long speed = param.toInt();
  stepperH.setMaxSpeed(speed);
}

//TODO: Add setMotor
void setMotor()
{

}

void setTracking()
{
  param = Serial.readStringUntil('\n');
  tracking = param.toInt();
}

void runD()
{
  zeroHAtEnd = true;
//  param = Serial.readStringUntil('\n');
//  int speed = param.toInt();
//  stepperV.setMaxSpeed(speed);
//  stepperH.setMaxSpeed(2000);
  Serial.println("stepperH at: " + String(stepperH.currentPosition()));
  positions[STEPPER_V] = minBottomPosition;
  Serial.println("stepperH moving at speed " + String(stepperH.maxSpeed()) + " going to " + angle);
  stepperH.moveTo(angle);
  stepperV.moveTo(minBottomPosition);
  up = false;
  startRun = true;
}

void runU()
{
  zeroHAtEnd = true;
//  param = Serial.readStringUntil('\n');
//  int speed = param.toInt();
//  stepperV.setMaxSpeed(speed);
//  stepperH.setMaxSpeed(2000);
  Serial.println("stepperH at: " + String(stepperH.currentPosition()));
  positions[STEPPER_V] = maxTopPosition;
  Serial.println("stepperH moving at speed " + String(stepperH.maxSpeed()) + " going to " + angle);
  stepperH.moveTo(angle);
  stepperV.moveTo(maxTopPosition);
  up = true;
  startRun = true;
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
  Serial.println("moving to " + String(dest));
  stepperH.moveTo(dest);
  startRun = true;
}

void moveV()
{
  
  param = Serial.readStringUntil(' ');	// get speed
  int speed = param.toInt();
  stepperV.setMaxSpeed(speed);
  param = Serial.readStringUntil('\n');	// get position
  Serial.println("this is the position as a String: " + param);
  long dest = param.toInt();
  up = abs(dest) > abs(stepperV.currentPosition()) ? true : false;  // set direction to up or down
  //Serial.print("up = ");
  //Serial.println(up);
  Serial.println("speed " + String(speed) + " to position " + String(dest));
//  positions[STEPPER_H] = stepperH.currentPosition();
//  positions[STEPPER_V] = dest;
//  steppers.moveTo(positions);
  stepperV.moveTo(dest);
  startRun = true;
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
  
  Serial.println("zeroing H to " + String(closestPos));
  stepperH.setMaxSpeed(2000);
  if(!fullRotate){
    stepperH.moveTo(hZeroPosition);
    }
  else{
    stepperH.moveTo(closestPos);
    }
  while(stepperH.currentPosition() != closestPos){
    stepperH.run();
    }
  stepperH.setCurrentPosition(hZeroPosition);
  Serial.println("H is zeroed");
  zeroHAtEnd = false;
  }

void endRun()
{
  Serial.println("endRun");
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