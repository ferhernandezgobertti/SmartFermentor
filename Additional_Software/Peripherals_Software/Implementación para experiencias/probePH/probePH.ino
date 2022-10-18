#include <Arduino.h>
#include <Wire.h>
#include <string.h>
#include <avr/sleep.h>
#include <avr/wdt.h>
#include "StringSplitter.h"

#define SERIAL_DELAY 100
#define SERIAL_BAUD 9600
#define I2C_ADDRESS 0x63
#define I2C_DELAY 300
#define I2C_DATA_DELAY 600
#define RESPONSE_MAXLENGTH 20

int medition = 0;
char tempUnit; //DEFAULT - ADD AS INPUT
char keepOn;

byte deviceReachable(){
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("Find <cr>");
  Wire.endTransmission();
  delay(I2C_DELAY);
  Wire.requestFrom(I2C_ADDRESS, 1, 1);
  byte responseRight = Wire.read();
  if(responseRight==1){
    Serial.print("#1GOOD!");
  }
  Wire.endTransmission();
  return responseRight;
}

byte calibrateClear(){
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("Cal,clear");
  Wire.endTransmission();
  delay(900);
  Wire.requestFrom(I2C_ADDRESS, 1, 1);
  byte responseRight = Wire.read();
  if(responseRight==1){
    Serial.print("#ClearGOOD!");
  }
  Wire.endTransmission();
  return responseRight;
}

byte calibrateMiddle(){
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("Cal,mid,7.00");
  Wire.endTransmission();
  delay(900);
  Wire.requestFrom(I2C_ADDRESS, 1, 1);
  byte responseRight = Wire.read();
  if(responseRight==1){
    Serial.print("#C7GOOD!");
  }
  Wire.endTransmission();
  return responseRight;
}

byte calibrateLow(){
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("Cal,low,4.00");
  Wire.endTransmission();
  delay(900);
  Wire.requestFrom(I2C_ADDRESS, 1, 1);
  byte responseRight = Wire.read();
  if(responseRight==1){
    Serial.print("#C4GOOD!");
  }
  Wire.endTransmission();
  return responseRight;
}

byte calibrateHigh(){
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("Cal,high,10.00");
  Wire.endTransmission();
  delay(900);
  Wire.requestFrom(I2C_ADDRESS, 1, 1);
  byte responseRight = Wire.read();
  if(responseRight==1){
    Serial.print("#C10GOOD!");
  }
  Wire.endTransmission();
  return responseRight;
}

byte getTemperature(){
  Wire.beginTransmission(I2C_ADDRESS);   
  Wire.write("R");  //WRITE TO SENSOR
  Wire.endTransmission();
  delay(900);
  Wire.requestFrom(I2C_ADDRESS, RESPONSE_MAXLENGTH, 1);
  byte responseRight = Wire.read(); //READ FROM SENSOR
  if (responseRight == 1) {  
    char temperature[RESPONSE_MAXLENGTH];
    byte i = 0;
    while (Wire.available()) {
      char medition = Wire.read();
      temperature[i] = medition;
      i++;
      if (medition== 0) {
        Serial.print("#");
        Serial.print(temperature);
        break;
      }
    }
  }
  Wire.endTransmission();
  return responseRight;
}

void setup() {
  Wire.begin();
  Serial.begin(SERIAL_BAUD);
  delay(SERIAL_DELAY); // WAIT FOR SERIAL PORT TO CONNECT
  
  if(deviceReachable() != 1){
    //Serial.print("Serial could not BE REACHED: ");
    Serial.print("#1ERROR");
  }

  //if(calibrateClear() != 1){
    //Serial.print("Serial could not BE REACHED: ");
    //Serial.print("#ClearERROR");
  //}

  //if(calibrateMiddle() != 1){
  //if(calibrateLow() != 1){
  if(calibrateHigh() != 1){
    //Serial.print("Serial could not BE REACHED: ");
    Serial.print("#C10ERROR");
  }

}

void loop() {
  medition++;
  int output;
  if((output = getTemperature()) != 1 && medition!=1){
    //Serial.print("Serial could not GET TEMPERATURE: ");
    Serial.print(output);
    Serial.println("#tERROR");
    //resetArduino(WDTO_15MS);
  }

  delay(300);

}
