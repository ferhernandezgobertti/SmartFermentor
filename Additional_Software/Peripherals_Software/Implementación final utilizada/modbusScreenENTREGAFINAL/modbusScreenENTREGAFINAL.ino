#include <Arduino.h>
#include <MaxMatrix.h>
#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>

#define SCREEN1_DataIn  7   // DIN pin - SCREEN 1
#define SCREEN1_Clock   6   // CLK pin - SCREEN 1 - SCREEN 2
#define SCREEN1_Counter 5   // CS pin - SCREEN 1
#define SCREEN2_DataIn  8   // DIN pin - SCREEN 2
#define SCREEN2_Counter 9   // CS pin - SCREEN 2
#define SCREENINFO_DataIn  11
#define SCREENINFO_Clock   13
#define SCREENINFO_Counter 10

#define VELOCITY_IDENTIFIER 1
#define TEMPERATURE_IDENTIFIER 2
#define POTENTIAL_HYDROGEN_IDENTIFIER 3
#define INITIAL_ANIMATION_DELAY 10
#define MAGNITUDES_ANIMATION_DELAY 250
#define ERRORS_AND_UNITS_ANIMATION_DELAY 300
#define BUF_SIZE  75
#define SERIAL_BAUD 19200
#define HOME_PAGE_IDENTIFIER 1
#define USER_PAGE_IDENTIFIER 2
#define FERMENTATION_PAGE_IDENTIFIER 5
#define CONTROLS_RUNNING_IDENTIFIER 6

MaxMatrix matrix1 (SCREEN1_DataIn, SCREEN1_Counter, SCREEN1_Clock, 1); 
MaxMatrix matrix2 (SCREEN2_DataIn, SCREEN2_Counter, SCREEN1_Clock, 1); 
MD_Parola matrixInfo = MD_Parola(SCREENINFO_DataIn, SCREENINFO_Clock, SCREENINFO_Counter, 4);

bool newMessageAvailable = true;
char content[10];
char curMessage[BUF_SIZE] = { "" };
char newMessage[BUF_SIZE] = { "" };
char velocityString[8];
char temperatureString[8];
char potentialString[8];
double velocityValue = 0.0 ;
double temperatureValue = 0.0;
double potentialValue = 0.0;
double temperaturePrevious, potentialPrevious;
int readVerification;
int pageStatus, errorStatus, controlStatus;
int packageReceived = 0;
int magnitudeSelected = 1;
int magnitudeChanged = 1;
int messageToScroll = 0;
int firstTime = 1;
int countInitialAnimation = 0;
int newMessageReceived = 1;
int controlsRunning[] = {0, 0, 0, 0};
int velocityError[] = {0, 0};
int temperatureError[] = {0, 0};
int potentialError = 0;
int velocityCustomization[] = {0, 0, 0};
int temperatureCustomization[] = {0, 0};
int potentialCustomization[] = {0, 0};
String allFrameData;
textEffect_t scrollEffect = PA_SCROLL_LEFT;
textPosition_t scrollAlign = PA_LEFT;
uint8_t scrollSpeed = 10;    // default frame delay value
uint16_t scrollPause = 100; // in milliseconds

// INFORMATION: PERIPHERALS IDENTIFIERS
byte crossError[] = {8, 8, B11000011,B11100111,B01111110,B00111100,B00111100,B01111110,B11100111,B11000011};
byte motorIdentifier[] = {8, 8, B11000011,B11100111,B10111101,B10011001,B10000001,B10000001,B10000001,B10000001};
byte bathIdentifier[] = {8, 8, B01111100,B01000010,B01000010,B01111100,B01000010,B01000010,B01000010,B01111100};
byte sensorIdentifier[] = {8, 8, B00011100,B00100010,B00100000,B00011100,B00000010,B00000010,B00100010,B00011100};
byte arduinoIdentifier[] = {8, 8, B01111110,B11111111,B10000001,B11000011,B11111111,B11111111,B11000011,B11000011};

// INFORMATION: MAGNITUDES IDENTIFIERS
byte potentialHydrogenStill[] = {8, 8, B00001001,B00001001,B00001001,B11101111,B10101111,B11101001,B10001001,B10001001};
byte potentialHydrogenWaiting[] = {8, 8, B00000000,B00000000,B00000000,B00000000,B11101001,B10101001,B11101111,B10001001};
byte temperatureStill[] = {8, 8, B01111110,B11111111,B10011001,B00011000,B00011000,B00011000,B00011000,B00011000}; 
byte temperatureWaiting[] = {8, 8, B00000000,B00000000,B00000000,B00000000,B01111110,B01011010,B00011000,B00011000};
byte velocityStill[] = {8, 8, B11000011,B11000011,B01000010,B01100110,B01100110,B00100100,B00111100,B00011000};

// INFORMATION: UNITS IDENTIFIERS
byte mililiterUnit[] = {8, 8, B00000010,B00000010,B00000010,B00000010,B11111010,B11111010,B10101011,B10101011};
byte revolutionsPerMinuteUnit1[] = {8, 8, B11111110,B11111110,B11000110,B11000110,B11111100,B11111100,B11001110,B11000111};
byte revolutionsPerMinuteUnit2[] = {8, 8, B11111111,B11111111,B11000011,B11000011,B11111111,B11111110,B11000000,B11000000};
byte revolutionsPerMinuteUnit3[] = {8, 8, B11000011,B11100111,B10111101,B10011001,B10000001,B10000001,B10000001,B10000001};
byte celsiusGrad[] = {8, 8, B11001110,B11011111,B00010011,B00110000,B00110000,B00110011,B00011111,B00001110};
byte noDimensionUnit[] = {8, 8, B00000000,B00000000,B00000000,B01111110,B01111110,B00000000,B00000000,B00000000};

// ANIMATION 01: Scrolling Horizontal Bars
byte screenLine1Horizontal[] = {8, 8, B00000000,B00000000,B00000000,B00000000,B00000000,B00000000,B00000000,B11111111}; // Most Down
byte screenLine2Horizontal[] = {8, 8, B00000000,B00000000,B00000000,B00000000,B00000000,B00000000,B11111111,B00000000};
byte screenLine3Horizontal[] = {8, 8, B00000000,B00000000,B00000000,B00000000,B00000000,B11111111,B00000000,B00000000};
byte screenLine4Horizontal[] = {8, 8, B00000000,B00000000,B00000000,B00000000,B11111111,B00000000,B00000000,B00000000};
byte screenLine5Horizontal[] = {8, 8, B00000000,B00000000,B00000000,B11111111,B00000000,B00000000,B00000000,B00000000};
byte screenLine6Horizontal[] = {8, 8, B00000000,B00000000,B11111111,B00000000,B00000000,B00000000,B00000000,B00000000};
byte screenLine7Horizontal[] = {8, 8, B00000000,B11111111,B00000000,B00000000,B00000000,B00000000,B00000000,B00000000};
byte screenLine8Horizontal[] = {8, 8, B11111111,B00000000,B00000000,B00000000,B00000000,B00000000,B00000000,B00000000}; // Most Up

// ANIMATION 02: Scrolling Vertical Bars
byte screenLine1Vertical[] = {8, 8, B00000001,B00000001,B00000001,B00000001,B00000001,B00000001,B00000001,B00000001}; // Most Right
byte screenLine2Vertical[] = {8, 8, B00000010,B00000010,B00000010,B00000010,B00000010,B00000010,B00000010,B00000010};
byte screenLine3Vertical[] = {8, 8, B00000100,B00000100,B00000100,B00000100,B00000100,B00000100,B00000100,B00000100};
byte screenLine4Vertical[] = {8, 8, B00001000,B00001000,B00001000,B00001000,B00001000,B00001000,B00001000,B00001000};
byte screenLine5Vertical[] = {8, 8, B00010000,B00010000,B00010000,B00010000,B00010000,B00010000,B00010000,B00010000};
byte screenLine6Vertical[] = {8, 8, B00100000,B00100000,B00100000,B00100000,B00100000,B00100000,B00100000,B00100000};
byte screenLine7Vertical[] = {8, 8, B01000000,B01000000,B01000000,B01000000,B01000000,B01000000,B01000000,B01000000};
byte screenLine8Vertical[] = {8, 8, B10000000,B10000000,B10000000,B10000000,B10000000,B10000000,B10000000,B10000000}; // Most Left

// ANIMATION 03: pH Increase / Decrease
byte potentialIncreasing1[] = {8, 8, B00000000,B00000000,B00011000,B00000000,B11101001,B10101001,B11101111,B10001001};
byte potentialIncreasing2[] = {8, 8, B00000000,B00011000,B00111100,B00000000,B11101001,B10101001,B11101111,B10001001};
byte potentialIncreasing3[] = {8, 8, B00011000,B00111100,B01100110,B00000000,B11101001,B10101001,B11101111,B10001001};
byte potentialDecreasing1[] = {8, 8, B00011000,B00000000,B00000000,B00000000,B11101001,B10101001,B11101111,B10001001};
byte potentialDecreasing2[] = {8, 8, B00111100,B00011000,B00000000,B00000000,B11101001,B10101001,B11101111,B10001001};
byte potentialDecreasing3[] = {8, 8, B01100110,B00111100,B00011000,B00000000,B11101001,B10101001,B11101111,B10001001};

// ANIMATION 04: Temperature Increase / Decrease
byte temperatureIncreasing1[] = {8, 8, B00000000,B00000000,B00011000,B00000000,B01111110,B01011010,B00011000,B00011000};
byte temperatureIncreasing2[] = {8, 8, B00000000,B00011000,B00111100,B00000000,B01111110,B01011010,B00011000,B00011000};
byte temperatureIncreasing3[] = {8, 8, B00011000,B00111100,B01100110,B00000000,B01111110,B01011010,B00011000,B00011000};
byte temperatureDecreasing1[] = {8, 8, B00011000,B00000000,B00000000,B00000000,B01111110,B01011010,B00011000,B00011000};
byte temperatureDecreasing2[] = {8, 8, B00111100,B00011000,B00000000,B00000000,B01111110,B01011010,B00011000,B00011000};
byte temperatureDecreasing3[] = {8, 8, B01100110,B00111100,B00011000,B00000000,B01111110,B01011010,B00011000,B00011000};

// ANIMATION 05: Velocity Control Activated
byte arrowClockwiseDown[] = {8, 8, B00001111,B00000001,B00000001,B00001101,B00011001,B00110111,B00011000,B00001100};
byte arrowClockwiseLeft[] = {8, 8, B00000000,B00000000,B00100000,B01110001,B11011001,B10101001,B00100001,B00111111};
byte arrowClockwiseUp[] = {8, 8, B00110000,B00011000,B11101100,B10011000,B10110000,B10000000,B10000000,B11111000};
byte arrowClockwiseRight[] = {8, 8, B11111100,B10000100,B10010101,B10011011,B10001110,B00000100,B00000000,B00000000};
byte arrowAntiClockwiseUp[] = {8, 8, B00000000,B00000000,B00000100,B00001110,B10011011,B10010101,B10000100,B11111100};
byte arrowAntiClockwiseLeft[] = {8, 8, B00001100,B00011000,B00110111,B00011001,B00001101,B00000001,B00000001,B00001111};
byte arrowAntiClockwiseDown[] = {8, 8, B00111111,B00100001,B10101001,B11011001,B01110000,B00100000,B00000000,B00000000};
byte arrowAntiClockwiseRight[] = {8, 8, B11110000,B10000000,B10000000,B10110000,B10011000,B11101100,B00011000,B00110000};
byte fanPosition1[] = {8, 8, B00011000,B00011000,B00011000,B00011000,B00111100,B01111110,B11100111,B11000011};
byte fanPosition2[] = {8, 8, B11000000,B11100000,B01110000,B00111111,B00111111,B01110000,B11100000,B11000000};
byte fanPosition3[] = {8, 8, B11000011,B11100111,B01111110,B00111100,B00011000,B00011000,B00011000,B00011000};
byte fanPosition4[] =  {8, 8, B00000011,B00000111,B00001110,B11111100,B11111100,B00001110,B00000111,B00000011};

// ANIMATION 06: Units of pH
byte metersPerSecondUnit1[] = {8, 8, B00000000,B00000000,B01000000,B01111110,B00111110,B00101010,B00101010,B00000000};
byte metersPerSecondUnit2[] = {8, 8, B00000000,B00000110,B00001110,B00011100,B00111000,B01110000,B01100000,B00000000};
byte metersPerSecondUnit3[] = {8, 8, B00000000,B00111100,B00100100,B00100000,B00011100,B00000100,B00100100,B00111000};
byte radiansPerSecondUnit1[] = {8, 8, B00000000,B01111000,B01000100,B01000100,B01111000,B01001000,B01001100,B00000000};
byte radiansPerSecondUnit2[] = {8, 8, B00000000,B00111100,B01000010,B01000010,B01111110,B01000010,B01000010,B00000000};
byte radiansPerSecondUnit3[] = {8, 8, B00000000,B01111100,B01000010,B01000010,B01000010,B01000010,B01111100,B00000000};
byte kelvinsGrad[] = {8, 8, B00000000,B01000100,B01001000,B01110000,B01110000,B01001000,B01000100,B00000000};
byte fahrenheitGrad[] = {8, 8, B11000000,B11000000,B00011110,B00010000,B00010000,B00011100,B00010000,B00010000};

void checkControlsRunning(){
  if((controlStatus & 0x0002) != 0){ //Potential Control Running
    controlsRunning[2] = 1;
  }
  if((controlStatus & 0x0004) != 0){ //Temperature Control Running
    controlsRunning[1] = 1;
  }
  if((controlStatus & 0x0008) != 0){ //Velocity Control Running
    controlsRunning[0] = 1;
  }
}

void checkControlsConfiguration(){
  if((controlStatus & 0x0010) != 0){ //Velocity Control on Nominal
    velocityCustomization[1] = 0;
  }
  if((controlStatus & 0x0020) != 0){ //Velocity Control on Slow
    velocityCustomization[1] = 1;
  }
  if((controlStatus & 0x0030) != 0){ //Velocity Control on Very Slow
    velocityCustomization[1] = 2;
  }
  if((controlStatus & 0x0040) != 0){ //Temperature Control on Nominal
    temperatureCustomization[1] = 0;
  }
  if((controlStatus & 0x0080) != 0){ //Temperature Control on Fast
    temperatureCustomization[1] = 1;
  }
  if((controlStatus & 0x00c0) != 0){ //Temperature Control on Very Fast
    temperatureCustomization[1] = 2;
  }
  if((controlStatus & 0x0000) != 0){ //Potential Control with Burst Mode 1 (Nominal)
    potentialCustomization[1] = 0;
  }
  if((controlStatus & 0x0100) != 0){ //Potential Control with Burst Mode 2
    potentialCustomization[1] = 1;
  }
  if((controlStatus & 0x0000) != 0){ //Velocity Orientation Clockwise
    velocityCustomization[2] = 0;
  }
  if((controlStatus & 0x0100) != 0){ //Velocity Orientation AntiClockwise
    velocityCustomization[2] = 1;
  }
}

void checkControlsUnit(){
  if((controlStatus & 0x0200) != 0){ //Velocity Magnitude Unit rpm
    velocityCustomization[0] = 0;
  }
  if((controlStatus & 0x0400) != 0){ //Velocity Magnitude Unit m/s
    velocityCustomization[0] = 1;
  }
  if((controlStatus & 0x0800) != 0){ //Velocity Magnitude Unit Rad/s
    velocityCustomization[0] = 2;
  }
  
  if((controlStatus & 0x0000) != 0){ //Temperature Magnitude Unit Celsius
    temperatureCustomization[0] = 0;
  }
  if((controlStatus & 0x2000) != 0){ //Temperature Magnitude Unit Kelvin
    temperatureCustomization[0] = 1;
  }
  if((controlStatus & 0x4000) != 0){ //Temperature Magnitude Unit Fahrenheit
    temperatureCustomization[0] = 2;
  }
}

void configureControlCustomizationData(){
  controlsRunning[0] = 0;
  controlsRunning[1] = 0;
  controlsRunning[2] = 0;
  controlsRunning[3] = 0;
  velocityCustomization[0] = 0;
  velocityCustomization[1] = 0;
  velocityCustomization[2] = 0;
  temperatureCustomization[0] = 0;
  temperatureCustomization[1] = 0;
  potentialCustomization[0] = 0;
  potentialCustomization[1] = 0;
  
  checkControlsRunning();
  checkControlsConfiguration();
  checkControlsUnit();
}

void checkVelocityControlError(){
  if((errorStatus & 0x0001) == 1){ //Motor Connection Error
    velocityError[0] = 0;
    velocityError[1] = 1;
  }
  if((errorStatus & 0x0002) == 2){ //Motor Data Error
    velocityError[0] = 0;
    velocityError[1] = 2;
  }
  if((errorStatus & 0x0003) == 3){ //Velocity Arduino Connection Error
    velocityError[0] = 1;
    velocityError[1] = 0;
  }
  if((errorStatus & 0x0004) == 4){ //Velocity Arduino Data Error
    velocityError[0] = 2;
    velocityError[1] = 0;
  }
}

void checkTemperatureControlError(){
  if((errorStatus & 0x0008) == 8){ //Bath Connection Error
    temperatureError[0] = 1;
    temperatureError[1] = 0;
  }
  if((errorStatus & 0x0010) == 16){ //Bath Data Error
    temperatureError[0] = 2;
    temperatureError[1] = 0;
  }
  if((errorStatus & 0x0020) == 32){ //Temperature Arduino Connection Error
    temperatureError[0] = 0;
    temperatureError[1] = 1;
  }
  if((errorStatus & 0x0040) == 64){ //Temperature Arduino Data Error
    temperatureError[0] = 0;
    temperatureError[1] = 2;
  }
}

void checkPotentialHydrogenControlError(){
  if((errorStatus & 0x0080) == 128){ //Potential Arduino Connection Error
    potentialError = 1;
  }
  if((errorStatus & 0x0100) == 256){ //Potential Arduino Data Error
    potentialError = 2;
    //Serial.println("PDATA");
  }
}

void configureControlErrorData(){
  //Serial.println("ENTRO A configureControlErrorData");
  velocityError[0] = 0;
  velocityError[1] = 0;;
  temperatureError[0] = 0;
  temperatureError[1] = 0;
  potentialError = 0;
  checkVelocityControlError();
  checkTemperatureControlError();
  checkPotentialHydrogenControlError();
}

void configureMagnitudesData(){
  configureControlCustomizationData();
  configureControlErrorData();
}

int StrToHex(char str[]) {
  return (int) strtol(str, 0, 16);
}

void getProtocolMessage(){
  allFrameData = "";
  byte syncByte = Serial.read();
  if(syncByte == 'X'){
    readVerification = Serial.readBytes(content, 1);
    if(readVerification==1){
      allFrameData.concat(content[0]);
      pageStatus = strtoul( content, NULL, 10 );
      readVerification = Serial.readBytes(content, 4);
      if(readVerification==4){
        allFrameData.concat(content[0]);
        allFrameData.concat(content[1]);
        allFrameData.concat(content[2]);
        allFrameData.concat(content[3]);
        errorStatus = StrToHex(content); 
        //Serial.println(errorStatus); //(int)(content[0]-48)*10+(int)(content[1]-48)*1;
        readVerification = Serial.readBytes(content, 4);
        if(readVerification==4){
          allFrameData.concat(content[0]);
          allFrameData.concat(content[1]);
          allFrameData.concat(content[2]);
          allFrameData.concat(content[3]);
          controlStatus = StrToHex(content); //(int)(content[0]-48)*10+(int)(content[1]-48)*1;
          readVerification = Serial.readBytes(content, 4);
          if(readVerification==4){
            allFrameData.concat(content[0]);
            allFrameData.concat(content[1]);
            allFrameData.concat(content[2]);
            allFrameData.concat(content[3]);
            velocityString[0] = ' ';
            velocityString[1] = content[0];
            velocityString[2] = content[1];
            velocityString[3] = content[2];
            velocityString[4] = '.';
            velocityString[5] = content[3];
            velocityValue = (int)( content[0]-48)*100+(int)( content[1]-48)*10+(int)(content[2]-48)*1+(int)(content[3]-48)*0.1;
            readVerification = Serial.readBytes(content, 4);
            if(readVerification==4){
              allFrameData.concat(content[0]);
              allFrameData.concat(content[1]);
              allFrameData.concat(content[2]);
              allFrameData.concat(content[3]);
              temperatureString[0] = ' ';
              temperatureString[1] = content[0];
              temperatureString[2] = content[1];
              temperatureString[3] = '.';
              temperatureString[4] = content[2];
              temperatureString[5] = content[3];
              temperatureValue = (int)( content[0]-48)*10+(int)( content[1]-48)*1+(int)(content[2]-48)*0.1+(int)(content[3]-48)*0.01; //(strtoul( content, NULL, 10 ))/100;
              readVerification = Serial.readBytes(content, 5);
              if(readVerification==5){
                allFrameData.concat(content[0]);
                allFrameData.concat(content[1]);
                allFrameData.concat(content[2]);
                allFrameData.concat(content[3]);
                allFrameData.concat(content[4]);
                potentialString[0] = content[0];
                potentialString[1] = content[1];
                potentialString[2] = '.';
                potentialString[3] = content[2];
                potentialString[4] = content[3];
                potentialString[5] = content[4];
                potentialValue = (int)( content[0]-48)*10+(int)( content[1]-48)*1+(int)(content[2]-48)*0.1+(int)(content[3]-48)*0.01+(int)(content[4]-48)*0.001;
                readVerification = Serial.readBytes(content, 4);
                if(readVerification==4){
                  allFrameData.concat(content[0]);
                  allFrameData.concat(content[1]);
                  allFrameData.concat(content[2]);
                  allFrameData.concat(content[3]);
                  readVerification = Serial.readBytes(content, 8);
                  if(readVerification==8){
                    String receivedCRC = "";
                    receivedCRC.concat(content[0]);
                    receivedCRC.concat(content[1]);
                    receivedCRC.concat(content[2]);
                    receivedCRC.concat(content[3]);
                    receivedCRC.concat(content[4]);
                    receivedCRC.concat(content[5]);
                    receivedCRC.concat(content[6]);
                    receivedCRC.concat(content[7]);
                    char frameData[23];
                    allFrameData.toCharArray(frameData, 23);
                    String crcString = String(crc32b(frameData), HEX);
                    readVerification = Serial.readBytes(content, 2);
                    if(content[0]=='\r' && content[1]=='\n'){
                      configureMagnitudesData();
                      packageReceived = 1;
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

uint16_t crc16_update(uint16_t crc, uint8_t a) { //Optimization CCITT
  int i; 
  crc ^= a;
  for (i = 0; i < 8; ++i) {
   if (crc & 1)
     crc = (crc >> 1) ^ 0xA001;
   else
     crc = (crc >> 1);
   } 
   return crc;
}

unsigned long crc32b(unsigned char *message) {
   int i, j;
   unsigned long Byte, crc, mask;

   i = 0;
   crc = 0xFFFFFFFF;
   while (message[i] != 0) {
      Byte = message[i];            // Get next byte.
      crc = crc ^ Byte;
      for (j = 7; j >= 0; j--) {    // Do eight times.
         mask = -(crc & 1);
         crc = (crc >> 1) ^ (0xEDB88320 & mask);
      }
      i = i + 1;
   }
   return ~crc;
}


void setArrowsAnimation () {
  int countAnimation = 0;
  //matrix2.clear();
  while(countAnimation<2){
    if(velocityCustomization[2]==0) { //Clockwise
      //matrix2.writeSprite(0, 0, arrowClockwiseDown);
      delay(125);
      //matrix2.clear();
      //matrix2.writeSprite(0, 0, arrowClockwiseLeft);
      delay(125);
      //matrix2.clear();
      //matrix2.writeSprite(0, 0, arrowClockwiseUp);
      delay(125);
      //matrix2.clear();
      //matrix2.writeSprite(0, 0, arrowClockwiseRight);
      delay(125);
      //matrix2.clear();
    } 
    if(velocityCustomization[2]==1) { //AntiClockwise
      //matrix2.writeSprite(0, 0, arrowAntiClockwiseDown);
      delay(125);
      //matrix2.clear();
      //matrix2.writeSprite(0, 0, arrowAntiClockwiseRight);
      delay(125);
      //matrix2.clear();
      //matrix2.writeSprite(0, 0, arrowAntiClockwiseUp);
      delay(125);
      //matrix2.clear();
      //matrix2.writeSprite(0, 0, arrowAntiClockwiseLeft);
      delay(125);
      //matrix2.clear();
    }
    countAnimation = countAnimation + 1;
  }
  setMagnitudeUnit(1);
}

void setVelocityAnimation () {
  int countAnimation = 0;
  int arrowsCount = 0;
  while(countAnimation<10){
    if(velocityCustomization[2]==0) { //Clockwise
      matrix1.writeSprite(0, 0, fanPosition1);
      if(arrowsCount==3){
        matrix2.clear();
        matrix2.writeSprite(0, 0, arrowClockwiseRight);
        arrowsCount = arrowsCount + 1;
      }
      if(arrowsCount==7){
        matrix2.clear();
        setLetterOfVelocityUnit(3);
        arrowsCount = 0;
      }
      delay(50);
      matrix1.clear();
      matrix1.writeSprite(0, 0, fanPosition2);
      if(arrowsCount==2){
        matrix2.clear();
        matrix2.writeSprite(0, 0, arrowClockwiseUp);
        arrowsCount = arrowsCount + 1;
      }
      if(arrowsCount==6){
        matrix2.clear();
        setLetterOfVelocityUnit(2);
        arrowsCount = arrowsCount + 1;
      }
      delay(50);
      matrix1.clear();
      matrix1.writeSprite(0, 0, fanPosition3);
      if(arrowsCount==1){
        matrix2.clear();
        matrix2.writeSprite(0, 0, arrowClockwiseLeft);
        arrowsCount = arrowsCount + 1;
      }
      if(arrowsCount==5){
        matrix2.clear();
        setLetterOfVelocityUnit(1);
        arrowsCount = arrowsCount + 1;
      }
      delay(50);
      matrix1.clear();
      matrix1.writeSprite(0, 0, fanPosition4);
      if(arrowsCount==0 || arrowsCount==4){
        matrix2.clear();
        matrix2.writeSprite(0, 0, arrowClockwiseDown);
        arrowsCount = arrowsCount + 1;
      }
      delay(50);
      matrix1.clear();
      
    }
    if(velocityCustomization[2]==1) { //AntiClockwise
      matrix1.writeSprite(0, 0, fanPosition1);
      if(arrowsCount==3){
        matrix2.clear();
        matrix2.writeSprite(0, 0, arrowAntiClockwiseLeft);
        arrowsCount = 0;
      }
      if(arrowsCount==7){
        matrix2.clear();
        setLetterOfVelocityUnit(3);
        arrowsCount = 0;
      }
      delay(50);
      matrix1.clear();
      matrix1.writeSprite(0, 0, fanPosition4);
      if(arrowsCount==2){
        matrix2.clear();
        matrix2.writeSprite(0, 0, arrowAntiClockwiseUp);
        arrowsCount = arrowsCount + 1;
      }
      if(arrowsCount==6){
        matrix2.clear();
        setLetterOfVelocityUnit(2);
        arrowsCount = arrowsCount + 1;
      }
      delay(50);
      matrix1.clear();
      matrix1.writeSprite(0, 0, fanPosition3);
      if(arrowsCount==1){
        matrix2.clear();
        matrix2.writeSprite(0, 0, arrowAntiClockwiseRight);
        arrowsCount = arrowsCount + 1;
      }
      if(arrowsCount==5){
        //matrix2.clear();
        setLetterOfVelocityUnit(1);
        arrowsCount = arrowsCount + 1;
      }
      delay(50);
      matrix1.clear();
      matrix1.writeSprite(0, 0, fanPosition2);
      if(arrowsCount==0 || arrowsCount==4){
        matrix2.clear();
        matrix2.writeSprite(0, 0, arrowAntiClockwiseDown);
        arrowsCount = arrowsCount + 1;
      }
      delay(50);
      matrix1.clear();
    }
    countAnimation = countAnimation + 1;
  }
}

void setTemperatureAnimation (int currentStatus) {
  matrix1.clear();
  if(currentStatus==0) { //Increasing
    matrix1.writeSprite(0, 0, temperatureWaiting);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, temperatureIncreasing1);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, temperatureIncreasing2);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, temperatureIncreasing3);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
  }
  if(currentStatus==1) { //Decreasing
    matrix1.writeSprite(0, 0, temperatureWaiting);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, temperatureDecreasing1);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, temperatureDecreasing2);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, temperatureDecreasing3);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
  }
}

void setPotentialHydrogenAnimation (int currentStatus) {
  matrix1.clear();
  if(currentStatus==0) { //Increasing
    matrix1.writeSprite(0, 0, potentialHydrogenWaiting);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, potentialIncreasing1);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, potentialIncreasing2);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, potentialIncreasing3);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
  }
  if(currentStatus==1) { //Decreasing
    matrix1.writeSprite(0, 0, potentialHydrogenWaiting);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, potentialDecreasing1);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, potentialDecreasing2);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
    matrix1.writeSprite(0, 0, potentialDecreasing3);
    delay(MAGNITUDES_ANIMATION_DELAY);
    matrix1.clear();
  }
}

void setMagnitudeIdentifier(int magnitude){
  if(magnitude == VELOCITY_IDENTIFIER){
    matrix1.writeSprite(0, 0, velocityStill);
  }
  if(magnitude == TEMPERATURE_IDENTIFIER){
    matrix1.writeSprite(0, 0, temperatureStill);
  }
  if(magnitude == POTENTIAL_HYDROGEN_IDENTIFIER){
    matrix1.writeSprite(0, 0, potentialHydrogenStill);
  }
}

void setErrorAnimation(int errorIdentifier){
  int countAnimation = 0;
  while(countAnimation<2){
    if(errorIdentifier==1) { // Motor ERROR
      matrix2.clear();
      matrix2.writeSprite(0, 0, crossError);
      delay(ERRORS_AND_UNITS_ANIMATION_DELAY);
      matrix2.clear();
      matrix2.writeSprite(0, 0, motorIdentifier);
      delay(700);
    }
    if(errorIdentifier==2) { // Bath ERROR
      matrix2.clear();
      matrix2.writeSprite(0, 0, crossError);
      delay(ERRORS_AND_UNITS_ANIMATION_DELAY);
      matrix2.clear();
      matrix2.writeSprite(0, 0, bathIdentifier);
      delay(700);
    }
    if(errorIdentifier==3) { // Sensor ERROR
      matrix2.clear();
      matrix2.writeSprite(0, 0, crossError);
      delay(ERRORS_AND_UNITS_ANIMATION_DELAY);
      matrix2.clear();
      matrix2.writeSprite(0, 0, sensorIdentifier);
      delay(700);
    }
    if(errorIdentifier==4) { // Arduino ERROR
      matrix2.clear();
      matrix2.writeSprite(0, 0, crossError);
      delay(ERRORS_AND_UNITS_ANIMATION_DELAY);
      matrix2.clear();
      matrix2.writeSprite(0, 0, arduinoIdentifier);
      delay(700);
    }
    countAnimation = countAnimation + 1;
  }
}

void setLetterOfVelocityUnit(int letterPosition){
  if(velocityCustomization[0]==0){
    if(letterPosition==1){
      matrix2.writeSprite(0, 0, revolutionsPerMinuteUnit1);
    }
    if(letterPosition==2){
      matrix2.writeSprite(0, 0, revolutionsPerMinuteUnit2);
    }
    if(letterPosition==3){
      matrix2.writeSprite(0, 0, revolutionsPerMinuteUnit3);
    }
  }
  if(velocityCustomization[0]==1){
    if(letterPosition==1){
      matrix2.writeSprite(0, 0, metersPerSecondUnit1);
    }
    if(letterPosition==2){
      matrix2.writeSprite(0, 0, metersPerSecondUnit2);
    }
    if(letterPosition==3){
      matrix2.writeSprite(0, 0, metersPerSecondUnit3);
    }
  }
  if(velocityCustomization[0]==2){
    if(letterPosition==1){
      matrix2.writeSprite(0, 0, radiansPerSecondUnit1);
    }
    if(letterPosition==2){
      matrix2.writeSprite(0, 0, radiansPerSecondUnit2);
    }
    if(letterPosition==3){
      matrix2.writeSprite(0, 0, radiansPerSecondUnit3);
    }
  }
  delay(ERRORS_AND_UNITS_ANIMATION_DELAY);
}

void setTemperatureUnit(){
  if(temperatureCustomization[0]==0){
    matrix2.writeSprite(0, 0, celsiusGrad);
  }
  if(temperatureCustomization[0]==1){
    matrix2.writeSprite(0, 0, kelvinsGrad);
  }
  if(temperatureCustomization[0]==2){
    matrix2.writeSprite(0, 0, fahrenheitGrad);
  }
}

void setMagnitudeUnit(int magnitudeIdentifier){
  if(magnitudeIdentifier==VELOCITY_IDENTIFIER){
    matrix2.clear();
    setLetterOfVelocityUnit(1);
    delay(ERRORS_AND_UNITS_ANIMATION_DELAY);
    matrix2.clear();
    setLetterOfVelocityUnit(2);
    delay(ERRORS_AND_UNITS_ANIMATION_DELAY);
    matrix2.clear();
    setLetterOfVelocityUnit(3);
    delay(ERRORS_AND_UNITS_ANIMATION_DELAY);
    matrix2.clear();
    delay(100);
  }
  if(magnitudeIdentifier==TEMPERATURE_IDENTIFIER){
    matrix2.clear();
    setTemperatureUnit();
    delay(2000);
    
  }
  if(magnitudeIdentifier==0 or magnitudeIdentifier==POTENTIAL_HYDROGEN_IDENTIFIER){
    matrix2.clear();
    //matrix2.writeSprite(0, 0, noDimensionUnit);
    delay(2000);
  }
}

void setMagnitudeInitialStatus(int magnitudeIdentifier){
  setMagnitudeIdentifier(magnitudeIdentifier);
  
  if(magnitudeIdentifier == VELOCITY_IDENTIFIER){
    if(controlsRunning[0]==0){ // NO CONTROL
      setMagnitudeUnit(0);
    } else {
      if(velocityError[0] == 0 && velocityError[1]==0){ // NO ERROR
        //setArrowsAnimation();
      }
      if(velocityError[0] == 1 || velocityError[0] == 2){ // Motor ERROR
        setErrorAnimation(1);
      }
      if(velocityError[1] == 1){ // Sensor ERROR
        setErrorAnimation(3);
      }
      if(velocityError[1] == 2){ // Arduino ERROR
        setErrorAnimation(4);
      }
    }
  }
  if(magnitudeIdentifier == TEMPERATURE_IDENTIFIER){
    if(controlsRunning[1]==0){ // NO CONTROL
      setMagnitudeUnit(0);
    } else {
      if(temperatureError[0] == 0 && temperatureError[1]==0){ // NO ERROR
        setMagnitudeUnit(magnitudeIdentifier);
      }
      if(temperatureError[0] == 1 || temperatureError[0] == 2){ // Bath ERROR
        setErrorAnimation(2);
      }
      if(temperatureError[1] == 1){ // Sensor ERROR
        setErrorAnimation(3);
      }
      if(temperatureError[1] == 2){ // Arduino ERROR
        setErrorAnimation(4);
      }
    }
  }
  if(magnitudeIdentifier == POTENTIAL_HYDROGEN_IDENTIFIER){
    if(controlsRunning[2]==0){ // NO CONTROL
      setMagnitudeUnit(0);
    } else {
      if(potentialError == 0){ // NO ERROR
        //matrix2.clear();
      }
      if(potentialError == 1){ // Sensor ERROR
        setErrorAnimation(3);
      }
      if(potentialError == 2){ // Arduino ERROR
        setErrorAnimation(4);
      }
    }
  }
}

void setMagnitudeInformation(int magnitudeIdentifier){
  if(magnitudeIdentifier == VELOCITY_IDENTIFIER && controlsRunning[0]==1){
    if(velocityError[0] == 0 && velocityError[1]==0){
      setVelocityAnimation();
    } else {
      //matrix2.clear();
      //matrix2.writeSprite(0, 0, crossError);
      delay(2000);
    }
  }
  if(magnitudeIdentifier == TEMPERATURE_IDENTIFIER && controlsRunning[1]==1){
    if(temperatureError[0] == 0 && temperatureError[1]==0){
      //matrix2.clear();
      setTemperatureUnit();
      if(temperaturePrevious >= temperatureValue){
        setTemperatureAnimation(1);
      } else {
        setTemperatureAnimation(0);
      }
      temperaturePrevious = temperatureValue;
    } else {
      matrix1.clear();
      matrix1.writeSprite(0, 0, temperatureStill);
      //matrix2.clear();
      //matrix2.writeSprite(0, 0, crossError);
      delay(2000);
    }
  }
  if(magnitudeIdentifier == POTENTIAL_HYDROGEN_IDENTIFIER && controlsRunning[2]==1){
    if(potentialError == 0){
      //matrix2.clear();
      //matrix2.writeSprite(0, 0, noDimensionUnit);
      if(potentialPrevious >= potentialValue){
        setPotentialHydrogenAnimation(1);
      } else {
        setPotentialHydrogenAnimation(0);
      }
      potentialPrevious = potentialValue;
    } else {
      matrix1.clear();
      matrix1.writeSprite(0, 0, potentialHydrogenStill);
      //matrix2.clear();
      //matrix2.writeSprite(0, 0, crossError);
      delay(2000);
    }
  }
}

void configureMatrixInformation(int magnitudeIdentifier){
  if(magnitudeIdentifier==VELOCITY_IDENTIFIER){
    if (velocityError[0] == 0 && velocityError[1] == 0) {
      matrixInfo.print(velocityString);
    }
    if (velocityError[0] == 1 || velocityError[1] == 1) {
      matrixInfo.print("CONN");
    }
    if (velocityError[0] == 2 || velocityError[1] == 2) {
      matrixInfo.print("DATA");
    }
  }
  if(magnitudeIdentifier==TEMPERATURE_IDENTIFIER){
    if (temperatureError[0] == 0 && temperatureError[1] == 0) {
      matrixInfo.print(temperatureString);
    }
    if (temperatureError[0] == 1 || temperatureError[1] == 1) {
      matrixInfo.print("CONN");
    }
    if (temperatureError[0] == 2 || temperatureError[1] == 2) {
      matrixInfo.print("DATA");
    }
  }
  if(magnitudeIdentifier==POTENTIAL_HYDROGEN_IDENTIFIER){
    if (potentialError == 0) {
      matrixInfo.print(potentialString);
    }
    if (potentialError == 1) {
      matrixInfo.print("CONN");
    }
    if (potentialError == 2) {
      matrixInfo.print("DATA");
    }
  }
}

void configureInitialAnimationStep0(){
    matrix1.clear();
    matrix2.clear();
    matrix1.writeSprite(0, 0, screenLine1Horizontal);
    matrix2.writeSprite(0, 0, screenLine8Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine2Horizontal);
    matrix2.writeSprite(0, 0, screenLine7Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine3Horizontal);
    matrix2.writeSprite(0, 0, screenLine6Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine4Horizontal);
    matrix2.writeSprite(0, 0, screenLine5Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine5Horizontal);
    matrix2.writeSprite(0, 0, screenLine4Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine6Horizontal);
    matrix2.writeSprite(0, 0, screenLine3Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine7Horizontal);
    matrix2.writeSprite(0, 0, screenLine2Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine8Horizontal);
    matrix2.writeSprite(0, 0, screenLine1Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
}

void configureInitialAnimationStep1(){
    matrix1.clear();
    matrix2.clear();
    matrix1.writeSprite(0, 0, screenLine1Vertical);
    matrix2.writeSprite(0, 0, screenLine8Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine2Vertical);
    matrix2.writeSprite(0, 0, screenLine7Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine3Vertical);
    matrix2.writeSprite(0, 0, screenLine6Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine4Vertical);
    matrix2.writeSprite(0, 0, screenLine5Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine5Vertical);
    matrix2.writeSprite(0, 0, screenLine4Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine6Vertical);
    matrix2.writeSprite(0, 0, screenLine3Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine7Vertical);
    matrix2.writeSprite(0, 0, screenLine2Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine8Vertical);
    matrix2.writeSprite(0, 0, screenLine1Vertical);
    delay(INITIAL_ANIMATION_DELAY);
}

void configureInitialAnimationStep2(){
    matrix1.clear();
    matrix2.clear();
    matrix1.writeSprite(0, 0, screenLine8Horizontal);
    matrix2.writeSprite(0, 0, screenLine1Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine7Horizontal);
    matrix2.writeSprite(0, 0, screenLine2Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine6Horizontal);
    matrix2.writeSprite(0, 0, screenLine4Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine5Horizontal);
    matrix2.writeSprite(0, 0, screenLine4Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine4Horizontal);
    matrix2.writeSprite(0, 0, screenLine5Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine3Horizontal);
    matrix2.writeSprite(0, 0, screenLine6Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine2Horizontal);
    matrix2.writeSprite(0, 0, screenLine7Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine1Horizontal);
    matrix2.writeSprite(0, 0, screenLine8Horizontal);
    delay(INITIAL_ANIMATION_DELAY);
}

void configureInitialAnimationStep3(){
    matrix1.clear();
    matrix2.clear();
    matrix1.writeSprite(0, 0, screenLine8Vertical);
    matrix2.writeSprite(0, 0, screenLine1Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine7Vertical);
    matrix2.writeSprite(0, 0, screenLine2Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine6Vertical);
    matrix2.writeSprite(0, 0, screenLine4Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine5Vertical);
    matrix2.writeSprite(0, 0, screenLine4Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine4Vertical);
    matrix2.writeSprite(0, 0, screenLine5Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine3Vertical);
    matrix2.writeSprite(0, 0, screenLine6Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine2Vertical);
    matrix2.writeSprite(0, 0, screenLine7Vertical);
    delay(INITIAL_ANIMATION_DELAY);
    matrix1.writeSprite(0, 0, screenLine1Vertical);
    matrix2.writeSprite(0, 0, screenLine8Vertical);
    delay(INITIAL_ANIMATION_DELAY);
}

void showMessageAnimation(){
  if(countInitialAnimation==0){
    configureInitialAnimationStep0();
  }
  if(countInitialAnimation==1){
    configureInitialAnimationStep1();
  }
  if(countInitialAnimation==2){
    configureInitialAnimationStep2();
  }
  if(countInitialAnimation==3){
    configureInitialAnimationStep3();
  }
  countInitialAnimation = countInitialAnimation + 1;
  if(countInitialAnimation==4){
    countInitialAnimation = 0;
  }
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  matrix1.init();
  matrix1.setIntensity(8);
  matrix2.init();
  matrix2.setIntensity(8);
  matrixInfo.begin();
  attachInterrupt(1, previousMagnitude, CHANGE);
  attachInterrupt(0, nextMagnitude, RISING);
}

void previousMagnitude() {
  magnitudeSelected = magnitudeSelected-1;
  if(magnitudeSelected == 0){
    magnitudeSelected = POTENTIAL_HYDROGEN_IDENTIFIER;
  }
  matrix1.clear();
  matrix2.clear();
  delay(500);
}

void nextMagnitude() {
  magnitudeSelected = magnitudeSelected+1;
  if(magnitudeSelected == 4){
    magnitudeSelected = VELOCITY_IDENTIFIER;
  }
  matrix1.clear();
  matrix2.clear();
  delay(500);
}

void loop() {
  detachInterrupt(1);
  detachInterrupt(0);
  getProtocolMessage();
  if(messageToScroll == 1){
    if(firstTime == 1){
      matrixInfo.displayText(curMessage, scrollAlign, scrollSpeed, scrollPause, scrollEffect, scrollEffect);
      firstTime = 0;
    }
    if (matrixInfo.displayAnimate()) {
      if (newMessageAvailable) {
        strcpy(curMessage, newMessage);
        newMessageAvailable = false;
      }
      matrixInfo.displayReset();
    }
    showMessageAnimation();
  }
  if(pageStatus == HOME_PAGE_IDENTIFIER && packageReceived==1){
    //Serial.println("Page=1");
    strcpy(newMessage, "Welcome to SmartFermentor(TM) !!!");
    newMessageAvailable = true;
    messageToScroll = 1;
    newMessageReceived = 1;
  }
  if(pageStatus == FERMENTATION_PAGE_IDENTIFIER && packageReceived==1){
    //Serial.println("Page=4");
    strcpy(newMessage, "Configure Your FERMENTATION !!!");
    newMessageAvailable = true;
    messageToScroll = 1;
    newMessageReceived = 1;
  }
  if((pageStatus == CONTROLS_RUNNING_IDENTIFIER && packageReceived == 1) || newMessageReceived == 0 ){
    messageToScroll = 0;
    newMessageReceived = 0;
    firstTime = 1;
    if(magnitudeChanged == 1){
      configureMatrixInformation(magnitudeSelected);
      setMagnitudeInitialStatus(magnitudeSelected);
      magnitudeChanged = 0;
    } else {
      configureMatrixInformation(magnitudeSelected);
      setMagnitudeInformation(magnitudeSelected);
    }
  }
  packageReceived = 0;
  attachInterrupt(1, previousMagnitude, CHANGE);
  attachInterrupt(0, nextMagnitude, CHANGE);
}
