#include <stdio.h>
#include <stdlib.h>
#include <Arduino.h>
#include "Main.h"
#include "Wheel.h"

Wheel::Wheel(byte i, byte a, byte b, byte c, byte d, byte e) { // Initialize Wheel variables;
  ID = i;
  ENABLE = a;
  IN_1 = b;
  IN_2 = c;
  A = d;
  B = e; 
  VelErrorInt = 0;
}

void Wheel::Set_PWM() { // Set PWM pins as outputs;
  pinMode(ENABLE, OUTPUT); 
  pinMode(IN_1, OUTPUT);
  pinMode(IN_2, OUTPUT);
}

void Wheel::Vel_Ctrl() {

  const float VEL_EST_GAIN = 6.51;
  const float VEL_PROP_GAIN = 9.6; // proportional constant;
  const float VEL_INT_GAIN = 48.0; // integral constant;

  GetVel(); // Read encoder and get velocity in c.p.s.; vel mínima que computa = 1000/(2*LOOP_DELAY[ms]) 1/s;
     
  float VelError = VelRef - Vel; // ESTIMATION OF VELOCITY ERRORS //
  VelErrorInt += VelError * LOOP_DELAY / 1000;   // INTEGRATION OF VELOCITY ERRORS // LOOP_DELAY is not exactly control time but very approximated 
  VelErrorInt = constrain(VelErrorInt, -80, 80); // INTEGRAL SATURATION & ANTI WIND-UP // 

  // CONTROL ACTION //
  Duty = VEL_EST_GAIN * VelRef + VEL_PROP_GAIN * VelError + VEL_INT_GAIN * VelErrorInt;
}

void Wheel::Drive() {

  unsigned int DutyApplied; // duty-cicles to be applied;

  if (Duty >= 0) {
    digitalWrite(IN_1, HIGH); // Set pins to counter-clockwise rotation
    digitalWrite(IN_2, LOW);
    DutyApplied = (int)(min(Duty, 4095) + 0.5); // Saturate duty at 4095 and round to integer units by adding 0.5 and truncate.
  }
  else if (Duty < 0) {
    digitalWrite(IN_1, LOW); // Set pins to clockwise rotation
    digitalWrite(IN_2, HIGH);
    DutyApplied = (-1) * (int)(max(Duty, -4095) - 0.5); // Saturate duty at -4095, round to integer units by sustracting 0.5 and truncate, and invert sign.
  }
  analogWrite(ENABLE, DutyApplied);  
}
