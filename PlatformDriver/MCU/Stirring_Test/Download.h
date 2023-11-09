/*******************
Download.h

*******************/

#ifndef _Download_H__
#define _Download_H__
 
#include"Setting.h"
#include"Extract.h"

class Download
{     
     private:
        int numberOfFomulars; 
        
     public:
          Download();
          
          Download(int numberOfFomulars);
          
          Setting *getSetting(String block);

          RelMotor *getMotorList(String block);
};


#endif
