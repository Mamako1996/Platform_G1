/*******************
ChemRelMotor.h

*******************/

#ifndef _ChemRelMotor_H__
#define _ChemRelMotor_H__

#include"Arduino.h"  
#include <AFMotor.h> 

class RelMotor
{
     private:
          int SMC_position; 
          int motor; 
          
     public:
          RelMotor();
          
          RelMotor(int SMC_position , int motor);

          int getPosition();
          
          int getMotor();
};


#endif
