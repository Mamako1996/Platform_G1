/*****************
ChemRelMotor.cpp

******************/
#include <AFMotor.h> 
#include"ChemRelMotor.h"
#include"Arduino.h"


RelMotor::RelMotor()
{
   chemical = "";
   motor = 0;
}

RelMotor::RelMotor(String ch , int mo)
{
   chemical = ch;
   motor = mo;
}

String RelMotor::getName(){
   return chemical;
}
          
int RelMotor::getMotor(){
   return motor;
}
