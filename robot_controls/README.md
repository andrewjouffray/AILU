# AILU firmware 

## Project description:

 The controls of the robot will be in 3 layers, these consist of an interface sending json requests to a python server, sending 
 commands through serial to an Arduino script.
 
#### Requirements for the Arduino script:

The script will wait for commands from the python script through serial. The arduino script should not need to
do any calculations (except unit conversions from mm or angle to rotation position), it should just take the data and do what it needs to do. 

__The main loop__

- Waits for data and parses the commands coming through.
- calls the function to perform the task needed.
- makes sure the serial buffer is empty after task is done

How to parse the data:

all commands will come with two letters to identify the command that needs to be ran followed by the required parameters, 
looking like this for example: rn0300360131 rn = run, 0300 = vertical speed, 360 = base plate rotate angle, 1 = track
the object, 3 = light setting, 1 = go to top position.

__1. run(position: int, speed: int, angle:int, lights: int, tracking: boolean)__

- sets the motors speed and the position to go to (converts angles motor position)
- starts a loop 
- runs the vertical stepper motor
- runs the horizontal stepper motor (if the angle is less than 360, go back and forth)
- calls the updateServo function every n loop
- calls the light function every n loop
- ends loop when position is reached
- sends 'done' back to the python server

__2. goTo(position: int, speed: int)__

- sets the motor speed and the position to go to
- starts a loop 
- runs the vertical stepper motor
- ends loop when position is reached
- sends 'done' back to the python server

__3. turnTo(angle: int, speed: int)__

- sets the motor speed and the position to go to
- starts a loop 
- runs the horizontal stepper motor
- ends loop when position is reached
- sends 'done' back to the python server

__4. zeroY()__

- sets the motor speed and the position to go to (something like speed:2000 pos: 1000000)
- checks to see if the bottom switch is already triggered, if not:
- starts a loop 
- runs the vertical stepper motor
- ends loop when bottom switch is triggered
- sets the motor position to zero
- sends 'done' back to the python server

__5. setBottomLimit()__

- sets the bottomLimit to the current motor position.
- sends 'done' back to the python server

__6. setCameraAngle(angle: int)__

- sets the servoAngle
- moves the servos to that angle
- sends 'done' back to the python server
 
__7. updateServo(verticalMotorPosition: int)__

_the distance from the motors to the center of the base is about 350 mm_

- converts the vertical motor pos to mm
- compute the angle that the servos need to be at
- sets the servos to that angle

__8. lights(lightsToTurnOn: int)__

_lightsToTurnOn values 1: all lights on, 2: right light, 3 left light_

- sets the correct relays on
- sets the correct relays off


__9. getDistanceToTravel()__

- calculates the distance that the camera will need to travel
- sends it to the python script

Thank you so much for working with me on this project, it will be a tone of fun, feel free to change things that you want.




