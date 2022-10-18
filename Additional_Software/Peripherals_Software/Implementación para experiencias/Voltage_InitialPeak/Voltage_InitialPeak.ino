#include <TimerOne.h>
#include <Arduino.h>
#include <string.h>
#include "StringSplitter.h"
const int pinGateInit = 4;
const int pingGate = 13;  
volatile unsigned int atraso = 280 ;
volatile unsigned long delta = 4;
char messageInput[20];
int atrasoPosibilidad;
int deltaPosibilidad;
int bytesRead;

void setup() {
    pinMode(pingGate, OUTPUT);
    digitalWrite(pinGateInit, LOW);
    pinMode(pingGate, OUTPUT);
    digitalWrite(pingGate, LOW);
    
    attachInterrupt(0, gateOff, RISING);    
    Serial.begin(9600);
    bytesRead = 0;
    //delay(1000);
    pinMode(pingGate, OUTPUT);
    digitalWrite(pinGateInit, HIGH);
    pinMode(pingGate, OUTPUT);
    
}

void gateOff(){
  
  delayMicroseconds(200);
  digitalWrite(pingGate, LOW);
  for(int j=0; j<atraso; j++){
    delayMicroseconds(25);
    }
  digitalWrite(pingGate, HIGH);
  for(int j=0; j<delta; j++){
    delayMicroseconds(25);
    }
  digitalWrite(pingGate, LOW);

}

void loop() {
  
  if(Serial.available()>0){
    
    int charsRead = Serial.readBytesUntil('X', messageInput, sizeof(messageInput)-1);
    
    int atrasoPos = atoi(messageInput);
    if(atrasoPos<90){
      atraso = atrasoPos + 200;
    }
    if(atrasoPos>90){
      atraso = atrasoPos + 100;
    }
    if(atraso==90){
      atraso = 400;
    }
    if(atrasoPos<0 || atrasoPos>99){
      Serial.print("ERROR");
    } else {
      Serial.print("GOOD!");
    }
    atrasoPos = 0;

  }
  
}

    /* ALTERATIVA: Separar por caracteres (desincronizacion con tiempo de Interrupciones)
    char deltaChar[2];
    deltaChar[0] = messageInput[2];
    deltaChar[1] = messageInput[3];
    delta = atoi(deltaChar);
    */

    /* ALTERNATIVA (+ propenso a errores):
    String atrasoString;
    String deltaString;
    StringSplitter *voltageSplitter = new StringSplitter(messageInput, '#', 2);
    int splitCount = voltageSplitter->getItemCount();
    for(int split=0; split<splitCount; split++){
      if(split==0){
        atrasoString = voltageSplitter->getItemAtIndex(split);
      }
      deltaString = voltageSplitter->getItemAtIndex(split);
    }
    char atrasoCharArray[20];
    atrasoString.toCharArray(atrasoCharArray, sizeof(atrasoCharArray));
    atrasoPosibilidad = atoi(atrasoCharArray);
    if(atrasoPosibilidad>=10){
      atraso = atrasoPosibilidad;
    }
    char deltaCharArray[20];
    deltaString.toCharArray(deltaCharArray, sizeof(deltaCharArray));
    deltaPosibilidad = atoi(deltaCharArray);
    if(deltaPosibilidad>=10){
      delta = deltaPosibilidad;
    }
    Serial.println("#GOOD!");*/



