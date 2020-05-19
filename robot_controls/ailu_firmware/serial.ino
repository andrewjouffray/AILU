// return enum of corresponding command
cmd hashit(String command){
//  Serial.print("Command: ");
//  Serial.println(command);
  if(command == "?") return eQ;
  if(command == ".") return eSettings;
  if(command == "getP") return eGetP;
  if(command == "setLighting") return eSetLighting;
  if(command == "setVLimit") return eSetVLimit;
  if(command == "setHLimit") return eSetHLimit;
  if(command == "setVSpeed") return eSetVSpeed; // consider deleting?
  if(command == "setHSpeed") return eSetHSpeed; // consider deleting?
  if(command == "setMotor") return eSetMotor;
  if(command == "setTracking") return eSetTracking;
  if(command == "runD") return eRunD;
  if(command == "runU") return eRunU;
  if(command == "moveH") return eMoveH;
  if(command == "moveV") return eMoveV;
  if(command == "end") return eEnd;
  if(command ==  "setZero") return eSetZero;
  if(command ==  "zeroV") return eReset;
  return eUnknown; // command not found
}

// parse command and call corresponding handler
void handleSerial()
{
  // Get command
  command = Serial.readStringUntil(' ');  

  switch(hashit(command)){
    case eQ:
      printCommands();
      break;
    case eSettings:
      printSettings();
      break;
    case eGetP:
      getPosition();
      break;
    case eSetLighting:
      setLighting();
      break;
    case eSetVLimit:
      setVLimit();
      break;
    case eSetHLimit:
      setHLimit();
      break;
    case eSetVSpeed:
      setVSpeed();
      break;
    case eSetHSpeed:
      setHSpeed();
      break;
    case eSetMotor:
      setMotor();
      break;
    case eSetTracking:
      setTracking();
      break;
    case eRunD:
      runD();
      break;
    case eRunU:
      runU();
      break;
    case eMoveH:
      moveH();
      break;
    case eMoveV:
      moveV();
      break;
    case eEnd:
      endRun();
      break;
    case eSetZero:
      setZero();
      break;
    case eReset:
      reset();
      break;
    case eUnknown:
    default:
      Serial.println("Error: Unknown command");
      break;     
  }
}