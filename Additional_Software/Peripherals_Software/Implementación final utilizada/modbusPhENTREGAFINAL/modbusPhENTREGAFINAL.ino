#include <Arduino.h>
#include <string.h>
#include <Wire.h>
#include <OneWire.h>

#define SERIAL_DELAY 100 // microseconds
#define SERIAL_BAUD 9600
#define I2C_ADDRESS 0x63
#define I2C_DELAY 300 // microseconds
#define I2C_DATA_DELAY 900 // microseconds
#define ANALOG_READ_MAX 1023
#define PH_I2C_ADDRESS 99
#define SECONDARY_PSU_STATUS_READ_THRESHOLD 512
#define SECONDARY_PSU_STATUS_PIN A0
#define RESPONSE_MAXLENGTH 20
#define COMMUNICATION_DELAY_MAX 60 // microseconds
#define MAXIMUM_SCALE_PH 14
#define MINIMUM_SCALE_PH 1
#define ACTION_PERIOD 6000 // 6 seconds
#define TWO_DIGIT_LIMIT 10

char functionID[3];
char content[2];
char receivedLRC[3];
char frameInformation[30];
char allFrameData[20];
char hexadecimalLRC[3];
char dataToSend[20];
char sendingLRC[3];
char sendingCharArray[20];
const byte PUMP_ENABLE[] = {5, 6, 3};
const byte PUMP_PIN1[] = {8, 10, 12};
const byte PUMP_PIN2[] = {9, 11, 13};
double pHActual;
int isDetected = 0;
int packageReceived = 0;
int dropsMode = 1;
int dutyCycle = 10; // Percentage
int timeInterval = 500;
int readVerification;
String dataSend;
String sendingFrame;
String sendingFrameLRC;
unsigned long sensorAddress;
unsigned long informationLength;

char versionInfo[5] = "1.50"; 

byte deviceReachable(){
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("Find <cr>");
  Wire.endTransmission();
  delay(I2C_DELAY);
  Wire.requestFrom(I2C_ADDRESS, 1, 1);
  byte responseRight = Wire.read();
  Wire.endTransmission();
  return responseRight;
}

byte calibrateClear(){
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("Cal,clear");
  Wire.endTransmission();
  delay(I2C_DATA_DELAY);
  Wire.requestFrom(I2C_ADDRESS, 1, 1);
  byte responseRight = Wire.read();
  Wire.endTransmission();
  return responseRight;
}

byte calibrateMiddle(){
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("Cal,mid,7.00");
  Wire.endTransmission();
  delay(I2C_DATA_DELAY);
  Wire.requestFrom(I2C_ADDRESS, 1, 1);
  byte responseRight = Wire.read();
  Wire.endTransmission();
  return responseRight;
}

byte calibrateLow(){
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("Cal,low,4.00");
  Wire.endTransmission();
  delay(I2C_DATA_DELAY);
  Wire.requestFrom(I2C_ADDRESS, 1, 1);
  byte responseRight = Wire.read();
  Wire.endTransmission();
  return responseRight;
}

byte calibrateHigh(){
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("Cal,high,10.00");
  Wire.endTransmission();
  delay(I2C_DATA_DELAY);
  Wire.requestFrom(I2C_ADDRESS, 1, 1);
  byte responseRight = Wire.read();
  Wire.endTransmission();
  return responseRight;
}

double getPotHydrogenValue(){
  double phFinal = 0.0;
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("R");  //WRITE TO SENSOR
  Wire.endTransmission();
  delay(I2C_DATA_DELAY);
  Wire.requestFrom(I2C_ADDRESS, RESPONSE_MAXLENGTH, 1);
  byte responseRight = Wire.read(); //READ FROM SENSOR
  if (responseRight == 1) {  
    char potHydrogenRead[RESPONSE_MAXLENGTH];
    byte i = 0;
    while (Wire.available()) {
      char medition = Wire.read();
      potHydrogenRead[i] = medition;
      i++;
      if (medition== 0) {
        String phString = String(potHydrogenRead);
        phFinal = phString.toDouble();
        break;

        // ALTERNATIVE:
        // String phStringFinal = String(phString.charAt(0))+String(phString.charAt(1))+String(phString.charAt(2))+String(phString.charAt(3));
        // Serial.println((int)(phString.toDouble()*10));
        // phFinal = ((int)(phString.toDouble()*10))/10;
      }
    }
  }
  Wire.endTransmission();
  return phFinal;
}

void setup() {
  Wire.begin();
  Serial.begin(SERIAL_BAUD);
  delay(SERIAL_DELAY);
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

int getDrops(int burstsAcid, int burstsBase){
  int bursts = 0;
  if(burstsAcid>0){
    setBurstsAcid(burstsAcid);
    bursts = burstsAcid;
  }
  if(burstsBase>0){
    setBurstsBase(burstsBase);
    bursts = burstsBase;
  }
  return bursts;
}

void setBurstsAcid(int burstsQuantity) {
  for(int i=1; i<= burstsQuantity; i++){
    setPump(0);
    delay(timeInterval);
  }
}

void setBurstsBase(int burstsQuantity) {
  for(int i=1; i<= burstsQuantity; i++){
    setPump(1);
    delay(timeInterval);
  }
} 

void setPump(int bombID) {
  int period = 1000;
  int timeUP = 10*dutyCycle; //gotas*100
  int timeDOWN = period - timeUP;
  turnPumpForwards(bombID);
  delay(timeUP);
  turnPumpsOff();
  delay(timeDOWN);
}

void turnPumpsOff(){
  digitalWrite(PUMP_PIN1[0], LOW);
  digitalWrite(PUMP_PIN1[1], LOW);
  digitalWrite(PUMP_PIN1[2], LOW);
}

void turnPumpForwards(int pump) {
  digitalWrite(PUMP_PIN2[pump], LOW);
  digitalWrite(PUMP_PIN1[pump], HIGH);
  digitalWrite(PUMP_ENABLE[pump], HIGH);
}

void loop() {
  getModbusMessage();
  
  if(strcmp(functionID, "CN")==0 && packageReceived == 1){
    if(strcmp(frameInformation, "CHSS")==0){
      if(deviceReachable() != 1){
        dataSend = "02";
        dataSend.concat("SSER");
      } else {
        dataSend = "02";
        dataSend.concat("SSOK");
      }
    }
    if(strcmp(frameInformation, "CHCR")==0){
      dataSend = "02";
      dataSend.concat("CROK");
    }
    
    sendModbusMessage();
    Serial.flush();
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
  if(strcmp(functionID, "CB")==0 && packageReceived == 1){

    // CALIBRATION 7 - NEUTRAL MEDIUM
    if(strcmp(frameInformation, "C7NT")==0){ 
      if(calibrateClear() != 1){
        dataSend = "02";
        dataSend.concat("CLER");
      } else {
        if(calibrateMiddle() != 1){
          dataSend = "02";
          dataSend.concat("C7ER");
        } else {
        dataSend = "02";
        dataSend.concat("C7OK");
        }
      }
    }

    // CALIBRATION 4 - ACID MEDIUM
    if(strcmp(frameInformation, "C4AC")==0){ 
      if(calibrateLow() != 1){
        dataSend = "02";
        dataSend.concat("C4ER");
      } else {
        dataSend = "02";
        dataSend.concat("C4OK");
      }
    }

    // CALIBRATION 10 - BASIC MEDIUM
    if(strcmp(frameInformation, "C10B")==0){
      if(calibrateHigh() != 1){
        dataSend = "03";
        dataSend.concat("CB10ER");
      } else {
        dataSend = "03";
        dataSend.concat("CB10OK");
      }
    }
    sendModbusMessage();
    Serial.flush();
    
    /* ALTERNATIVE: 
    int countPrueba = 0;
    while(countPrueba<5){
      double potentialActual = getPotHydrogenValue();
      Serial.println(potentialActual);
      countPrueba = countPrueba + 1;
    } */
  }
  if(strcmp(functionID, "EX")==0 && packageReceived == 1){
    int burstsExpulsionQuantity = ((int)frameInformation[2]-48)*10+((int)frameInformation[3]-48)*1;
    dropsMode = ((int)frameInformation[5]-48)*1;
    if(dropsMode == 4){
      dutyCycle = 40;
    }
    if(dropsMode == 3){
      dutyCycle = 30;
    }
    if(dropsMode == 2){
      dutyCycle = 20;
    } 
    if(dropsMode == 1) {
      dutyCycle = 10;
    }
    // ALTERNATIVE: unsigned long expulsionQuantity = strtoul( dataQuantity, NULL, 10 );
    
    dataSend = "02";
    
    //EXTRACT ACID THROUGH PUMP 01
    if((frameInformation[0] == 'A') && (frameInformation[1] == 'C')){ 
      setBurstsAcid(burstsExpulsionQuantity);
      dataSend.concat("ACOK");
    } else {
      
      //EXTRACT BASE THROUGH PUMP 02
      if((frameInformation[0] == 'B') && (frameInformation[1] == 'A')){ //EXTRACT BASE
        setBurstsBase(burstsExpulsionQuantity);
        dataSend.concat("BAOK");
      } else {
        dataSend.concat("ERRO");
      }
    }
    sendModbusMessage();
    Serial.flush();
  }
  if(strcmp(functionID, "CR")==0 && packageReceived == 1){
    int burstsAcid = ((int)frameInformation[0]-48)*10+((int)frameInformation[1]-48)*1; // Independent from MODE
    int burstsBase = ((int)frameInformation[2]-48)*10+((int)frameInformation[3]-48)*1; // Independent from MODE
    dropsMode = ((int)frameInformation[5]-48)*1;
    timeInterval = ((int)frameInformation[7]-48)*100+((int)frameInformation[8]-48)*10+((int)frameInformation[9]-48)*1;
    
    if(dropsMode == 4){
      dutyCycle = 40;
    }
    if(dropsMode == 3){
      dutyCycle = 30;
    }
    if(dropsMode == 2){
      dutyCycle = 20;
    } 
    if(dropsMode == 1) {
      dutyCycle = 10;
    }
    int burstsActual = getDrops(burstsAcid, burstsBase);
    int delayCompensation = burstsActual*(1000+timeInterval-COMMUNICATION_DELAY_MAX);
    if(delayCompensation<ACTION_PERIOD){
      delay(ACTION_PERIOD-delayCompensation);
    }
    
    dataSend = "02";
    burstsActual = burstsActual*dropsMode;
    if(burstsActual>=0){
      dataSend.concat("OK");
      if(burstsActual<TWO_DIGIT_LIMIT){
        dataSend.concat("0");
      } 
      dataSend.concat(burstsActual);
    } else {
      dataSend.concat("ERRO");
    }
    sendModbusMessage();
  }
  
  if(strcmp(functionID, "TS")==0 && packageReceived == 1){
    int countTesting = 0;
    while(countTesting < 5){
      dataSend = "04";
      pHActual = getPotHydrogenValue();
      if(pHActual<MINIMUM_SCALE_PH){
        dataSend.concat("ERRORL");
      } else {
        if(pHActual>MAXIMUM_SCALE_PH){
          dataSend.concat("ERRORM");
        } else {
          if(pHActual<TWO_DIGIT_LIMIT){
            dataSend.concat("0");
          }
          dataSend.concat("0");
          dataSend.concat(pHActual);

          // ALTERNATIVE: 
          // String pHFinalFinal = String(pHActual).substring(0,6);
          // dataSend.concat(pHFinalFinal); //((int)(pHActual*10))/10);  //(pHActual);
        }
      }
      sendModbusMessage();
      countTesting = countTesting + 1;
    }
  }
  
  if(strcmp(functionID, "DT")==0 && packageReceived == 1){
    dataSend = "04";
    pHActual = getPotHydrogenValue();
    if(pHActual<MINIMUM_SCALE_PH){
      dataSend.concat("ERRORL");
    } else {
      if(pHActual>MAXIMUM_SCALE_PH){
        dataSend.concat("ERRORM");
      } else {
        if(pHActual<TWO_DIGIT_LIMIT){
          dataSend.concat("0");
        }
        dataSend.concat("0");
        dataSend.concat(pHActual);
        
        //ALTERNATIVE: 
        //String pHFinalFinal = String(pHActual).substring(0,4);
        //dataSend.concat(pHFinalFinal);

        //ALTERNATIVE:
        //dataToSend = strcat(&dataInfo[0], "02");
        //sprintf (dataToSend, "%02c%04c", "02", dataInfo);
      }
    }
    sendModbusMessage();
  }
  packageReceived = 0;
}
