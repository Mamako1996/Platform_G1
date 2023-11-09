/*******************
Download.h

*******************/

#ifndef _Download_H__
#define _Download_H__
 
#include"Fomular.h"
#include"Extract.h"

class Download
{     
     private:
        int numberOfFomulars; 
        
     public:
          Download();
          
          Download(int numberOfFomulars);
          
          Fomular *getFomular(String block);
};


#endif
