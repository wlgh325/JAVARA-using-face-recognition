#include <Stepper.h>

const int STEPS = 2048;
char X = 0;
char Y = 1;
char serialChar = 0;
Stepper stepper(STEPS, 8,9,10,11);
Stepper stepper2(STEPS, 4,5,6,7);
String str="";

void setup()
{
  stepper.setSpeed(15);
  stepper2.setSpeed(15);
  Serial.begin(9600);
}

void loop()
{
  if(Serial.available()) {
    serialChar = Serial.read();
   if(serialChar == X)
  {
    stepper.step(1);
  }
  else if(serialChar == Y)
  {
    stepper2.step(1);
  }
}
