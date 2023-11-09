#include"Fomular.h" 
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

RelMotor rellist[] = {RelMotor("A", 1), RelMotor("B", 2), RelMotor("C", 3), RelMotor("D", 4)};

float MaxDefaultSpeed = 50.0;

/*****************
 * LENGTH OF LIST 
******************/
int getListLength(int nOF)
{
  int lengthOfList = nOF;
  return lengthOfList;
}

int modes(int lengthOfList, Fomular list[]){             //*****ERROR

  bool allSame = 1;
  bool allInorder = 1;
  
  for (int i = 0; i < lengthOfList; i++)
  {
    if(list[0].getOrder() != list[i].getOrder()){
      allSame = 0;
    }
    
    for (int j = i; j < lengthOfList - 1; j++)
    { 
      if(list[i].getOrder() == list[j + 1].getOrder())
      {
        allInorder = 0;
      }
    }
    
  }
  
//  Serial.print("\n");
//  Serial.print(allSame);
//  Serial.print("\t");
//  Serial.print(allInorder);
//  Serial.print("\n");
    
  if (allSame){
    return 3;
  } else {
    if (allInorder){
      return 1;
    } else {
      return 2;
    }
  }
  
}

/*********************
  * Sorting Algorithm 
**********************/
Fomular *shortSort(int lengthOfList, Fomular list[], int mode){
  int pos = 0;
  
//  Fomular temp[lengthOfList];
//  Fomular temp1[lengthOfList];
  
  Fomular *temp = (Fomular *)calloc(lengthOfList, sizeof(Fomular));
  Fomular *temp1 = (Fomular *)calloc(lengthOfList, sizeof(Fomular));
  
  bool duplicate = 0;
  
  for (int i = 0; i < lengthOfList; i++)
  {
    if(list[i].activated()){
      temp1[i] = list[i];
    } else {
      temp1[i] = Fomular(list[i].getName() , 0, 0, 1, true);
    }
  }


  if(mode == 3){
    for (int i = 0; i < lengthOfList - 1; i++) {
      for (int j = 0; j < lengthOfList - i - 1; j++) {
        if (temp1[j].getTime() > temp1[j+1].getTime()) {
          Fomular t = temp1[j];
          temp1[j] = temp1[j+1];
          temp1[j+1] = t;
        }
      }
    }
    temp = temp1;
  } else {
    for (int i = 0; i < lengthOfList - 1; i++) {
      for (int j = 0; j < lengthOfList - i - 1; j++) {
        if (temp1[j].getTime() > temp1[j+1].getTime()) {
          Fomular t = temp1[j];
          temp1[j] = temp1[j+1];
          temp1[j+1] = t;
        }
      }
    }
    temp = temp1;
    for (int i = 0; i < lengthOfList - 1; i++) {
      for (int j = 0; j < lengthOfList - i - 1; j++) {
        if (temp1[j].getOrder() > temp1[j+1].getOrder()) {
          Fomular t = temp1[j];
          temp1[j] = temp1[j+1];
          temp1[j+1] = t;
        }
      }
    }  
    temp = temp1;
  }
//  Serial.print("shortsort");
//  for (int j = 0; j < 4; j++){                      // TEST
//    Serial.print("\n");
//    Serial.print(temp[j].getOrder());
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
AF_DCMotor *getSortedMotorList(int lengthOfList, Fomular list[])            //[motor1, motor2, motor3, motor4] -> [motor3, motor1, motor4, motor2] in input order
{
  int *rel = (int *)calloc(lengthOfList, sizeof(int));
  AF_DCMotor *sortedMotorList = (AF_DCMotor *)calloc(lengthOfList, sizeof(AF_DCMotor));
  
  for (int j = 0; j < lengthOfList; j++)
  {
    for (int k = 0; k < lengthOfList; k++)
    {
      if (list[j].getName() == rellist[k].getName())
      {
        rel[j] = rellist[k].getMotor();
      }
    }
  }
  for (int l = 0; l < lengthOfList; l++)
  {
   sortedMotorList[l] = motorList[rel[l] - 1];
  }
  
//  Serial.print("Motor List");
//  for (int j = 0; j < 4; j++){                      // TEST
//    Serial.print("\n");
//    Serial.print(list[j].getOrder());
//    Serial.print("\t");
//    Serial.print(rel[j]);
//    Serial.print("\n");
//  }  
  return sortedMotorList;
}

unsigned long *getDelayTimeList(int lengthOfList, Fomular list[], int mode)
{
  unsigned long *delayTimeList = (unsigned long *)calloc(lengthOfList, sizeof(unsigned long));
  if (mode == 3)
  {
    for (int i = 0; i < lengthOfList; i++)
    {
      if(i == 0){
        delayTimeList[0] = list[0].getTime();
      } else{
        delayTimeList[i] = list[i].getTime() - list[i-1].getTime();
      }
    }
  }

  if (mode == 1)
  {
    for (int i = 0; i < lengthOfList; i++)
    {
      delayTimeList[i] = list[i].getTime();
    }
  }

//  Serial.print("Time List");
//  for (int j = 3; j >= 0; j--){                      // TEST
//    Serial.print("\n");
//    Serial.print(list[j].getOrder());
//    Serial.print("\t");
//    Serial.print(delayTimeList[j]);
//    Serial.print("\n");
//  }  

  return delayTimeList;
}

int *getspdList(int lengthOfList, Fomular list[], float maxDefaultSpeed)
{
  int *spdList = (int *)calloc(lengthOfList, sizeof(int));
  for (int i = 0; i < lengthOfList; i++)
  {
    spdList[i] = list[i].getSpeed(maxDefaultSpeed);
    

  }
//  Serial.print("Speed List");
//  for (int j = 0; j < 4; j++){                      // TEST
//    Serial.print("\n");
//    Serial.print(list[j].getOrder());
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
  }
  
  for (int i = 0; i < lengthOfList; i++) 
  {
    motorList[i].run(RELEASE); 
  }
  finish = true;
  return finish;
}

/*****************
 * IN-ORDER
 * STIRRING
******************/
bool orderStir(int lengthOfList, AF_DCMotor motorList[],unsigned long delayTimeList[], int spdList[]){
  bool finish = false;
  for (int i = 0; i < lengthOfList; i++) 
  {
    motorList[i].setSpeed(spdList[i]);
    motorList[i].run(FORWARD);
    delay(delayTimeList[i]);
    motorList[i].run(RELEASE);
    
  }
  finish = true;
  return finish;
}

void switchBottom(int lengthOfList, int start, int endd, bool sameTime, Fomular list[], AF_DCMotor motorList[], int spdList[]){ //ERROR
  
  unsigned long *delayTimeList = (unsigned long *)calloc(lengthOfList, sizeof(unsigned long));
  

  
  int j = 0;
  int count = start + 1;
  if (sameTime){
    for (int i = start; i < endd + 1; i++)
    {
      if(i == start){
        delayTimeList[0] = list[start].getTime();
      } else{
        delayTimeList[j] = list[i].getTime() - list[i-1].getTime(); 
      }
      j++;
    }
//    Serial.print("SBTime List");
//    for (int k = 0; k < j; k++){                      // TEST
//      Serial.print("\n");
//      Serial.print(k);
//      Serial.print("\t");
//      Serial.print(delayTimeList[k]);
//      Serial.print("\n");
//    }          

    
    for (int i = 0; i < j; i++)
    {
      if (i > 0) 
      {
        spdList[count - 1] = 0;
        count++;
      }   
      for (int k = start; k < endd + 1; k++) 
      {
        motorList[k].setSpeed(spdList[k]);
        motorList[k].run(FORWARD);
      }    
      delay(delayTimeList[i]);
//      Serial.print("\n");
//      Serial.print(delayTimeList[i]);
//      Serial.print("\n");
    }
    
    for (int k = start; k < endd + 1; k++) 
    {
      motorList[k].run(RELEASE); 
    }
            
  } else {
    
    for (int i = start; i < endd + 1; i++)
    {
      delayTimeList[i] = list[i].getTime();
    }
        
    for (int j = start; j < endd + 1; j++) 
    {
      motorList[j].setSpeed(spdList[j]);
      motorList[j].run(FORWARD);
      delay(delayTimeList[j]);
      motorList[j].run(RELEASE);      
    }   
  }
  
}

bool ComboStir(int lengthOfList, AF_DCMotor motorList[], Fomular list[],int spdList[]){   //ERROR
  bool finish = false;

//  switchBottom(lengthOfList ,0, 1, 1, list, motorList, spdList);
//  switchBottom(lengthOfList ,2, 3, 0, list, motorList, spdList);

  int c1 = 0;
  int c2 = 0;
  int c3 = 0;

  if (list[0].getOrder() == list[1].getOrder()){
    c3 = 0;
  } else {
    c3 = 1;  
  }
  
  int inOrder[lengthOfList];
  int sameTime[lengthOfList];
  
  for (int i = 0; i < lengthOfList - 1; i++) 
  {     
    
    if (c3 == 0) {
      if (list[i].getOrder() == list[i+1].getOrder()){
        sameTime[c1] = i;
        c1++;
        if ((i+1) == (lengthOfList - 1)){
          sameTime[c1] = i+1;
          switchBottom(lengthOfList ,sameTime[0], sameTime[c1], 1, list, motorList, spdList);
          c1 = 0;
        }
      }
      if (list[i].getOrder() != list[i+1].getOrder()){
        sameTime[c1] = i;
        switchBottom(lengthOfList ,sameTime[0], sameTime[c1], 1, list, motorList, spdList);
        c1 = 0;
        c3 = 1;
        if ((i+1) == (lengthOfList - 1)){
          inOrder[c1] = i+1;
          switchBottom(lengthOfList ,inOrder[0], inOrder[c1], 0, list, motorList, spdList);
        }
        if ((i+2) == (lengthOfList - 1)){
          if (list[i+1].getOrder() == list[i+2].getOrder()){
            c3 = 0;
          } else {
            c3 = 1;  
          }
        }
      }
      
    } else {
      if (list[i].getOrder() != list[i+1].getOrder()){
        inOrder[c2] = i;
        c2++;
          
        if ((i+1) == (lengthOfList - 1)){
          inOrder[c2] = i+1;
          switchBottom(lengthOfList ,inOrder[0], inOrder[c2], 0, list, motorList, spdList);
          c2 = 0;
        }
      }
      if (list[i].getOrder() == list[i+1].getOrder()){
        
        inOrder[c2] = i;
        switchBottom(lengthOfList ,inOrder[0], inOrder[c2 - 1], 0, list, motorList, spdList);
        i--;
        c2 = 0;
        c3 = 0;    
      }      
    }
    
  }
  finish = true;
  return finish;
}


void setup() {
  Serial.begin(9600);                // set up Serial library at 9600 bps
}

void loop() {
  Fomular fomular[4];
  Fomular *fom;
  int mode = 0;
  int len = 0;    


  String block;
  int count = 1;

  Fomular *temp = (Fomular *)calloc(numberOfFomulars, sizeof(Fomular));  
  
  while(Serial.available()>0)
  {    
    Serial.println(count);
    block = Serial.readString();
    if(block != ' '){
      Serial.println(block);  
      temp = Download(numberOfFomulars).getFomular(block);   
      count = count + 1;   
      break;
    }
    while(count<=1);
  }
  
  if (count > 1){
    delay(2000);
    for (int i = 0; i < 4; i++){                      // TEST
      fomular[i] = temp[i];
    }
    
    len = getListLength(numberOfFomulars);
  
    mode = modes(len, fomular);
    
    fom = shortSort(len, fomular, mode);
    
    Serial.print("Sorted List");
    for (int j = 0; j < 4; j++){                      // TEST   
      Serial.print("\n");
      Serial.print(fom[j].getName());
      Serial.print("\t");
      Serial.print(fom[j].getOrder());
      Serial.print("\t");
      Serial.print(fom[j].getSpeed(MaxDefaultSpeed));
      Serial.print("\t");
      Serial.print(fom[j].getTime());
      Serial.print("\t");
      Serial.print(fom[j].activated());
    }
    bool finish = false;
    if (mode == 1)                                    //MODE 1 - ALL  IN-ORDER
    {
//      Serial.print("\n");
//      Serial.println("Mode 1");
      finish = orderStir(len, getSortedMotorList(len,fom), getDelayTimeList(len, fom, mode),  getspdList(len, fom, MaxDefaultSpeed));
    }
  
    if (mode == 2)                                    //MODE 2 - HELF IN-ORDER HELF & SIMULTANEOUS
    {
//      Serial.print("\n");
//      Serial.println("Mode 2");
     finish = ComboStir(len, getSortedMotorList(len,fom), fom, getspdList(len, fom, MaxDefaultSpeed));
    }
  
    if (mode == 3)                                    //MODE 3 - ALL SIMULTANEOUS
    {
//      Serial.print("\n");
//      Serial.println("Mode 3");
       finish = simuStir(len, getSortedMotorList(len,fom), getDelayTimeList(len, fom, mode),  getspdList(len, fom, MaxDefaultSpeed));
    } 
      
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
