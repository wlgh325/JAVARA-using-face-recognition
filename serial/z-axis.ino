#include <Stepper.h>

const int STEPS = 2048;
Stepper stepper(STEPS, 8,9,10,11);
String str="";

void setup()
{
  stepper.setSpeed(20);
  Serial.begin(9600);
}

void loop()
{
  if(Serial.available()) {
    char temp[10];    //serial로 부터 받을 buffer
    //angle=map(angle,0,360,0,2048); //회전각 스템
    byte leng = Serial.readBytes(temp,3); //byte형태로 받아서 temp저장, 크기 반환

    //String으로 변환
    for(int i=0; i<leng; i++){
      str += temp[i];
    }

    //string을 int형으로 변환
    int angle = str.toInt();

    //step수에 맞게 변환
    angle = map(angle,0,360,0,2048);

    //Serial.println(angle);

    //angle만큼 정회전
    stepper.step(angle);

    //역회전 전에 delay
    delay(2000);

    //angle만큼 역회전
    stepper.step(-angle);

    //다시 값 전달 받기 전에 str 초기화
    str="";
  }
}
