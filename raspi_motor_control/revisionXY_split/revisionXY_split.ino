#include <StepperMulti.h>

const int STEPS = 2048;
StepperMulti stepper(STEPS, 8,9,10,11);  //y axis
StepperMulti stepper2(STEPS, 4,5,6,7); //x axis
String sCopy ="";

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
  byte leng = Serial.readBytes(temp,9);
  
  //x   
   int nCount = 0;
   int nGetIndex = 0 ;

     String sTemp_x = "";   
     String sTemp_y="";


     //String으로 변환
    for(int i=0; i<leng; i++){
      sCopy += temp[i];
    }



      //구분자 찾기
      nGetIndex = sCopy.indexOf('/');

      //리턴된 인덱스가 있나?
      if(-1 != nGetIndex)
      {
         //있다.

         //데이터 넣고
         sTemp_x = sCopy.substring(0, nGetIndex);

         Serial.println( sTemp_x );
    
         //뺀 데이터 만큼 잘라낸다.

         sTemp_y = sCopy.substring(nGetIndex + 1);
      }
    
      moveXYstep(sTemp_x, leng, 11, X);
      moveXYstep(sTemp_y, leng, 8, Y);
  }

  //다시 값 전달 받기 전에 str 초기화
  sCopy="";

  stepper.moveStep();
  stepper2.moveStep();
}

void moveXYstep(String temp, int leng, int multiply, char axis) {
    int flag; //flag =0 일때 +각도 flag=1일때 -각도
    int angle = 0;
    if(temp.substring(0,1).equals("-")){
        flag=1;
         angle = temp.substring(1).toInt();
    }
    else{
      flag=0;
      angle = temp.toInt();
    }
    
    //string을 int형으로 변
    angle*=multiply;
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
    delay(500);
}


