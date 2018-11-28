#include <StepperMulti.h>

const int STEPS = 2048;
StepperMulti stepper(STEPS, 8,9,10,11);
String str="";

void setup()
{
  stepper.setSpeed(15);
  Serial.begin(9600);
}

void loop()
{
  if(Serial.available()) {
    char temp[10];    //serial로 부터 받을 buffer
    byte leng = Serial.readBytes(temp,4); //byte형태로 받아서 temp저장, 크기 반환
    int flag=0; //flag =0 일때 +각도 flag=1일때 -각도
    int i = 0;

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

    //step수에 맞게 변환
    angle = map(angle,0,360,0,2048);
    
    if(flag == 0){
      //angle만큼 정회전
      stepper.setStep(angle);
    }
    else if(flag == 1){
      Serial.write("11111111");
      stepper.setStep(-angle);

    }
  }
  
  stepper.moveStep();
  
  //다시 값 전달 받기 전에 str 초기화
  str="";
}
