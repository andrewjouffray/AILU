String inByte;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {

   Serial.print("connection init");

   if(Serial.available()>0){ //checks if there is data coming from the python script
        Serial.print("got some data: ");
        inByte = Serial.readStringUntil('\n');
        Serial.println(inByte);
   }
}
