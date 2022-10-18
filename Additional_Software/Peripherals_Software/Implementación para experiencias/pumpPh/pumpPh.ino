#include <Arduino.h>
#include <string.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
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

// General
//#define SERIAL_BAUD 115200
#define ANALOG_READ_MAX 1023
#define PH_I2C_ADDRESS 99
#define TEMP_I2C_ADDRESS 102
#define SECONDARY_PSU_STATUS_READ_THRESHOLD 512

// Pins
const byte PUMP_ENABLE[] = {5, 6, 3};
const byte PUMP_PIN1[] = {8, 10, 12};
const byte PUMP_PIN2[] = {9, 11, 13};
#define SECONDARY_PSU_STATUS_PIN A0


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

void setup() {
  Serial.begin(SERIAL_BAUD);
  Serial.setTimeout(50);
  pinMode(PUMP_ENABLE[0], OUTPUT);
  digitalWrite(PUMP_ENABLE[0], LOW);
  pinMode(PUMP_ENABLE[1], OUTPUT);
  digitalWrite(PUMP_ENABLE[1], LOW);
  pinMode(PUMP_ENABLE[2], OUTPUT);
  digitalWrite(PUMP_ENABLE[2], LOW);
  pinMode(PUMP_PIN1[0], OUTPUT);
  digitalWrite(PUMP_PIN1[0], LOW);
  pinMode(PUMP_PIN1[1], OUTPUT);
  digitalWrite(PUMP_PIN1[1], LOW);
  pinMode(PUMP_PIN1[2], OUTPUT);
  digitalWrite(PUMP_PIN1[2], LOW);
  pinMode(PUMP_PIN2[0], OUTPUT);
  digitalWrite(PUMP_PIN2[0], LOW);
  pinMode(PUMP_PIN2[1], OUTPUT);
  digitalWrite(PUMP_PIN2[1], LOW);
  pinMode(PUMP_PIN2[2], OUTPUT);
  digitalWrite(PUMP_PIN2[2], LOW);
  Wire.begin();

  /*int salto = 0;
  while(salto<=100){
    medition++;
    int output;
    Serial.print((int)(salto/100));
    if((output = getTemperature()) != 1 && medition!=1){
      //Serial.print("Serial could not GET TEMPERATURE: ");
      //Serial.print(output);
      Serial.print("#tERROR");
      //resetArduino(WDTO_15MS);
    }
    salto = salto + 1;
    delay(60);
  }
  salto = 0;
  while(salto<=250){
    setPump();
    salto = salto + 1;
  }*/
  
  //if(deviceReachable() != 1){
    //Serial.print("Serial could not BE REACHED: ");
    //Serial.print("#1ERROR");
  //}

}

void loop() {

  /*int salto = 0;
  while(salto<=100){
    medition++;
    int output;
    Serial.print((int)(salto/100));
    if((output = getTemperature()) != 1 && medition!=1){
      //Serial.print("Serial could not GET TEMPERATURE: ");
      //Serial.print(output);
      Serial.print("#tERROR");
      //resetArduino(WDTO_15MS);
    }
    salto = salto + 1;
    delay(60);
  }*/
  
  //setPump(2);
  /*int salto = 0;
  while(salto<=100){
    medition++;
    int output;
    Serial.print((int)(salto/100));
    if((output = getTemperature()) != 1 && medition!=1){
      //Serial.print("Serial could not GET TEMPERATURE: ");
      //Serial.print(output);
      Serial.print("#tERROR");
      //resetArduino(WDTO_15MS);
    }
    salto = salto + 1;
    //delay(60);
  }*/
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
        //Serial.print("#");
        Serial.print(temperature);
        
        break;
      }
    }
  }
  Wire.endTransmission();
  return responseRight;
}

char* setPump(int bomba) {
  int drops = 1;
  int period = 1000;
  int timeUP = drops*100;
  int timeDOWN = period - timeUP;
  turnPumpForwards(bomba);
  delay(timeUP);
  digitalWrite(PUMP_PIN1[0], LOW);
  digitalWrite(PUMP_PIN1[1], LOW);
  digitalWrite(PUMP_PIN1[2], LOW);
  delay(timeDOWN);
}

char* setPump32() {
  int drops = 5;
  int period = 1000;
  int timeUP = drops*100;
  int timeDOWN = period - timeUP;
  //turnPumpBackwards(2);
  turnPumpForwards(0);
  turnPumpForwards(1);
  turnPumpForwards(2);
  delay(timeUP);
  digitalWrite(PUMP_PIN1[0], LOW);
  digitalWrite(PUMP_PIN1[1], LOW);
  digitalWrite(PUMP_PIN1[2], LOW);
  //turnPumpBackwards(0);
  //turnPumpBackwards(1);
  //turnPumpBackwards(2);
  delay(timeDOWN);
}

char* setPump2() {
  int drops = 5;
  int period = 1000;
  int timeUP = drops*100;
  int timeDOWN = period - timeUP;
  digitalWrite(PUMP_PIN1[0], LOW);
  digitalWrite(PUMP_PIN1[1], LOW);
  digitalWrite(PUMP_PIN1[2], LOW);
  delay(timeUP);
  turnPumpBackwards(0);
  turnPumpBackwards(1);
  turnPumpBackwards(2);
  delay(timeDOWN);
}

void turnPumpOff(int pump) {
  digitalWrite(PUMP_ENABLE[pump], LOW);
  digitalWrite(PUMP_PIN1[pump], LOW);
  digitalWrite(PUMP_PIN2[pump], LOW);
}

void turnPumpForwards(int pump) {
  digitalWrite(PUMP_PIN2[pump], LOW);
  digitalWrite(PUMP_PIN1[pump], HIGH);
  digitalWrite(PUMP_ENABLE[pump], HIGH);
}

void turnPumpBackwards(int pump) {
  digitalWrite(PUMP_PIN1[pump], LOW);
  digitalWrite(PUMP_PIN2[pump], HIGH);
  digitalWrite(PUMP_ENABLE[pump], HIGH);
}
