// Consola ESP32 humanoide - dos joysticks y botones
const int J1X=34,J1Y=35,J2X=32,J2Y=33,B1=25,B2=26;
float n(int v){return (v-2047.5f)/2047.5f;}
void setup(){Serial.begin(115200);pinMode(B1,INPUT_PULLUP);pinMode(B2,INPUT_PULLUP);}
void loop(){
 Serial.printf("CTRL,%.3f,%.3f,%.3f,%.3f,%d,%d\n",
 n(analogRead(J1X)),n(analogRead(J1Y)),n(analogRead(J2X)),n(analogRead(J2Y)),
 digitalRead(B1)==LOW,digitalRead(B2)==LOW);
 delay(30);
}