char palabra[] = "X030395";

void setup(){
Serial.begin(9600);
Serial.print("The string to which LRC is calculated is : ");
Serial.println(palabra);
int lrc = 0;
byte character = 0;
int i = 0;
int suma = 0;
char vrc[1];
for (i=0; i<strlen(palabra); i++){
  character = palabra[i];
  Serial.println(character);
  suma = suma + character;
  lrc = (lrc + character) & 0xff;
}
lrc = (((lrc^0xff)+1)&0xff);
//Serial.println(lrc, HEX);

Serial.println(suma);

vrc[0] = '0';
if(suma%2!=0){
  vrc[0] = '1';
}

strcat(palabra,vrc);

char hex[2];
utoa((unsigned)lrc,hex,16); // utoa() function is used to convert unsigned int to HEX array (whatever the base we specified as third argument)
strcat(palabra,hex);

int finalval = 256;
char buf [6];
sprintf (buf, "%01c%01c%03i", '0', '0', finalval);
Serial.println(buf);

Serial.println(palabra);

//int hex_val = (int)strtol(hex,NULL,16);// strtol() is used to covert string into long int according to the given base

//int val = calculate();
//convert_to_hex(lrc);
}

void loop(){}
/*
//CALCULATE() FUNCTION
int calculate(){
  int i = 0;
  for (i=0; i<strlen(a); i++){
    
  }
return sum;
}//end of calculate() function

//FUNCTION_SUM() FUNCTION
int find_sum(const int * val) {
int sum = 0;
Serial.print("VAL: ");
Serial.println(val[0]);
for(int i=0;i<= (strlen(a)/2) - 1;i++) {
  Serial.print("VAL[i]:");
  Serial.println(val[i]);
  sum = sum + val[i];
}
return sum; 
}//end of find_sum() function

//FUNCTION TO CONVERT HEX TO THE DECIMAL VALUE
int conv(char val1,char val2){
int val_a = toDec(val1); // convert to the decimal value
int val_b = toDec(val2);
return (val_a*16) + val_b; // converting decimal value into HEX decimal Equalent B1*16 + B0
}//end of conv() function

int toDec(char val){
if(val<='9')
{
return val - '0'; // please see the ASCII table for clarification
}
else 
{
return val - '0'-7; // 7 is offset for capital letters please see the ASCII table 
}

}//end of toDec() function
*/
void convert_to_hex(int val){
char hex[5];
utoa((unsigned)val,hex,16); // utoa() function is used to convert unsigned int to HEX array (whatever the base we specified as third argument)
int hex_val = (int)strtol(hex,NULL,16);// strtol() is used to covert string into long int according to the given base

Serial.print("the LRC value is : ");
Serial.println(hex_val,HEX);
char hex_val_str[4];
sprintf(hex_val_str,"%0.2x",hex_val);// putting hex value in the string back
Serial.print("the concated string is : ");
strcat(palabra,hex_val_str);
//char ter[] = "\r\n";
//strcat(a,ter);//adding terminators at the end or STOP bits
Serial.println(palabra);
}

