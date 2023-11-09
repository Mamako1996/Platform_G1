/*******************
Setting.h

*******************/

#ifndef _Setting_H__
#define _Setting_H__

#include"Arduino.h"  


class Setting
{
     private:
          int SMC_position; 
          float stirringSpeed;  
          float duration; 
          bool used;    
     
     
     public:
          Setting();
          
          Setting(int SMC_position , float stirringSpeed, float duration, bool used);

          int getPosition();
          
          float getSpeed(float maxDefaultSpeed);

          float getTime();

          bool activated();
};


#endif
