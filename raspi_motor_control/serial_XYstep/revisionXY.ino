#include <StepperMulti.h>

const int STEPS = 2048;
StepperMulti stepper(STEPS, 8,9,10,11);  //y axis
StepperMulti stepper2(STEPS, 4,5,6,7); //x axis
String str="";

char xSignal = '0';
char ySignal = '1';
char X = 'X';
char Y = 'Y';

void setup(){
  stepper.setSpeed(10);
  stepper2.setSpeed(10);
  Serial.begin(9600);
}

void loop(){
  
  if(Serial.available()) {
  char temp[10];
  byte leng = Serial.readBytes(temp,4);
  
  //x 
    if(temp[0] == xSignal){
      while(Serial.available() <= 0);
      char temp2[10];
      byte leng = Serial.readBytes(temp2,4);
      moveXYstep(temp2, leng, 1, X);
    }
    else if(temp[0] == ySignal){
      while(Serial.available() <= 0);
      char temp3[10];
      byte leng = Serial.readBytes(temp3,4);
      moveXYstep(temp3, leng, 8, Y);
    }
  }

  //다시 값 전달 받기 전에 str 초기화
  str="";

  stepper.moveStep();
  stepper2.moveStep();
}

void moveXYstep(char * temp, int leng, int multiply, char axis) {
    int flag; //flag =0 일때 +각도 flag=1일때 -각도
    int i;
 
    if(temp[0] == '-'){
        i=1;
        flag=1;
    }
    else{
      i=0;
      flag=0;
    }

    //String으로 변환
    for(; i<leng; i++){
      str += temp[i];
    }

    //string을 int형으로 변환
    int angle = str.toInt();
    
    if( angle > 3){
      //step수에 맞게 변환
      angle = map(angle,0,360,0,2048);

      if(flag == 0){
        if(axis == 'Y')
          stepper.setStep(-angle);
        else if (axis == 'X'){
          stepper2.setStep(angle);  
        }
      }
      else if(flag == 1){
        if(axis == 'Y'){
          stepper.setStep(angle);
        }
        else if (axis =='X')
          stepper2.setStep(-angle);
      }
    }
    delay(1000);
 
}
