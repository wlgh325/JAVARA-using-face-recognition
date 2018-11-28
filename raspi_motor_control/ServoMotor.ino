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
    char temp[5];
    byte leng = Serial.readBytes(temp,3);
    
    for(int i=0; i<leng; i++){
      str += temp[i];
    }
    Serial.print("1");
    int angle = str.toInt();
    Serial.print(angle);
    servo.write(angle);
    str="";
  }
}
