#include <FuzzyRule.h>
#include <FuzzyComposition.h>
#include <Fuzzy.h>
#include <FuzzyRuleConsequent.h>
#include <FuzzyOutput.h>
#include <FuzzyInput.h>
#include <FuzzyIO.h>
#include <FuzzySet.h>
#include <FuzzyRuleAntecedent.h>

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

int medition = 1;
int totalGotas = 1;
String totalGotasString = "";

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





int inicio = 1;
double phObjetivo = 6.8;
double pHanterior;
double zonaMuerta = 0.05;
double gotas;
static double pHAhora;
static float sens;

// Paso 1 -  creo el objetos Fuzzy
Fuzzy* fuzzyAcid = new Fuzzy();

void setup() {
  Wire.begin();
  Serial.begin(SERIAL_BAUD);
  delay(SERIAL_DELAY);
  

  // Paso 2 - creo entrada difuza Error acidez
  FuzzyInput* errorA = new FuzzyInput(1);

  //Paso 3 - Creo los conjuntos difuzos que componen la entrada difuza error
  FuzzySet* sinErrorA = new FuzzySet(0, 0, 0.05, 0.3); //0.01, 0.2); //0.05, 0.2); // defino funcion de pertenencia sinError
  errorA->addFuzzySet(sinErrorA); // agrego funcion de pertenencia sinError a universo error

  FuzzySet* errorMedioA = new FuzzySet(0.2, 0.5, 0.5, 0.8); //(0.1, 0.5, 0.5, 0.8);//defino funcion epertenencia errorMedioPos
  errorA->addFuzzySet(errorMedioA); // agrego funcion de pertenencia errorMedioPos a universo error

  FuzzySet* muchoErrA = new FuzzySet(0.7, 0.95, 1.1, 1.1); //(0.6, 1, 1.1, 1.1);//defino funcion de pertenencia muchoErrPos
  errorA->addFuzzySet(muchoErrA); // agrego funcion de pertenencia muchoErrPos a universo error

  fuzzyAcid->addFuzzyInput(errorA); // agrego universo de entreda error al objeto Fuzzy


  FuzzyInput* sensibilidadA = new FuzzyInput(2);

  FuzzySet* enBufferA = new FuzzySet(5, 5, 20, 35); // defino funcion de pertenencia sinError
  sensibilidadA->addFuzzySet(enBufferA); // agrego funcion de pertenencia sinError a universo error

  FuzzySet* fueraBufferA = new FuzzySet(28, 37, 50, 50); //(30, 37, 50 , 50); // defino funcion de pertenencia sinError
  sensibilidadA->addFuzzySet(fueraBufferA); // agrego funcion de pertenencia sinError a universo error

  fuzzyAcid->addFuzzyInput(sensibilidadA); // agrego universo de entreda error al objeto Fuzzy


  FuzzyOutput* gotasA = new FuzzyOutput(1);

  FuzzySet* noTiroA = new FuzzySet(0, 0, 1, 2); //Creo funcion de pertenencia noTiro
  gotasA->addFuzzySet(noTiroA); //agrego func. pertenencia noTiro a universo rafagas

  FuzzySet* intermediasA = new FuzzySet(1, 3, 3, 5); //6);
  gotasA->addFuzzySet(intermediasA);

  FuzzySet* muchasA = new FuzzySet(4, 6, 8, 8); //(4,7,8,8); //(4, 6, 7, 7);
  gotasA->addFuzzySet(muchasA);

  fuzzyAcid->addFuzzyOutput(gotasA);

 
  //Paso 6 - Ensamblado de reglas difusas
  // regla difusa "Si error=muchoErrA AND sensibilidad=fueraBufferA  ENTONCES gotas = intermediasA"
  FuzzyRuleAntecedent* SImuchoErrAyyfueraBufferA = new FuzzyRuleAntecedent(); // instancio antecedente
  SImuchoErrAyyfueraBufferA->joinWithAND(muchoErrA, fueraBufferA); // agrego conjuntos difusos al objeto antecedente
  FuzzyRuleConsequent* entoncesIntermediasA = new FuzzyRuleConsequent(); // instancion consecuente
  entoncesIntermediasA->addOutput(intermediasA);// Agrego conjunto difuso al consecuente
  // Instantiating a FuzzyRule object
  FuzzyRule* fuzzyRule01 = new FuzzyRule(1, SImuchoErrAyyfueraBufferA, entoncesIntermediasA); // agrego consecuente y antecedente a la regla difusa

  fuzzyAcid->addFuzzyRule(fuzzyRule01); //agrego regla difusa al objeto fuzzy

  // regla difusa "Si error=errorMedioA AND sensibilidad=fueraBufferA  ENTONCES gotas = noTiroA"
  FuzzyRuleAntecedent* SIerrorMedioAyyfueraBufferA = new FuzzyRuleAntecedent(); // instancio antecedente
  SIerrorMedioAyyfueraBufferA->joinWithAND(errorMedioA, fueraBufferA); // agrego conjuntos difusos al objeto antecedente
  FuzzyRuleConsequent* entoncesnoTiroA = new FuzzyRuleConsequent(); // instancion consecuente
  entoncesnoTiroA->addOutput(noTiroA);// Agrego conjunto difuso al consecuente
  // Instantiating a FuzzyRule object
  FuzzyRule* fuzzyRule02 = new FuzzyRule(2, SImuchoErrAyyfueraBufferA, entoncesnoTiroA); // agrego consecuente y antecedente a la regla difusa

  fuzzyAcid->addFuzzyRule(fuzzyRule02); //agrego regla difusa al objeto fuzzy

  // regla difusa "Si error=muchoErrA AND sensibilidad=enBufferA  ENTONCES gotas = muchasA"
  FuzzyRuleAntecedent* SImuchoErrAyyenBufferA = new FuzzyRuleAntecedent(); // instancio antecedente
  SImuchoErrAyyenBufferA->joinWithAND(muchoErrA, enBufferA); // agrego conjuntos difusos al objeto antecedente
  FuzzyRuleConsequent* entoncesmuchasA = new FuzzyRuleConsequent(); // instancion consecuente
  entoncesmuchasA->addOutput(muchasA);// Agrego conjunto difuso al consecuente
  // Instantiating a FuzzyRule object
  FuzzyRule* fuzzyRule03 = new FuzzyRule(3, SImuchoErrAyyenBufferA, entoncesmuchasA); // agrego consecuente y antecedente a la regla difusa

  fuzzyAcid->addFuzzyRule(fuzzyRule03); //agrego regla difusa al objeto fuzzy

  // regla difusa "Si error=errorMedioA AND sensibilidad=enBufferA  ENTONCES gotas = mediasA"
  FuzzyRuleAntecedent* SIerrorMedioAyyenBufferA = new FuzzyRuleAntecedent(); // instancio antecedente
  SIerrorMedioAyyenBufferA->joinWithAND(errorMedioA, enBufferA); // agrego conjuntos difusos al objeto antecedente
  FuzzyRuleConsequent* entoncesintermediasA = new FuzzyRuleConsequent(); // instancion consecuente
  entoncesintermediasA->addOutput(intermediasA);// Agrego conjunto difuso al consecuente
  // Instantiating a FuzzyRule object
  FuzzyRule* fuzzyRule04 = new FuzzyRule(4, SIerrorMedioAyyenBufferA, entoncesintermediasA); // agrego consecuente y antecedente a la regla difusa

  fuzzyAcid->addFuzzyRule(fuzzyRule04); //agrego regla difusa al objeto fuzzy

  // regla difusa "Si error=sinErrorA AND sensibilidad=enBufferA  ENTONCES gotas = noTiroA"
  FuzzyRuleAntecedent* SIsinErrorAyyenBufferA = new FuzzyRuleAntecedent(); // instancio antecedente
  SIsinErrorAyyenBufferA->joinWithAND(sinErrorA, enBufferA); // agrego conjuntos difusos al objeto antecedente
  // FuzzyRuleConsequent* entoncesnoTiroA = new FuzzyRuleConsequent(); // instancion consecuente
  entoncesnoTiroA->addOutput(noTiroA);// Agrego conjunto difuso al consecuente
  // Instantiating a FuzzyRule object
  FuzzyRule* fuzzyRule05 = new FuzzyRule(5, SIsinErrorAyyenBufferA, entoncesnoTiroA); // agrego consecuente y antecedente a la regla difusa

  fuzzyAcid->addFuzzyRule(fuzzyRule05); //agrego regla difusa al objeto fuzzy

  // regla difusa "Si error=errorMedioA AND sensibilidad=fueraBufferA  ENTONCES gotas = noTiroA"
  // FuzzyRuleAntecedent* SIerrorMedioAyyfueraBufferA = new FuzzyRuleAntecedent(); // instancio antecedente
  SIerrorMedioAyyfueraBufferA->joinWithAND(errorMedioA, fueraBufferA); // agrego conjuntos difusos al objeto antecedente
  //FuzzyRuleConsequent* entoncesnoTiroA = new FuzzyRuleConsequent(); // instancion consecuente
  entoncesnoTiroA->addOutput(noTiroA);// Agrego conjunto difuso al consecuente
  // Instantiating a FuzzyRule object
  FuzzyRule* fuzzyRule06 = new FuzzyRule(6, SIerrorMedioAyyfueraBufferA, entoncesnoTiroA); // agrego consecuente y antecedente a la regla difusa

  fuzzyAcid->addFuzzyRule(fuzzyRule06); //agrego regla difusa al objeto fuzzy

  

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
  int got=0;
  double pHAhora = getTemperature();
  double err = (pHAhora - phObjetivo);
  double Aerr=abs(pHAhora - phObjetivo);
  if (inicio == 1 ) {
    sens = 0;
  }
  else {
    if(gotas>0){
    //sens = 17;
    sens = abs(1000*(pHAhora - pHanterior) / gotas);
    }
  }
  fuzzyAcid->setInput(1, Aerr);
  fuzzyAcid->setInput(2, sens);
  fuzzyAcid->fuzzify();
  gotas = fuzzyAcid->defuzzify(1);
  got= (int)(gotas+0.5);

  if (err > abs(zonaMuerta)) {
    setGotasHacido(got);
    totalGotas = totalGotas + got;
  }
  if(err < abs(zonaMuerta)*(-1)){
    setGotasBase(got);
    totalGotas = totalGotas + got;
  }
  inicio = 0;
  pHanterior=pHAhora;
  //Serial.println(gotas);
  //Serial.println(got);
  //Serial.println(sens);
  //Serial.println(5000-got*1000);
  //delay(1000);
  if(got*1000<7000){
    delay(7000-got*1000);
  }

}
