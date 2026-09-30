// Consola ESP32 - Drones A/B/C
// Envia A, B o C por Serial al programa Python.
const int BTN_A=25, BTN_B=26, BTN_C=27;
bool antA=HIGH, antB=HIGH, antC=HIGH;
void setup(){
  Serial.begin(115200);
  pinMode(BTN_A,INPUT_PULLUP); pinMode(BTN_B,INPUT_PULLUP); pinMode(BTN_C,INPUT_PULLUP);
}
void loop(){
  bool a=digitalRead(BTN_A), b=digitalRead(BTN_B), c=digitalRead(BTN_C);
  if(antA==HIGH && a==LOW) Serial.println("TARGET:A");
  if(antB==HIGH && b==LOW) Serial.println("TARGET:B");
  if(antC==HIGH && c==LOW) Serial.println("TARGET:C");
  antA=a; antB=b; antC=c; delay(20);
}