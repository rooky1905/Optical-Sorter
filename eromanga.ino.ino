/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/
int i;
#include <Servo.h>

Servo myservo1;
Servo myservo2;// create servo object to control a servo
// twelve servo objects can be created on most boards

//char pos[2] = {"\0"};
int pos=0;
int old=0;

void setup() {
  myservo1.attach(9);
  myservo2.attach(8);
   Serial.begin(9600);// attaches the servo on pin 9 to the servo object
    myservo1.write(135); 
    myservo2.write(42); 
    
}
void scan()
{ 
myservo1.write(135);
delay(2000);
myservo1.write(108);
delay(1000);
/*myservo1.write(85);
delay(500);     
*/  
 }
void sort()
{ delay(500);

 if(Serial.available()>0)
 {pos=Serial.read();
  

  if(pos==49)
   {
    myservo2.write(15);
   }
   else if(pos==50)
   {
   myservo2.write(30);
   }
   
   else if(pos==51)
   {
   myservo2.write(45);
   }
   else if(pos==52)
   {
   
   myservo2.write(60);
   }
   else if(pos==53)
   {
   myservo2.write(75);
   }
   else if(pos==54)
   {
   myservo2.write(90);
   }
 
   delay(500);
   
 }
 }
void returnb()
{ for(i=110; i>=55; i--)
{myservo1.write(i);
delay(1);
  }
   delay(350);
   myservo1.write(135);
   delay(500);
}


void loop() {
  pos=0;
 
 scan();
 sort();
 if(pos>=49)
 {
  returnb();
 }
 else
 {
  myservo1.write(135);
   
 }
 }
        
  
