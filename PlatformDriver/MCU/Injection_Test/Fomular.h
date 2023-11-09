/*******************
Fomular.h

*******************/

#ifndef _Fomular_H__
#define _Fomular_H__

#include"Arduino.h"  


class Fomular
{
     private:
          String chemical; 
          float injectionSpeed;  
          float dosage; 
          int order;
          bool used;    
     
     
     public:
          Fomular();
          
          Fomular(String chemical , float injectionSpeed, float dosage, int order, bool used);

          String getName();
          
          float getSpeed(float maxDefaultSpeed);

          float getTime();

          int getOrder();

          bool activated();
};


#endif
