/*****************
ChemRelMotor.cpp

******************/
#include <AFMotor.h> 
#include"ChemRelMotor.h"
#include"Arduino.h"


RelMotor::RelMotor()
{
   SMC_position = 0;
   motor = 0;
}

RelMotor::RelMotor(int sp , int mo)
{
   SMC_position = sp;
   motor = mo;
}

int RelMotor::getPosition(){
   return SMC_position;
}
          
int RelMotor::getMotor(){
   return motor;
}
