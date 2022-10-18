#include <Arduino.h>
#include <string.h>
#include <OneWire.h> 
#include <DallasTemperature.h>

#define SERIAL_BAUD 9600
#define DATA_DELAY 50
#define MINIMUM_SCALE_TEMPERATURE 0
#define MAXIMUM_SCALE_TEMPERATURE 99
#define TWO_DIGIT_LIMIT 10
#define THREE_DIGIT_LIMIT 100
#define RESPONSE_MAXLENGTH 20
#define ONE_WIRE_BUS 2 
OneWire oneWire(ONE_WIRE_BUS); 
DallasTemperature sensors(&oneWire);

char receivedLRC[3];
char frameInformation[20];
char allFrameData[20];
char hexadecimalLRC[3];
char functionID[3];
char content[2];
char dataToSend[20];
char sendingLRC[3];
char sendingCharArray[20];
int readVerification;
int isDetected = 0;
int packageReceived = 0;
String dataSend;
String sendingFrame;
String sendingFrameLRC;
unsigned long sensorAddress;
unsigned long informationLength;

char versionInfo[5] = "1.50"; 

void setup() {
  Serial.begin(SERIAL_BAUD);
  sensors.begin();
}

void updateFrameData(){
  int count = 0;
  while(count<informationLength*2){
    allFrameData[6+count] = frameInformation[count];
    count = count + 1;
  }
}

void getLRCData(){
  int lrc = 0;
  for (int i=0; i<strlen(allFrameData); i++){
    char character = allFrameData[i];
    lrc = (lrc + character) & 0xff;
  }
  lrc = (((lrc^0xff)+1)&0xff);
  utoa((unsigned)lrc,hexadecimalLRC,16); 
  int positionCount = 0;
  while (hexadecimalLRC[positionCount]) {
    hexadecimalLRC[positionCount] = toupper(hexadecimalLRC[positionCount]);
    positionCount++;
  }
}

void getModbusMessage(){
  byte sincByte = Serial.read();
  if(sincByte == ':'){
    readVerification = Serial.readBytes(content, 2);
    if(readVerification==2){
      allFrameData[0] = content[0];
      allFrameData[1] = content[1];
      sensorAddress = strtoul( content, NULL, 10);
      readVerification = Serial.readBytes(content, 2);
      if(readVerification==2){
        allFrameData[2] = content[0];
        allFrameData[3] = content[1];
        functionID[0] = content[0];
        functionID[1] = content[1];
        readVerification = Serial.readBytes(content, 2);
        if(readVerification==2){
          allFrameData[4] = content[0];
          allFrameData[5] = content[1];
          informationLength = strtoul( content, NULL, 10);
          readVerification = Serial.readBytes(frameInformation, informationLength*2);
          if(readVerification==informationLength*2){
            updateFrameData();
            getLRCData();
            readVerification = Serial.readBytes(receivedLRC, 2);
            if(strcmp(hexadecimalLRC, receivedLRC)==0 && readVerification==2){
              readVerification = Serial.readBytes(content, 2);
              if(content[0]=='\r' && content[1]=='\n'){
                packageReceived = 1;
              }
            }
          }
        }
      }
    }
  }
}

void getLRCDataSending(){
  int lrc = 0;
  sendingFrameLRC.toCharArray(sendingCharArray, sendingFrameLRC.length()+1);
  for (int i=0; i<strlen(sendingCharArray); i++){
    char character = sendingCharArray[i];
    lrc = (lrc + character) & 0xff;
  }
  lrc = (((lrc^0xff)+1)&0xff);
  utoa((unsigned)lrc,sendingLRC,16); 
}

void sendModbusMessage(){
  sendingFrame = ":";
  sendingFrameLRC = "";
  sendingFrameLRC.concat("01");
  sendingFrameLRC.concat(functionID);
  sendingFrameLRC.concat(dataSend);
  getLRCDataSending();
  sendingFrame.concat(sendingFrameLRC);
  sendingFrame.concat(sendingLRC);
  Serial.println(sendingFrame);
  
  /*ALTERNATIVE:
  sendingFrame = strcat("01",":");
  sendingFrame = strcat(sendingFrame, functionID);
  sendingFrame = strcat(sendingFrame, dataToSend);
  sendingFrame = strcat(sendingFrame, sendingLRC);
  sendingFrame = strcat(sendingFrame, '\r');
  sendingFrame = strcat(sendingFrame, '\n');
  */
  
}

void getTemperatureValue(){
  sensors.requestTemperatures(); // Send the command to get temperature readings 
  delay(DATA_DELAY);
  double tempValue = sensors.getTempCByIndex(0)+0.94; //IMPLICIT TEMPERATURE CALIBRATION
  String tempString = "";
  if(tempValue<MINIMUM_SCALE_TEMPERATURE){
    tempString.concat("ERRORL");
  } else {
    if(tempValue>MAXIMUM_SCALE_TEMPERATURE){
      tempString.concat("ERRORM");
    } else {
      if(tempValue<TWO_DIGIT_LIMIT){
        tempString.concat("00");
      } else {
        if(tempValue<THREE_DIGIT_LIMIT){
          tempString.concat("0");
        }
      }
      tempString.concat(tempValue);
    }
  }
  dataSend = "03";
  dataSend.concat(tempString);
  sendModbusMessage();
}

void loop() {
  getModbusMessage();
  
  if(strcmp(functionID, "CN")==0 && packageReceived == 1){
    char statusInfo[3] = "OK";
    dataSend = "01";
    dataSend.concat(statusInfo);
    sendModbusMessage();
    Serial.flush();
    // ALTERNATIVE: sprintf (dataToSend, "%02c%03c", "01", statusInfo);
  }
  if(strcmp(functionID, "VS")==0 && packageReceived == 1){
    dataSend = "02";
    dataSend.concat(versionInfo);
    sendModbusMessage();
    Serial.flush();

    // ALTERNATIVE:
    // dataToSend = strcat(&versionInfo[0], "02");
    // sprintf (dataToSend, "%02c%04c", "02", versionInfo);
  }
  if(strcmp(functionID, "TS")==0 && packageReceived == 1){
    int countTesting = 0;
    while(countTesting < 5){
      getTemperatureValue();
      countTesting = countTesting + 1;
    }
  }
  if(strcmp(functionID, "DT")==0 && packageReceived == 1){
    getTemperatureValue();
    Serial.flush();
    
    // ALTERNATIVE:
    // dataToSend = strcat(&dataInfo[0], "02");
    // sprintf (dataToSend, "%02c%04c", "02", dataInfo);

    // ALTERNATIVE:
    // dataSend = "02";
    // dataSend.concat(getTemperatureValue());
  }
  packageReceived = 0;
}
