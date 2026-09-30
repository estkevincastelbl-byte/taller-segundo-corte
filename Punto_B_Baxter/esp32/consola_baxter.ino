// Consola ESP32 para Baxter: 2 joysticks + botones de pinza
const int LX=34, LY=35, RX=32, RY=33;
const int OPEN_BTN=25, CLOSE_BTN=26;
void setup(){
  Serial.begin(115200);
  pinMode(OPEN_BTN,INPUT_PULLUP); pinMode(CLOSE_BTN,INPUT_PULLUP);
}
float normADC(int v){ return (v-2047.5f)/2047.5f; }
void loop(){
  Serial.printf("JOY,%.3f,%.3f,%.3f,%.3f,%d,%d\n",
    normADC(analogRead(LX)), normADC(analogRead(LY)),
    normADC(analogRead(RX)), normADC(analogRead(RY)),
    digitalRead(OPEN_BTN)==LOW, digitalRead(CLOSE_BTN)==LOW);
  delay(30);
}