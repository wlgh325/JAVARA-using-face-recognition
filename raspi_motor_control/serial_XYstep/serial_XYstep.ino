#include <Stepper.h>

const int STEPS = 2048;
char X = '0';
char Y = '1';
char serialChar = 0;
Stepper stepper(STEPS, 8,9,10,11);
Stepper stepper2(STEPS, 4,5,6,7);
String str="";

void setup()
{
  stepper.setSpeed(5);
  stepper2.setSpeed(5);
  Serial.begin(9600);
}

void loop()
{
  int angle=0;

  if(Serial.available()) {
    serialChar = Serial.read();
    if(serialChar == X){
      angle = map(2,0,360,0,2048);
      stepper.step(angle);
      Serial.write("X\n");
    }
    else if(serialChar == Y){
      angle = map(2,0,360,0,2048);
      stepper2.step(angle);
      Serial.write("Y\n");
    }
  }
}


