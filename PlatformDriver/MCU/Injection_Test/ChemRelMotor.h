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
          String chemical; 
          int motor; 
          
     public:
          RelMotor();
          
          RelMotor(String chemical , int motor);

          String getName();
          
          int getMotor();
};


#endif
