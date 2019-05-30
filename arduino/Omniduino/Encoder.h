#ifndef _ENCODER_H
#define _ENCODER_H

volatile byte pinB[3]; // Pin B of encoders;
volatile long pre_t[3] = {0, 0, 0}; // Previous time of encoder interruption;
volatile long del_t[3] = {999999, 999999, 999999}; // Time lapse between encoder interruption;

volatile int count[3] = {0, 0, 0};

#endif
