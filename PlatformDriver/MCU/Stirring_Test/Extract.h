/*******************
Extract.h

*******************/

#ifndef _Extract_H__
#define _Extract_H__
 
#include"Setting.h"
#include"ChemRelMotor.h"

class Extract
{
     private:
          String block; 
          bool activate;    
     
     public:
          Extract();
          
          Extract(String block, bool activate);

          String getBlock();

          bool getAct();

          Setting *fillin();
          
          RelMotor *motors();
};


#endif
