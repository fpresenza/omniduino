#include <stdio.h>
#include <stdlib.h>
#include <Arduino.h>
#include "Encoder.h"
#include "Wheel.h"

void Wheel::Set_Encoder() {
  pinMode(A, INPUT); // Set Encoders pins as inputs;
  pinMode(B, INPUT);
  
  pinB[ID] =  B;// Get Pin B numbers for IRS;
}

void Wheel::GetVel() { // Get velocity of encoders = (1 revolution) / (2 * time between interruptions);
  Vel = 1000000 / (2 * (float)del_t[ID]); 
}

void UpdateEncoder0() {
  long cur_t = micros(); // Get current time;

  if (digitalRead(pinB[0]) == LOW)  del_t[0] = cur_t - pre_t[0]; // Get time between interruptions and sign according to sense of rotation;
  else del_t[0] = (-1) * (cur_t - pre_t[0]);
  pre_t[0] = cur_t;
}

void UpdateEncoder1() {
  long cur_t = micros(); // Get current time
  
  if (digitalRead(pinB[1]) == LOW)  del_t[1] = cur_t - pre_t[1]; // Get time between interruptions and sign according to sense of rotation;
  else del_t[1] = (-1) * (cur_t - pre_t[1]);
  pre_t[1] = cur_t;
}

void UpdateEncoder2() {
  long cur_t = micros(); // Get current time
  
  if (digitalRead(pinB[2]) == LOW)  del_t[2] = cur_t - pre_t[2]; // Get time between interruptions and sign according to sense of rotation;
  else del_t[2] = (-1) * (cur_t - pre_t[2]);
  pre_t[2] = cur_t;
}
