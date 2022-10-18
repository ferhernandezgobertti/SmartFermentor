#include <Arduino.h>
#include <string.h>
#include <TimerOne.h>
#include <OneWire.h> 
#include <DallasTemperature.h>

#define MINIMUM_OFF_TIME 300 // 5*60 seconds
#define MINIMUM_ON_TIME 300 // 5*60 seconds
#define MAXIMUM_OFF_TIME 2400 // 40*60 seconds
#define MAXIMUM_ON_TIME 2100 // 35*60 seconds
#define OFF_TIME 1200 // 20*60 seconds 
#define ON_TIME 1200 // 20*60 seconds
#define MINIMUM_TEMPERATURE 37.00 // Celsius
#define NOMINAL_TEMPERATURE 25.00 // Celsius
#define MAXIMUM_TEMPERATURE 55.00 // Celsius
#define RESPONSE_MAXLENGTH 20
#define TIME_BASE 100
#define INTERRUPT_PIN 2
#define FAN_CONTROL_PIN 5
#define ONE_WIRE_BUS 9 
OneWire oneWire(ONE_WIRE_BUS); 
DallasTemperature sensors(&oneWire);

bool turningOffErrorOccurred = false;
bool turningOnErrorOccurred = false;
bool controlInitialized = false;
char functionID[3];
char content[2];
char receivedLRC[3];
char frameInformation[20];
char allFrameData[20];
char hexadecimalLRC[3];
char dataToSend[20];
char sendingLRC[3];
char sendingCharArray[20];
double currentTemperature = 25.00; // Celsius
int ledState = LOW;
int informationCount = 0;
int currentTime = 0; // Seconds
int currentState = 0;
int firstData = 1;
int readVerification;
int timeCount = 0;
int isDetected = 0;
int packageReceived = 0;
String dataSend;
String sendingFrame;
String sendingFrameLRC;
unsigned long sensorAddress;
unsigned long informationLength;
volatile unsigned long timer = 0;
volatile unsigned long count = 1;
volatile float velocity = 1.00;

char versionInfo[5] = "1.50"; 

void getTemperatureData(){
  sensors.requestTemperatures();
  double possibleTemperature = sensors.getTempCByIndex(0);
  if(possibleTemperature<100 && possibleTemperature>10){
    currentTemperature = possibleTemperature;
  }
}

void controlStateOffDueToFanTemperature(){
  if(currentTemperature < MAXIMUM_TEMPERATURE && currentTime < MAXIMUM_OFF_TIME && !(turningOffErrorOccurred&&turningOnErrorOccurred)){
    digitalWrite(FAN_CONTROL_PIN, LOW);
  } else {
    if(currentTemperature > MAXIMUM_TEMPERATURE){
      turningOffErrorOccurred = currentTime<MINIMUM_OFF_TIME;
      currentState = 1;
      turnFanOn();
    } else {
      if((currentTime > MAXIMUM_OFF_TIME)||(turningOffErrorOccurred&&turningOnErrorOccurred)){
        currentState = 2;
        turnFanOn();
      }
    }
  }
}

void controlStateOnDueToFanTemperature(){
  if(currentTemperature > MINIMUM_TEMPERATURE && !(turningOffErrorOccurred&&turningOnErrorOccurred)){
    digitalWrite(FAN_CONTROL_PIN, HIGH);
  } else {
    if(currentTemperature <= MINIMUM_TEMPERATURE){
      turningOnErrorOccurred = currentTime<MINIMUM_ON_TIME;
      currentState = 0;
      turnFanOff();
    } else {
      if(turningOffErrorOccurred&&turningOnErrorOccurred){
        currentState = 2;
        turnFanOn();
      }
    }
  }   
}

void controlStateOnDueToFanTime(){
  if(currentTime < ON_TIME){
    digitalWrite(FAN_CONTROL_PIN, HIGH);
  } else {
    if(currentTemperature >= ON_TIME){
      currentState = 3;
      turnFanOff();
    }
  }
}

void controlStateOffDueToFanTime(){
  if(currentTime < OFF_TIME){
    digitalWrite(FAN_CONTROL_PIN, LOW);
  } else {
    if(currentTime >= OFF_TIME){
      currentState = 2;
      turnFanOn();
    }
  }
}

void applyFanControl(){
  if(currentState == 0){
    controlStateOffDueToFanTemperature();
  } else {
    if(currentState == 1){
      controlStateOnDueToFanTemperature();
    } else {
      if(currentState == 2){
         controlStateOnDueToFanTime();
      } else {
        if(currentState == 3){
          controlStateOffDueToFanTime();
        }
      }
    }
  }
}

void turnFanOn(){
  digitalWrite(FAN_CONTROL_PIN, HIGH);
  currentTime = 0;
}

void turnFanOff(){
  digitalWrite(FAN_CONTROL_PIN, LOW);
  currentTime = 0;
}

void setup() {
  attachInterrupt(0, stopTimer, RISING);
  pinMode(INTERRUPT_PIN, OUTPUT); 
  pinMode(FAN_CONTROL_PIN, OUTPUT);
  digitalWrite(FAN_CONTROL_PIN, LOW);
  Serial.begin(9600);
  digitalWrite(FAN_CONTROL_PIN, LOW);
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
      sensorAddress = strtoul( content, NULL, 10 );
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
          informationLength = strtoul( content, NULL, 10 );
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


void increaseTimer() {
  timer++;
  if(timer>120000){
    String velString = "";
    velString.concat("000.00");
    velString.concat(currentTemperature);
    velString.concat(currentState);
    Serial.println(velString);
  }
  timeCount = timeCount + 1;
  if(timeCount==10000){
    currentTime = currentTime + 1;
    timeCount = 0;
  }
}  


void stopTimer() {
  char velChar[6];
  String velString = "";
  count = timer;
  velocity = 600000.00/(count);
  if(firstData==0){
    if(velocity<0){
      Serial.println("ERRORL");
    } else {
      if(velocity>1000){
        Serial.println("ERRORM");
      } else {
        if(velocity<10){
          velString.concat("00");
          //ALTERNATIVE: sprintf (velChar, "%01c%01d%01c%01c%02d", '0', 2, '0', '0', velocidad);
        } else {
          if(velocity<100){
            velString.concat("0");
            //ALTERNATIVE: sprintf (velChar, "%01c%01d%01c%03d", '0', 3, '0', velocidad);
          }
        }
        velString.concat(velocity);
        velString.concat(currentTemperature);
        velString.concat(currentState);
        Serial.println(velString);
        informationCount = informationCount + 1;
      }
    }  
  } else {
    firstData = 0;
  }     
  timer = 0;
  digitalWrite(INTERRUPT_PIN, LOW);
}

void loop() {
  getModbusMessage();
  
  if(strcmp(functionID, "CN")==0 && packageReceived == 1){
    char statusInfo[3] = "OK";
    dataSend = "01";
    dataSend.concat(statusInfo);
    sendModbusMessage();
    Serial.flush();

    //ALTERNATIVE: sprintf (dataToSend, "%02c%03c", "01", statusInfo);
  }
  if(strcmp(functionID, "VS")==0 && packageReceived == 1){
    dataSend = "02";
    dataSend.concat(versionInfo);
    sendModbusMessage();
    Serial.flush();
    
    //ALTERNATIVE: 
    //dataToSend = strcat(&versionInfo[0], "02");
    //sprintf (dataToSend, "%02c%04c", "02", versionInfo);
  }
  if(strcmp(functionID, "TF")==0 && packageReceived == 1){
    turnFanOff();
    dataSend = "01OK";
    sendModbusMessage();
    Serial.flush();
  }
  if(strcmp(functionID, "DT")==0 && packageReceived == 1){
    controlInitialized = true;
    dataSend = "02";
    dataSend.concat("OK90");
    sendModbusMessage();

    //ALTERNATIVE:
    //dataToSend = strcat(&dataInfo[0], "02");
    //sprintf (dataToSend, "%02c%04c", "02", dataInfo);

    Timer1.initialize(TIME_BASE);
    Timer1.attachInterrupt(increaseTimer);
    firstData = 1;
    while(informationCount<90){
      digitalWrite(INTERRUPT_PIN, HIGH);
    }
    Timer1.detachInterrupt();
    Serial.flush();
    informationCount = 0;
    firstData = 1;
  }
  getTemperatureData();
  if(controlInitialized){
    applyFanControl();
  }
  packageReceived = 0;
}
