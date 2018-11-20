#include <StepperMulti.h>

const int STEPS = 2048;
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
  if(Serial.available()) {
    char temp[10];    //serial로 부터 받을 buffer
    byte leng = Serial.readBytes(temp,4); //byte형태로 받아서 temp저장, 크기 반환
    int flag; //flag =0 일때 +각도 flag=1일때 -각도
    int i;

    if(temp[0] == "-"){
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

    //step수에 맞게 변환
    angle = map(angle,0,360,0,2048);

    if(flag == 0){
      //angle만큼 정회전
      stepper.setStep(angle);
      stepper2.setStep(angle);
    }
    else if(flag == 1){
      //angle만큼 역회전
      stepper.setStep(-angle);
      stepper2.setStep(-angle);
    }

  }

  stepper.moveStep();
  stepper2.moveStep();

  //다시 값 전달 받기 전에 str 초기화
  str="";
}
