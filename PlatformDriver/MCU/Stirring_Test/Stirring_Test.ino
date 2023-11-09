#include"Setting.h" 
#include"ChemRelMotor.h"
#include"Extract.h"
#include"Download.h"
#include <AFMotor.h> 
#define numberOfFomulars 4

AF_DCMotor motor1(1);               // create motor #1, 64KHz pwm - linked to the M3 port on L293D driver
AF_DCMotor motor2(2);               // create motor #2, 64KHz pwm - linked to the M4 port on L293D driver
AF_DCMotor motor3(3);               // create motor #3, 64KHz pwm - linked to the M3 port on L293D driver
AF_DCMotor motor4(4);               // create motor #4, 64KHz pwm - linked to the M4 port on L293D driver

AF_DCMotor motorList[] = {motor1, motor2, motor3 ,motor4};

float MaxDefaultSpeed = 7000;

int getListLength(Setting list[])
{
  int lengthOfList = 0;
  
  for (int i = 0; i < 4; i++){
    if (list[i].activated()){
      lengthOfList++;
    }
  }
  return lengthOfList;
}

/*********************
  * Sorting Algorithm 
**********************/
Setting *shortSort(int lengthOfList, Setting list[]){
  int pos = 0;
  int p = 0;
  
  Setting *temp = (Setting *)calloc(lengthOfList, sizeof(Setting));
  Setting *temp1 = (Setting *)calloc(lengthOfList, sizeof(Setting));
  
  bool duplicate = 0;
  
  for (int i = 0; i < lengthOfList; i++)
  {
    if(list[i].activated()){
      temp1[i] = list[i];
    }
  }

  for (int i = 0; i < lengthOfList; i++) 
  {
    for (int j = 0; j < lengthOfList; j++)
    {
      if(temp1[i].getTime() > temp1[j].getTime()){
        pos++; 
      }
    }
    if (temp1[i].getTime() == temp[pos].getTime()){
      p = pos;
      for(int k = pos; k < lengthOfList; k++){
        if (temp1[p].getTime() == temp[k].getTime()){
          pos++;
        }
      }
    }
    temp[pos] = temp1[i];
    pos = 0;
    p = 0;
  }
  
  
//  Serial.print("shortsort");
//  for (int j = 0; j < 4; j++){                      // TEST
//    Serial.print("\n");
//    Serial.print(temp[j].getPosition());
//    Serial.print("\t");
//    Serial.print(temp[j].getSpeed(MaxDefaultSpeed));
//    Serial.print("\t");
//    Serial.print(temp[j].getTime());
//    Serial.print("\t");
//    Serial.print(temp[j].activated());
//  }
//  Serial.print("\n");
  
  return temp;
}

/********************
 * Sorting MOTORLIST 
 ********************/
AF_DCMotor *getSortedMotorList(int lengthOfList, Setting list[], RelMotor *rellist)            //[motor1, motor2, motor3, motor4] -> [motor3, motor1, motor4, motor2] in input order
{
  int *rel = (int *)calloc(lengthOfList, sizeof(int));
  AF_DCMotor *sortedMotorList = (AF_DCMotor *)calloc(lengthOfList, sizeof(AF_DCMotor));

  for (int l = 0; l < lengthOfList; l++)
  {
   sortedMotorList[l] = motorList[list[l].getPosition()];
  }
  
//  Serial.print("Motor List");
//  for (int j = 0; j < 4; j++){                      // TEST
//    Serial.print("\n");
//    Serial.print(list[j].getPosition());
//    Serial.print("\t");
//    Serial.print(rel[j]);
//    Serial.print("\n");
//  }
    
  return sortedMotorList;
}

unsigned long *getDelayTimeList(int lengthOfList, Setting list[])
{
  unsigned long *delayTimeList = (unsigned long *)calloc(lengthOfList, sizeof(unsigned long));

  for (int i = 0; i < lengthOfList; i++)
  {
    if(i == 0){
      delayTimeList[0] = list[0].getTime();
    } else{
      delayTimeList[i] = list[i].getTime() - list[i-1].getTime();
    }
  }

//  Serial.print("Time List");
//  for (int j = 3; j >= 0; j--){                      // TEST
//    Serial.print("\n");
//    Serial.print(list[j].getPosition());
//    Serial.print("\t");
//    Serial.print(delayTimeList[j]);
//    Serial.print("\n"); 
//  }
  return delayTimeList;
}

int *getspdList(int lengthOfList, Setting list[], float maxDefaultSpeed)
{
  int *spdList = (int *)calloc(lengthOfList, sizeof(int));
  for (int i = 0; i < lengthOfList; i++)
  {
    spdList[i] = list[i].getSpeed(maxDefaultSpeed);
  }
//  Serial.print("Speed List");
//  for (int j = 0; j < 4; j++){                      // TEST
//    Serial.print("\n");
//    Serial.print(list[j].getPosition());
//    Serial.print("\t");
//    Serial.print(spdList[j]);
//    Serial.print("\n");
//  }
  return spdList;
}

/*****************
 * SIMULTANEOUS
 * STIRRING
******************/
bool simuStir(int lengthOfList, AF_DCMotor motorList[],unsigned long delayTimeList[], int spdList[])
{
  bool finish = false;

  
//  Serial.print("Speed List");
//  for (int j = 0; j < 4; j++){                      // TEST
//    Serial.print(spdList[j]);
//    Serial.print("\n");
//  }
//
//  Serial.print("Time List");
//  for (int j = 3; j >= 0; j--){                      // TEST
//    Serial.print(delayTimeList[j]);
//    Serial.print("\n"); 
//  }

  
  for (int i = 0; i < lengthOfList; i++)
  {
    if (i > 0) 
    {
      spdList[i - 1] = 0;
    }   
    for (int i = 0; i < lengthOfList; i++) 
    {
      motorList[i].setSpeed(spdList[i]);
      motorList[i].run(FORWARD);
    }    
    delay(delayTimeList[i]);
    Serial.print("\n");
    Serial.print(delayTimeList[i]);
    Serial.print("\n"); 
  }
  
  for (int i = 0; i < lengthOfList; i++) 
  {
    motorList[i].run(RELEASE); 
  }
  finish = true;
  return finish;
}

void setup() {
  Serial.begin(9600);                // set up Serial library at 9600 bps
  
}

void loop() {
  Setting SMC_position[4];
  Setting *fom;
  int mode = 0;
  int len = 0;    


  String block;
  int count = 1;

  Setting *temp = (Setting *)calloc(numberOfFomulars, sizeof(Setting));  
  RelMotor *temp1 = (RelMotor *)calloc(numberOfFomulars, sizeof(RelMotor));     
  while(Serial.available()>0)
  {    
    Serial.println(count);
    block = Serial.readString();
    if(block != ' '){
      Serial.println(block);  
      temp = Download(numberOfFomulars).getSetting(block);  
      temp1 = Download(numberOfFomulars).getMotorList(block); 
      count = count + 1;   
      break;
    }
    while(count<=1);
  }
  
  if (count > 1){
    delay(2000);
    for (int i = 0; i < 4; i++){                      // TEST
      SMC_position[i] = temp[i];
    }
    
    len = getListLength(SMC_position);
    
    fom = shortSort(len, SMC_position);
    Serial.print("\n");
    Serial.print("Sorted List");
    for (int j = 0; j < 4; j++){                      // TEST   
      Serial.print("\n");
      Serial.print(fom[j].getPosition());
      Serial.print("\t");
      Serial.print(fom[j].getSpeed(MaxDefaultSpeed));
      Serial.print("\t");
      Serial.print(fom[j].getTime());
      Serial.print("\t");
      Serial.print(fom[j].activated());
      Serial.print("\n");
    }
    bool finish = false;

    finish = simuStir(len, getSortedMotorList(len,fom,temp1), getDelayTimeList(len, fom),  getspdList(len, fom, MaxDefaultSpeed));
      
    motor1.run(RELEASE);
    motor2.run(RELEASE); 
    motor3.run(RELEASE); 
    motor4.run(RELEASE); 
    if (finish){
      count = count+1;
      Serial.print("finished");
    }
    while(count<=2);     
  }
  if (count > 2){
    while(1);
  }
}
