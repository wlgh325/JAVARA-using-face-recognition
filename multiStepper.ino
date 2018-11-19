#include <StepperMulti.h>

const int STEPS = 2048;
char X = '0';
char Y = '1';
char serialChar = 0;
StepperMulti stepper(STEPS, 8,9,10,11);
StepperMulti stepper2(STEPS, 4,5,6,7);
String str="";

void setup()
{
  stepper.setSpeed(10);
  stepper2.setSpeed(10);
  Serial.begin(9600);
}

void loop()
{

  if(Serial.available()){
    char temp[10];
    
    byte leng = Serial.readBytes(temp,3);
    
    for(int i=0; i<leng; i++){
      str += temp[i];
    }
    
    int angle = str.toInt();
    
    angle = map(angle,0,360,0,2048);
    
    stepper.setStep(angle);
    stepper2.setStep(angle);
    
  }
  
    stepper.moveStep();
    stepper2.moveStep();
}


