/*****************
Download.cpp

******************/

#include"Extract.h"
#include"Fomular.h"
#include"Download.h"

Download::Download(int nof)
{
  numberOfFomulars = nof;
}

Download::Download()
{
  numberOfFomulars = 0;
}

Fomular *Download::getFomular(String block)
{
  Fomular *temp = (Fomular *)calloc(numberOfFomulars, sizeof(Fomular));     
  temp = Extract(block,true).fillin();
  return temp;
}
