/*******************
Extract.h

*******************/

#ifndef _Extract_H__
#define _Extract_H__
 
#include"Fomular.h"

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

          Fomular *fillin();
};


#endif
