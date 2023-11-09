/*****************
Extract.cpp

******************/

#include"Extract.h"
#include"Setting.h"
#include"ChemRelMotor.h"

#define numberOfFomulars 4
int number = 0;

Extract::Extract(String blc, bool act)
{
   block = blc;
   activate = act;
}

Extract::Extract()
{
   block = "";
   activate = false;
}

String Extract::getBlock(){
   return block;
}
          
bool Extract::getAct(){
   return activate;
}

Setting *Extract::fillin()
{
  String buff = block;
  String setting[buff.length()];
  int numbers = 0;
  Setting fdata = Setting();
  Setting *temp = (Setting *)calloc(numberOfFomulars, sizeof(Setting));  

  if (activate == true){
    while(buff.length()>0)
    {
      int index = buff.indexOf(',');
      if (index != -1){
        setting[numbers++] = buff.substring(0,index);
        buff = buff.substring(index+1);
      } else {
        setting[numbers++] = buff;
        
        break;
      }
    }
    
    int count = 0;
    for(int i=0; i<numberOfFomulars; i++) //4
    {
      int SMC_position = setting[count].toInt();
      float injectionSpeed = setting[count+1].toFloat();    
      float duration = setting[count+2].toFloat();
      bool act = true;
      
      if (setting[count+3] == "true"){
        act = 1;
      }else{
        act = 0;
      }
      if (i == numberOfFomulars-1){
          if (setting[count+3].indexOf("true") == 0){
            act = 1;
          } else{
            act = 0;
          }
      }

      if (act==0){
        injectionSpeed = 0;
        duration = 0;
        act = 1;
      }
      
      fdata = Setting(SMC_position, injectionSpeed, duration, act);
      temp[i] = fdata;
      count = count+4;

      
      Serial.print("# ");
      Serial.println(i);
      Serial.print("Position: ");
      Serial.println(temp[i].getPosition());
      Serial.print("Stirring Speed: ");
      Serial.println(temp[i].getSpeed(7000));
      Serial.print("Time Usage: ");
      Serial.println(temp[i].getTime());
      Serial.print("Activated: ");
      Serial.println(temp[i].activated());
    }
    Serial.print("Download_Completed");
  }
  return temp;
}

RelMotor *Extract::motors()
{
  String buff = block;
  String setting[buff.length()];
  int numbers = 0;
  RelMotor fdata = RelMotor();
  RelMotor *temp = (RelMotor *)calloc(numberOfFomulars, sizeof(RelMotor));  

  if (activate == true){
    while(buff.length()>0)
    {
      int index = buff.indexOf(',');
      if (index != -1){
        setting[numbers++] = buff.substring(0,index);
        buff = buff.substring(index+1);
      } else {
        setting[numbers++] = buff;
        
        break;
      }
    }
    
    int count = 0;
    for(int i=0; i<numberOfFomulars; i++) //4
    {
      int SMC_position = setting[count].toInt();
      fdata = RelMotor(SMC_position, i);
      temp[i] = fdata;
      count = count+4;

      Serial.println();
      Serial.print("# ");
      Serial.println(i);
      Serial.print("Position: ");
      Serial.println(temp[i].getPosition());
      Serial.print("Motor: ");
      Serial.println(temp[i].getMotor());

    }
    Serial.print("Download_Completed");
  }
  return temp;
}
