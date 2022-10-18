#include <Arduino.h>
#include <string.h>
#include <TimerOne.h>
const int led = 2;  // the pin with a LED
#include <OneWire.h> 
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 9 
OneWire oneWire(ONE_WIRE_BUS); 
DallasTemperature sensors(&oneWire);
const unsigned long baseDetiempo = 100;
int ledState = LOW;    // El LED empieza apagado
volatile unsigned long timer = 0; // La definimos como volatile
volatile unsigned long count = 1; // La definimos como volatile
//volatile unsigned long vel = 1;
volatile float velocity = 1.00;
int primerDato = 1;
#define RESPONSE_MAXLENGTH 20

char content[2];
int readVerification;
unsigned long sensorAddress;
char functionID[3];
unsigned long informationLength;
char receivedLRC[3];
char frameInformation[20];
char allFrameData[20];
char hexadecimalLRC[3];

int cuentaParaTiempo = 0;

int tiempoApagado = 20*60;
int tiempoEncendido = 20*60;

int tiempoApagadoMinimo = 5*60; // segundos
int tiempoApagadoMaximo = 40*60; // segundos
int tiempoPrendidoMinimo = 5*60; // segundos
int tiempoPrendidoMaximo = 35*60; // segundos
double temperaturaMinimo = 37.00; // en Celsius
double temperaturaMaximo = 55.00; // en Celsius
double temperaturaActual;
int tiempoActual; // segundos
int estadoActual = 0;
bool errorEnApagadoOccurred = false;
bool errorEnPrendidoOccurred = false;

String dataSend;
String sendingFrame;
String sendingFrameLRC;
int isDetected = 0;
int packageReceived = 0;
char dataToSend[20];
char sendingLRC[3];
char sendingCharArray[20];

int informationCount = 0;
char versionInfo[5] = "1.50"; 

void obtenerDatosTemperatura(){
  sensors.requestTemperatures();
  double temperaturaPosible = sensors.getTempCByIndex(0);
  if(temperaturaPosible<100 && temperaturaPosible>10){
    temperaturaActual = temperaturaPosible;
  }
}

void controlEstadoApagadoPorTemperaturaVentilador(){
  if(temperaturaActual < temperaturaMaximo && tiempoActual < tiempoApagadoMaximo && !(errorEnApagadoOccurred&&errorEnPrendidoOccurred)){
    digitalWrite(5, LOW);
  } else {
    if(temperaturaActual > temperaturaMaximo){
      errorEnApagadoOccurred = tiempoActual<tiempoApagadoMinimo;
      estadoActual = 1;
      encenderVentilador();
    } else {
      if((tiempoActual > tiempoApagadoMaximo)||(errorEnApagadoOccurred&&errorEnPrendidoOccurred)){
        estadoActual = 2;
        encenderVentilador();
      }
    }
  }
}

void controlEstadoPrendidoPorTemperaturaVentilador(){
  if(temperaturaActual > temperaturaMinimo && !(errorEnApagadoOccurred&&errorEnPrendidoOccurred)){
    digitalWrite(5, HIGH);
  } else {
    if(temperaturaActual <= temperaturaMinimo){
      errorEnPrendidoOccurred = tiempoActual<tiempoPrendidoMinimo;
      estadoActual = 0;
      apagarVentilador();
    } else {
      if(errorEnApagadoOccurred&&errorEnPrendidoOccurred){
        estadoActual = 2;
        encenderVentilador();
      }
    }
  }   
}

void controlEstadoPrendidoPorTiempoVentilador(){
  if(tiempoActual < tiempoEncendido){
    digitalWrite(5, HIGH);
  } else {
    if(temperaturaActual >= tiempoEncendido){
      estadoActual = 3;
      apagarVentilador();
    }
  }
}

void controlEstadoApagadoPorTiempoVentilador(){
  if(tiempoActual < tiempoApagado){
    digitalWrite(5, LOW);
  } else {
    if(tiempoActual >= tiempoApagado){
      estadoActual = 2;
      encenderVentilador();
    }
  }
}

void realizarControlVentilador(){
  if(estadoActual == 0){
    controlEstadoApagadoPorTemperaturaVentilador();
  } else {
    if(estadoActual == 1){
      controlEstadoPrendidoPorTemperaturaVentilador();
    } else {
      if(estadoActual == 2){
         controlEstadoPrendidoPorTiempoVentilador();
      } else {
        if(estadoActual == 3){
          controlEstadoApagadoPorTiempoVentilador();
        }
      }
    }
  }
}

void encenderVentilador(){
  digitalWrite(5, HIGH);
  tiempoActual = 0;
}

void apagarVentilador(){
  digitalWrite(5, LOW);
  tiempoActual = 0;
}

void incrementoTimer() { //incrementa timer en un tiempo Timer.initialize
  timer++;
  cuentaParaTiempo = cuentaParaTiempo + 1;
  if(cuentaParaTiempo==10000){
    tiempoActual = tiempoActual + 1;
    cuentaParaTiempo = 0;
  }
}  

void setup() {
  attachInterrupt(0, stopTimer, RISING);
  pinMode(led, OUTPUT); 
  pinMode(5, OUTPUT);
  digitalWrite(5, LOW);    
  //Timer1.initialize(baseDetiempo);         // Dispara cada 100 us
  //ALTERNATIVA: Timer1.initialize(1000);
  //Timer1.attachInterrupt(incrementoTimer); // Activa la interrupcion y la asocia a ISR_Blink
  Serial.begin(9600);
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
  //Serial.println(sendingCharArray);
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
  //Serial.println(sendingLRC);
  sendingFrame.concat(sendingFrameLRC);
  sendingFrame.concat(sendingLRC);
  //sendingFrame.concat('\r');
  //sendingFrame.concat('\n');
  
  /*ALTERNATIVE:
  sendingFrame = strcat("01",":");
  sendingFrame = strcat(sendingFrame, functionID);
  sendingFrame = strcat(sendingFrame, dataToSend);
  sendingFrame = strcat(sendingFrame, sendingLRC);
  sendingFrame = strcat(sendingFrame, '\r');
  sendingFrame = strcat(sendingFrame, '\n');
  */
  
  Serial.println(sendingFrame);
}

void stopTimer() { //inicializa timer y conserva cuenta anterior en count
  char velChar[6];
  String velString = "";
  count = timer;
  velocity = 600000.00/(count);
  //double velocity = ((int)((vel*100)+0.5))/100
  if(primerDato==0){
    if(velocity<0){
      //Serial.println("ERRORL");
    } else {
      if(velocity>1000){
        //Serial.println("ERRORM");
      } else {
        if(velocity<10){
          velString.concat("00");
          //sprintf (velChar, "%01c%01d%01c%01c%02d", '0', 2, '0', '0', velocidad);
        } else {
          if(velocity<100){
            velString.concat("0");
            //sprintf (velChar, "%01c%01d%01c%03d", '0', 3, '0', velocidad);
          }
        }
        velString.concat(velocity);
        velString.concat(temperaturaActual);
        velString.concat(estadoActual);
        Serial.println(velString);
        informationCount = informationCount + 1;
      }
    }  
  } else {
    primerDato = 0;
  }     
  timer = 0;
  digitalWrite(led, LOW);
}

void loop() {
  getModbusMessage();
  
  if(strcmp(functionID, "CN")==0 && packageReceived == 1){
    char statusInfo[3] = "OK";
    //sprintf (dataToSend, "%02c%03c", "01", statusInfo);
    
    dataSend = "01";
    dataSend.concat(statusInfo);
    sendModbusMessage();
    //Serial.println("CONNECTION");
    //Serial.println(dataSend);
    Serial.flush();
  }
  if(strcmp(functionID, "VS")==0 && packageReceived == 1){
    //dataToSend = strcat(&versionInfo[0], "02");
    //sprintf (dataToSend, "%02c%04c", "02", versionInfo);

    dataSend = "02";
    dataSend.concat(versionInfo);
    sendModbusMessage();
    //Serial.println("VERSION");
    //Serial.println(dataSend);
    Serial.flush();
  }
  if(strcmp(functionID, "DT")==0 && packageReceived == 1){

    //ALTERNATIVE:
    //dataToSend = strcat(&dataInfo[0], "02");
    //sprintf (dataToSend, "%02c%04c", "02", dataInfo);
    
    dataSend = "02";
    dataSend.concat("OK90");
    sendModbusMessage();

    //COMIENZA SENSADO
    //char dataInfo[7] = "000399";
    Timer1.initialize(baseDetiempo);
    Timer1.attachInterrupt(incrementoTimer);
    primerDato = 1;
    //Serial.println("DATA");
    while(informationCount<90){
      // REALIZA SENSADO
      digitalWrite(led, HIGH);
      //Serial.println(dataInfo);
      //informationCount++;
    }
    Timer1.detachInterrupt();
    Serial.flush();
    informationCount = 0;
    primerDato = 1;
    //TERMINA SENSADO
  }
  obtenerDatosTemperatura();
  realizarControlVentilador();
  packageReceived = 0;
  
  
}
