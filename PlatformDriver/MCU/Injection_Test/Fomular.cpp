/*****************
Fomular.cpp

******************/

#include"Fomular.h"
#include"Arduino.h"


Fomular::Fomular(String ch , float in, float dos, int ord, bool us)
{
   chemical = ch;
   injectionSpeed = in;
   dosage = dos;
   order = ord;
   used = us;
}

Fomular::Fomular()
{
   chemical = "";
   injectionSpeed = 0;
   dosage = 0;
   order = 0;
   used = 0;
}

String Fomular::getName(){
   return chemical;
}
          
float Fomular::getSpeed(float maxDefaultSpeed){
  float Injspeed = (injectionSpeed * 1000) / ((maxDefaultSpeed * 1000)/255);
  if(injectionSpeed == 0){
    Injspeed = 0;
  }
  return Injspeed;
}

float Fomular::getTime(){
  float d = (dosage / (injectionSpeed/60))*1000;
  if(dosage == 0){
    d = 0;
  }
  return d;
}

int Fomular::getOrder(){
  return order;
}

bool Fomular::activated(){
  return used;
}
