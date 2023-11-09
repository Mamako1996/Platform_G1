/*****************
Setting.cpp

******************/

#include"Setting.h"
#include"Arduino.h"


Setting::Setting(int sp , float in, float ti, bool us)
{
   SMC_position = sp;
   stirringSpeed = in;
   duration = ti;
   used = us;
}

Setting::Setting()
{
   SMC_position = 0;
   stirringSpeed = 0;
   duration = 0.00;
   used = 0;
}

int Setting::getPosition(){
   return SMC_position;
}
          
float Setting::getSpeed(float maxDefaultSpeed){
  
  return (stirringSpeed) / (maxDefaultSpeed/255);
}

float Setting::getTime(){
  return duration;
}

bool Setting::activated(){
  return used;
}
