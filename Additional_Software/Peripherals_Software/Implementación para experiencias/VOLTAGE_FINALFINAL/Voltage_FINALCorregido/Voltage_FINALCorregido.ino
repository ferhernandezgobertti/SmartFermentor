#include <TimerOne.h>
#include <Arduino.h>
#include <string.h>
#include "StringSplitter.h"
const int pingGate = 13;  // the pin with a LED
volatile unsigned int atraso = 50 ; // La definimos como volatile
volatile unsigned long delta = 5;
char atrasoChar[20];
int atrasoPosibilidad;
char deltaChar[20];
int deltaPosibilidad;
byte characterRead;

void setup() {
  // put your setup code here, to run once:
    attachInterrupt(0, gateOff, RISING);
    pinMode(pingGate, OUTPUT);//leed de prueba y gate de triac
    digitalWrite(pingGate, HIGH);
    Serial.begin(9600);
    //Serial.setTimeout(2);
}

void gateOff(){
  digitalWrite(pingGate, HIGH);
  for(int j=0; j<atraso; j++){
    delayMicroseconds(100);
    }
  digitalWrite(pingGate, LOW);
  for(int j=0; j<delta; j++){
    delayMicroseconds(100);
    }
  digitalWrite(pingGate, HIGH);
}

void loop() {
  int bytesRead=0;
  if(Serial.available()>0){
    
    while(bytesRead<4){
      characterRead = Serial.read();
      /*if(bytesRead==0 && characterRead!='#'){
        Serial.println("#ERROR");
      }*/
      Serial.println(characterRead);
      if(bytesRead==0){
        atrasoChar[0] = characterRead;
      }
      if(bytesRead==1){
        atrasoChar[1] = characterRead;
      }
      /*if(bytesRead==3 && characterRead!='#'){
        Serial.println("#ERROR");
      }*/
      if(bytesRead==2){
        deltaChar[0] = characterRead;
      }
      if(bytesRead==3){
        deltaChar[1] = characterRead;
      }
      bytesRead++;
    }
    atrasoPosibilidad = atrasoChar-'0';
    deltaPosibilidad = deltaChar-'0';
    if(atrasoPosibilidad>=10 && atrasoPosibilidad<=99){
      atraso = atrasoPosibilidad;
      Serial.print("ATRASO: ");
      Serial.println(atraso);
    }
    if(deltaPosibilidad>=1 && deltaPosibilidad<=10){
      delta = deltaPosibilidad;
      Serial.print("DELTA: ");
      Serial.println(delta);
    }
    
    Serial.println("#GOOD!");
  }
}




