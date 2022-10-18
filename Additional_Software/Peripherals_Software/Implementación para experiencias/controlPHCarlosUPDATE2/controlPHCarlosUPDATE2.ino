#include <Arduino.h>
#include <string.h>
#include <Wire.h>
#include <OneWire.h>
#define SERIAL_DELAY 100
#define SERIAL_BAUD 9600
#define I2C_ADDRESS 0x63
#define I2C_DELAY 300
#define I2C_DATA_DELAY 600
#define RESPONSE_MAXLENGTH 20

double pHObjetivo = 4;
double pHanterior=0;
double zonaMuerta = 0.05;
int gotas=0;
double sencibilidad=0;
int medition = 1;
int totalGotas = 1;
String totalGotasString = "";

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

double getTemperature(){
  double phFinal = 0.0;
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
        String phString = String(temperature);
        phFinal = phString.toDouble();
        if(phFinal<10){
          Serial.print("0");
        }
        Serial.print(temperature);
        break;
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
  
  //if(deviceReachable() != 1){
  //  Serial.print("#1ERROR");
  //}

}

void loop() {
  if(totalGotas<10){
    totalGotasString = "000"+String(totalGotas);
  } else{
     if(totalGotas<100){
          totalGotasString = "00"+String(totalGotas);
     } else {
        if(totalGotas<1000){
         totalGotasString = "0"+String(totalGotas);
        } else {
          totalGotasString = String(totalGotas);
        }
     }
  }
  Serial.print(totalGotasString);
  double pHAhora = getTemperature();
  //if(pHAhora<10){
  //  Serial.print("0");
  //}
  //Serial.print(pHAhora);
  double error = pHAhora - pHObjetivo;
  if(medition>1){
        sencibilidad=abs(1000*(pHAhora-pHanterior)/gotas);
        if(sencibilidad<=20){
          if(abs(error)<=0.2){
            gotas = 2;
          } else{
            if(abs(error)<=0.5){
              gotas = 3;
            } else {
              if(abs(error)<=1){
                gotas = 4;
              } else {
                gotas = 5;
              }
            }
          }
        } else {
          if(abs(error)<=0.2){
            gotas = 1;
          } else{
            if(abs(error)<=0.5){
              gotas = 2;
            } else {
              if(abs(error)<=1){
                gotas = 3;
              } else {
                if(abs(error)<=2){
                   gotas = 4;
                } else {
                  gotas = 5;
                }
              }
            }
          }
        }
  
    if(error>abs(zonaMuerta)){
        setGotasHacido(gotas);
        totalGotas = totalGotas + gotas;
        //setPump(0);
    }
    if(error<(abs(zonaMuerta)*(-1))){
        setGotasBase(gotas);
        totalGotas = totalGotas + gotas;
        //setPump(1);
    }
 }
 medition++;
 pHanterior=pHAhora;
 //delay(5000);
 if(gotas>0){
    delay(5000-gotas*1000);
 } else {
    delay(5000);
 }
}

void setGotasHacido(int gotas) {
  for(int i=1; i<= gotas; i++){
    setPump(0);
  }
}

void setGotasBase(int gotas) {
  for(int i=1; i<= gotas; i++){
      setPump(1);
  }
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

void turnPumpForwards(int pump) {
  digitalWrite(PUMP_PIN2[pump], LOW);
  digitalWrite(PUMP_PIN1[pump], HIGH);
  digitalWrite(PUMP_ENABLE[pump], HIGH);
}

/*char phChar[6];
  phChar[0] = '2';
  phChar[1] = '3';
  phChar[2] = '.';
  phChar[3] = '3';
  phChar[4] = '2';
  String phString = String(phChar);
  double phFinal = phString.toDouble();
  Serial.println(phFinal);*/
