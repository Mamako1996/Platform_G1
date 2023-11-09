/*****************
Download.cpp

******************/

#include"Extract.h"
#include"Setting.h"
#include"Download.h"
#include"ChemRelMotor.h"

Download::Download(int nof)
{
  numberOfFomulars = nof;
}

Download::Download()
{
  numberOfFomulars = 0;
}

Setting *Download::getSetting(String block)
{
  Setting *temp = (Setting *)calloc(numberOfFomulars, sizeof(Setting));     
  temp = Extract(block,true).fillin();
  return temp;
}

RelMotor *Download::getMotorList(String block)
{
  RelMotor *temp = (RelMotor *)calloc(numberOfFomulars, sizeof(RelMotor));     
  temp = Extract(block,true).motors();
  return temp;
}
