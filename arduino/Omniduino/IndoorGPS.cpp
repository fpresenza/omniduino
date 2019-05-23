#include <stdio.h>
#include <stdlib.h>
#include <Arduino.h>
#include "IndoorGPS.h"
#include "Robot.h"

void Robot::Setup_IndoorGPS() {  
  Serial2.begin(115200, SERIAL_8N1);
  while (Serial2.available() > 0) Serial2.read();
  IndoorGPS.Updated = false;
}

void Robot::Read_IndoorGPS() {
  
  long hedgehog_x, hedgehog_y;// coordinates of hedgehog (X,Y,Z) in mm.
  int toMeters_factor;
  int incoming_byte;
  int total_received_in_loop = 0;
  int packet_received = 0;
  bool good_byte;
  byte packet_size;
  uni_8x2_16 un16;
  uni_8x4_32 un32;
  
  while(Serial2.available() > 0) {

    //Serial1.println(true);
    
    if (hedgehog_serial_buf_ofs>=HEDGEHOG_BUF_SIZE) {
      hedgehog_serial_buf_ofs= 0;// restart bufer fill
      break;// buffer overflow
    }
   
    total_received_in_loop++;
    if (total_received_in_loop>100) break;// too much data without required header
    
    incoming_byte= Serial2.read();
    good_byte= false;
    //Serial1.println(hedgehog_serial_buf_ofs);
    switch(hedgehog_serial_buf_ofs) {
      case 0: {
        good_byte= (incoming_byte = 0xff);
        //Serial1.println("0");
        break;
      }
      case 1: {
        good_byte= (incoming_byte = 0x47);
        //Serial1.println("1");
        break;
      }
      case 2: {
        good_byte= true;
        //Serial1.println("2");
        break;
      }
      case 3: {
        hedgehog_data_id= (((unsigned int) incoming_byte)<<8) + hedgehog_serial_buf[2];
        good_byte=   (hedgehog_data_id == POSITION_DATAGRAM_ID) ||
                     (hedgehog_data_id == POSITION_DATAGRAM_HIGHRES_ID);
        //Serial1.println(hedgehog_data_id, HEX);
        break;
      }
      case 4: {
        switch(hedgehog_data_id) {
          case POSITION_DATAGRAM_ID: {
            good_byte= (incoming_byte == HEDGEHOG_CM_DATA_SIZE);
            //Serial1.println("cm data");
            break;
          }
          case POSITION_DATAGRAM_HIGHRES_ID: {
            good_byte= (incoming_byte == HEDGEHOG_MM_DATA_SIZE);
            //Serial1.println("mm data");
            break;
          }
        }
        break;
      }
      default: {
        good_byte= true;
        break;
      }
    }
      
    if (!good_byte) {
      hedgehog_serial_buf_ofs= 0;// restart bufer fill         
      continue;
    }     
    
    hedgehog_serial_buf[hedgehog_serial_buf_ofs++]= incoming_byte; 
    if (hedgehog_serial_buf_ofs>5) {
      packet_size=  7 + hedgehog_serial_buf[4];
      if (hedgehog_serial_buf_ofs == packet_size) {// received packet with required header
        packet_received= 1;
        hedgehog_serial_buf_ofs= 0;// restart bufer fill
        break; 
      }
    }
  }

  if (packet_received) {

    //Serial1.println("packet received");
    
    hedgehog_set_crc16(&hedgehog_serial_buf[0], packet_size);// calculate CRC checksum of packet
    if ((hedgehog_serial_buf[packet_size] == 0)&&(hedgehog_serial_buf[packet_size+1] == 0)) { // checksum success
      switch(hedgehog_data_id) {
        case POSITION_DATAGRAM_ID: {
          toMeters_factor = 100;
              
          // coordinates of hedgehog (X,Y), cm
          un16.b[0]= hedgehog_serial_buf[9];
          un16.b[1]= hedgehog_serial_buf[10];
          hedgehog_x= 10*long(un16.wi);

          un16.b[0]= hedgehog_serial_buf[11];
          un16.b[1]= hedgehog_serial_buf[12];
          hedgehog_y= 10*long(un16.wi);
                     
          break;
        }
        case POSITION_DATAGRAM_HIGHRES_ID: {
          toMeters_factor = 1000;
              
          // coordinates of hedgehog (X,Y), mm
          un32.b[0]= hedgehog_serial_buf[9];
          un32.b[1]= hedgehog_serial_buf[10];
          un32.b[2]= hedgehog_serial_buf[11];
          un32.b[3]= hedgehog_serial_buf[12];
          hedgehog_x= un32.vi32;
          
          un32.b[0]= hedgehog_serial_buf[13];
          un32.b[1]= hedgehog_serial_buf[14];
          un32.b[2]= hedgehog_serial_buf[15];
          un32.b[3]= hedgehog_serial_buf[16];
          hedgehog_y= un32.vi32;
          break;
        }
      }

      if (hedgehog_serial_buf[22] == 0x02) {
            // Store hedgehog position x, y in m.
        IndoorGPS.Raw_X = (float)(hedgehog_x)/toMeters_factor;
        IndoorGPS.Raw_Y = (float)(hedgehog_y)/toMeters_factor;
        IndoorGPS.Updated = true;// flag of new data from hedgehog received   
      }

    } 
  }
}

// Calculate CRC-16 of hedgehog packet
void hedgehog_set_crc16(byte *buf, byte size) {
  
  uni_8x2_16 sum;
  byte shift_cnt;
  byte byte_cnt;
 
  sum.w=0xffffU;
  for(byte_cnt=size; byte_cnt>0; byte_cnt--) {
    sum.w=(unsigned int) ((sum.w/256U)*256U + ((sum.w%256U)^(buf[size-byte_cnt])));
    for(shift_cnt=0; shift_cnt<8; shift_cnt++) {
      if((sum.w&0x1)==1) sum.w=(unsigned int)((sum.w>>1)^0xa001U);
      else sum.w>>=1;
    }
  }  

  buf[size]=sum.b[0];
  buf[size+1]=sum.b[1];// little endian

}// hedgehog_set_crc16
