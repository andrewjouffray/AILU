
int Vspeed = 0;
int Vlimit = 0;
int Hlimit = 360;
bool tracking = true;
int lightingPreSet = 0;
String currentPosition = "bottom";


String inByte;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

// Vlim = set bottom limit | value 0, -38407
// Hlim = set rotation limit | value 0 , 3492
// trac = track the object of interest | value 0, 1
// ligh = sets the lighting settigs | value 1, 3
// runD = runs the robot down (base rotates, lights go on, camera goes down and tracks) | value <speed of the motor>
// runU = runs the robot up (base rotates, lights go on, camera goes up and tracks) | value <speed of the motor>
// getP = returns the current position of the camera | value is not impotant 
// goHo = go horizontal, rotates the robot to a specific position | value 0 , 3492 
// goVe = go vertical, brings the camera up / down to a specific position | value 0, -38407
// anything = gets returns all the settings | value is not important 

void loop() {
  if(Serial.available()){ //checks if there is data coming from the python script
        inByte = Serial.readStringUntil('\n'); // read data until newline
        String command =  inByte.substring(0,4); // first 4 char are the command
        inByte.remove(0,4);
        int value = inByte.toInt(); // the rest of the message is the value (speed, position, settings etc...)

          // sets the lower limit
          if(command == "Vlim"){
            value = value / (0.0097378 * -1);
            Vlimit = value;
            Serial.println("Vertical limit set to : " + String(value));
            
            }

          // sets the rotation limit 
          else if (command == "Hlim"){
            value = value * 9.7;
            Hlimit = value;
            Serial.println("Horizontal limit set to : " + String(value));
            }

          // sets the track object boolean
          else if (command == "trac"){
                if(value != 1){
                    tracking = false;
                  }else{
                  tracking = true;   
                 }
                Serial.println("object tracking set to : " + String(tracking));
            
            }

          // sets the lights settings 
          else if (command == "ligh"){
             lightingPreSet = value;
             Serial.println("lighting pre-set, set to : " + String(value));
            
            }

          // run down, runs the robot and makes the camera go down
          else if (command == "runD"){
            currentPosition = "bottom";
            Serial.println("going down at speed " + String(value));
            // here you would run everything at the given speed
            
            }

          // run Up, runs the robot and makes the camera go up
          else if (command == "runU"){
            currentPosition = "top";
            Serial.println("going up at speed " + String(value));
            }
            
          //prints current position
          else if (command == "getP"){
            Serial.println(currentPosition);
            
            }
            
          // rotates to a position
          else if (command == "goHo"){
            // we will use a constant speeed of 2000
            value = value * 9.7;
            Serial.println("rotating to " + String(value));
            }

          // goes to a position
          else if (command == "goVe"){
            // we will use a constant speeed of 2000
            value = value / (0.0097378 * -1);
            Serial.println("going to " + String(value));
            }

           // prints all the settings
           else{
              Serial.println(String(Vspeed) + "," + String(Vlimit) + "," +  String(Hlimit) + "," + String(tracking) + "," + String(lightingPreSet));
            }



  }

}
