String variable = "0";
String inByte;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){ //checks if there is data coming from the python script
    // read data
    
        
        inByte = Serial.readStringUntil('\n'); // read data until newline
        if(inByte.length() >= 8){

          // parses the data into strings
          String vSpeedByte = inByte;
          String hAngleByte = inByte;
          String trackObjectByte = inByte;
          String lightingByte = inByte;
          String directionByte = inByte;
    
          lightingByte = lightingByte.charAt(7);
          trackObjectByte = trackObjectByte.charAt(6);
          hAngleByte.remove(6,7);
          hAngleByte.remove(0,3);
          vSpeedByte.remove(3,7);
          directionByte = directionByte.charAt(8);
            
          Serial.println(vSpeedByte + "|" + hAngleByte + "|" + trackObjectByte+ "|" + lightingByte);

        }else{
          String all = inByte;
          char message = all.charAt(0);
          if(message == 'm'){
            delay(1000);
            Serial.println("responce after delay!");
            
            }
          else if(message == 'n'){

            Serial.println("emidiate responce");
            
            }
          else if (message == 's'){
            inByte.remove(0);
            variable = inByte;
            Serial.println(variable);
            }

          else if (message == 'g'){

                Serial.println(variable);
            
            }
        }

  }

}
