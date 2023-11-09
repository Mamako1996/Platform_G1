/*****************
Extract.cpp

******************/

#include"Extract.h"
#include"Fomular.h"

#define numberOfPrameters 5
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

Fomular *Extract::fillin()
{
  String buff = block;
  String fomular[buff.length()];
  int numbers = 0;
  Fomular fdata = Fomular();
  Fomular *temp = (Fomular *)calloc(numberOfFomulars, sizeof(Fomular));  

  if (activate == true){
    while(buff.length()>0)
    {
      int index = buff.indexOf(',');
      if (index != -1){
        fomular[numbers++] = buff.substring(0,index);
        buff = buff.substring(index+1);
      } else {
        fomular[numbers++] = buff;
        
        break;
      }
    }
    
    int count = 0;
    for(int i=0; i<numberOfFomulars; i++) //4
    {
      String chemical = fomular[count];
      float injectionSpeed = fomular[count+1].toFloat();    
      float dosage = fomular[count+2].toFloat();
      int order = fomular[count+3].toInt();
      bool act = true;
      
      if (fomular[count+4] == "true"){
        act = 1;
      }else{
        act = 0;
      }
      if (i == numberOfFomulars-1){
          if (fomular[count+4].indexOf("true") == 0){
            act = 1;
          } else{
            act = 0;
          }
      }
      
      fdata = Fomular(chemical, injectionSpeed, dosage, order, act);
      temp[i] = fdata;
      count = count+5;

      
      Serial.print("# ");
      Serial.println(i);
      Serial.print("Chmeical Name: ");
      Serial.println(temp[i].getName());
      Serial.print("Injection Speed: ");
      Serial.println(temp[i].getSpeed(50.0));
      Serial.print("Time Usage: ");
      Serial.println(temp[i].getTime());
      Serial.print("Order: ");
      Serial.println(temp[i].getOrder());
      Serial.print("Activated: ");
      Serial.println(temp[i].activated());
    }
    Serial.print("Download_Completed");
  }
  return temp;
}
