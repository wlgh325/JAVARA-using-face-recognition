#include <Servo.h>

int servoPin=8;
Servo servo;
int angle =0;
String str="";

void setup(){
  servo.attach(servoPin);
  Serial.begin(9600);
}

void loop(){
  
  if(Serial.available()){
    char temp[10];
    byte leng = Serial.readBytes(temp,3);
    
    for(int i=0; i<leng; i++){
      str += temp[i];
    }
    
    int angle = str.toInt();
    for(int i = 0;  i < angle; i++){
      servo.write(i);
      delay(15);
    }
    str="";
  }
}
