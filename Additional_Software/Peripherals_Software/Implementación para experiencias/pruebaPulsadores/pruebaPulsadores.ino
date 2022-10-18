void setup() {
  attachInterrupt(0, previousMagnitude, RISING);
  attachInterrupt(1, nextMagnitude, RISING);
  Serial.begin(9600);
}

void previousMagnitude() { //inicializa timer y conserva cuenta anterior en count
  detachInterrupt(0);
  detachInterrupt(1);
  delay(10000);
  Serial.println("PREVIOUS");
  attachInterrupt(0, previousMagnitude, RISING);
  attachInterrupt(1, nextMagnitude, RISING);
}

void nextMagnitude() { //inicializa timer y conserva cuenta anterior en count
  detachInterrupt(0);
  detachInterrupt(1);
  delay(10000);
  Serial.println("NEXT");
  attachInterrupt(0, previousMagnitude, RISING);
  attachInterrupt(1, nextMagnitude, RISING);
  
}

void loop() {
  

}
