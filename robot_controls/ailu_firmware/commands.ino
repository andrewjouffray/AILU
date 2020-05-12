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
  Serial.print("Current position: ");
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
  Serial.println("not implemented");
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
  angle;
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
  int hLimit = param.toInt();
  if (angle >= 3492)
  {
    angle = 100000;	// Set horizontal motor to rotate without stopping
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
void setSpeed()
{
  param = Serial.readStringUntil('\n');
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
  param = Serial.readStringUntil('\n');
  int speed = param.toInt();
  stepperV.setMaxSpeed(speed);
  positions[STEPPER_V] = minBottomPosition;
  steppers.moveTo(positions);
  up = false;
  startRun = true;
}

void runU()
{
  param = Serial.readStringUntil('\n');
  int speed = param.toInt();
  stepperV.setMaxSpeed(speed);
  positions[STEPPER_V] = maxTopPosition;
  steppers.addStepper(stepperH);
  steppers.addStepper(stepperV);
  steppers.moveTo(positions);
  up = true;
  startRun = true;
}

void moveH()
{
  param = Serial.readStringUntil(' ');	// get speed
  int speed = param.toInt();
  stepperH.setMaxSpeed(speed);
  param = Serial.readStringUntil('\n');	// get position
  positions[STEPPER_H] = param.toInt();
  positions[STEPPER_V] = stepperV.currentPosition();
  steppers.moveTo(positions);
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
  positions[STEPPER_H] = stepperH.currentPosition();
  positions[STEPPER_V] = dest;
  steppers.moveTo(positions);
  startRun = true;
}

void endRun()
{
  // Stop both motors
  up = false;
  startRun = false;
  stepperH.stop();
  stepperH.runToPosition();
  stepperV.stop();
  stepperV.runToPosition();
}
