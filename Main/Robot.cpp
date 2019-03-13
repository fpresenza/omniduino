#include <stdio.h>
#include <stdlib.h>
#include <Arduino.h>
#include "Main.h"
#include "Robot.h"

Robot::Robot() { // Initialize Omni variables;
  vX = vY = vYaw = 0;
  Init_Ref = false;
}

bool Robot::Initialized() { // Wait until Serial Port 1, IndoorGPS and Magnetometer data are ready //

  Read_PosRef(); // Read Omni's X, Y, YAW references from Serial port 1.
  Read_IndoorGPS(); // Read position of hedgehog from Indoor GPS service;
  Read_Mag_HMC5883(); // Read Earth's magnetic field vector from Magnetometer.
  if (Init_Ref && IndoorGPS.Updated && Mag.Updated) return true;
  else return false;
}

void Robot::Read_PosRef() { // Read last position reference in Serial 1 buffer

  float incoming_ref[3] = {0, 0, 0};
  new_pos_ref[0] = new_pos_ref[1] = new_pos_ref[2] = false;
  static bool ref_data_available[3] = {false, false, false};
  bool terminate = false;

  while (Serial1.available() > 0) {
    if (Serial1.read() != 'p') {
      while (Serial1.available() > 0 && Serial1.read() != '\n') {};
      continue;
    }
    do {
      char id_char = Serial1.read();
      switch (id_char) {
        case ('z'):
          new_pos_ref[0] = true;
          new_pos_ref[1] = true;
          new_pos_ref[2] = true;
          break;
        case ('x'):
          incoming_ref[0] = Serial1.parseFloat();
          new_pos_ref[0] = true;
          break;
        case ('y'):
          incoming_ref[1] = Serial1.parseFloat();
          new_pos_ref[1] = true;
          break;
        case ('w'):
          incoming_ref[2] = Serial1.parseFloat();
          new_pos_ref[2] = true;
          break;
        case ('r'):
          if (new_pos_ref[0]) {
            pXRef = incoming_ref[0];
            if (!ref_data_available[0]) ref_data_available[0] = true;
          }
          if (new_pos_ref[1]) {
            pYRef = incoming_ref[1];
            if (!ref_data_available[1]) ref_data_available[1] = true;
          }
          if (new_pos_ref[2]) {
            YawRef = incoming_ref[2] * PI / 180;
            if (!ref_data_available[2]) ref_data_available[2] = true;
          }
        default:
          terminate = true;
          break;
      }
    } while (!terminate);
  }
  if (!Init_Ref && ref_data_available[0] && ref_data_available[1] && ref_data_available[2]) Init_Ref = true;
}

void Robot::Get_Coordinates() {

  const float d[2] = {0.06, 0.03}; // X, Y distance from hedgehog to center of robot;

  const float c[3] = {13.81, 15.59, -40.91}; // Center correction of magnetometer values;
  const float a[2][3] = {{0.0758, 0.0009, -0.0022},
    			 {0.0009, 0.0749, 0.0012}
  }; // Magnitude correction matrix of magnetometer;

  const float zeroAngle = (-50) * PI / 180; // Angle correction for declination;
  float AngleRead, deltaAngle;
  static float preAngle = 0;
  static int lap = 0;

  if (Mag.Updated) {
    float mX = Mag.Raw_X - c[0]; // X correction in center of Mag;
    float mY = Mag.Raw_Y - c[1]; // Y correction in center of Mag;
    float mZ = Mag.Raw_Z - c[2]; // Z correction in center of Mag;

    mX = a[0][0] * mX + a[0][1] * mY + a[0][2] * mZ; // Correction in magnitude of Mag;
    mY = a[1][0] * mX + a[1][1] * mY + a[1][2] * mZ;

    AngleRead = atan2(mY, mX); // Get Yaw in +/-pi range;
    AngleRead -= zeroAngle; // Declination correction;

    deltaAngle = AngleRead - preAngle; // Count laps;
    if (deltaAngle < -6) lap++;
    else if (deltaAngle > 6) lap--;

    Yaw = AngleRead + lap * 2 * PI; // Get Yaw;
    Mag.Updated = false; // CLEAR MAGNETOMETER UPDATE FLAG //
    preAngle = AngleRead;
  }
  if (IndoorGPS.Updated) {
    pX = IndoorGPS.Raw_X + d[0] * cos(Yaw) - d[1] * sin(Yaw); // Correction in center of hedgehog;
    pY = IndoorGPS.Raw_Y + d[0] * sin(Yaw) + d[1] * cos(Yaw);
    IndoorGPS.Updated = false; // CLEAR HEDGEHOG POSITION UPDATE FLAG //
  }
}

void Robot::Pos_Ctrl() {

  const float PROP_GAIN[3] = {1, 1, 1.5}; // Proportional X, Y, Yaw gain;
  const float INT_GAIN[3]  = {1.25, 1.25, 0}; // Integral X, Y, Yaw gain;
  const float DER_GAIN[3]  = {0, 0, 0}; // Derivative X, Y, Yaw gain;
  static float SAT_LIM[3] = {0.05, 0.05 , 10}; // Integral saturation limit;

  static float pX_ErrorInt = 0;
  static float pY_ErrorInt = 0;
  float pX_ErrorDer = 0;
  float pY_ErrorDer = 0;

  // ESTIMATION OF POSITION ERRORS //
  float pX_Error = pXRef - pX; // X error //
  float pY_Error =  pYRef - pY; // Y error //
  float Yaw_Error = YawRef - Yaw; // YAW error //

  // INTEGRATION OF POSITION ERRORS //
  pX_ErrorInt += pX_Error * LOOP_DELAY / 1000;
  pY_ErrorInt += pY_Error * LOOP_DELAY / 1000;

  // INTEGRAL SATURATION & ANTI WIND-UP //
  pX_ErrorInt = constrain(pX_ErrorInt, -SAT_LIM[0], SAT_LIM[0]);
  pY_ErrorInt = constrain(pY_ErrorInt, -SAT_LIM[1], SAT_LIM[1]);

  // DERIVATIVE OF POSITION ERRORS //
  static float pX_preError = 0;
  static float pY_preError = 0;

  pX_ErrorDer = 1000 * (pX_Error - pX_preError) / LOOP_DELAY;
  pX_ErrorDer = 1000 * (pY_Error - pY_preError) / LOOP_DELAY;

  pX_preError = pX_Error;
  pY_preError = pY_Error;

  // ACCEPTANCE ZONE //
#define XLim   0.05 // Limits of acceptance zone;
#define YLim   0.05
#define YawLim 0.15

  if (!new_pos_ref[0] && (abs(pX_Error) < XLim) && (abs(pY_Error) < YLim) && (abs(Yaw_Error) < YawLim)) {
    pX_Error = 0;
    pX_ErrorInt = 0;
    pX_ErrorDer = 0;
    pX_preError = 0;
    SAT_LIM[0] = 0.1;

    pY_Error = 0;
    pY_ErrorInt = 0;
    pY_ErrorDer = 0;
    pY_preError = 0;
    SAT_LIM[1] = 0.1;
    
    Yaw_Error = 0;
  }

  // CONTROL ACTION //
  float vX_global = PROP_GAIN[0] * pX_Error + INT_GAIN[0] * pX_ErrorInt + DER_GAIN[0] * pX_ErrorDer;     // X Control Action. Obtain global frame's X velocity required;
  float vY_global = PROP_GAIN[1] * pY_Error + INT_GAIN[1] * pY_ErrorInt + DER_GAIN[1] * pX_ErrorDer;     // Y Control Action. Obtain global frame's Y velocity required;
  float vYaw_global = PROP_GAIN[2] * Yaw_Error;                                // Yaw Control Action. Obtain global frame's Yaw velocity required;

  // GLOBAL FRAME TO OMNI's FRAME CONVERTION //
  vX = cos(Yaw) * vX_global + sin(Yaw) * vY_global;
  vY = - sin(Yaw) * vX_global + cos(Yaw) * vY_global;
  vYaw = vYaw_global;
}
