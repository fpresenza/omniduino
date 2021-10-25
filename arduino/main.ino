/* 
 *  
  Created on Tue May 21 11:52:24 2019
  @author: fpresenza 
 *  
 */

#include "main.h"
#include "robot.h"
#include "wheel.h"

// CREATE OBJETS //
Robot Omni;

Wheel Wheel[3] {
  {0, 2, 22, 23, 48, 49},  // Initialize Wheel 0 ID & Pin Numbers; 
  {1, 3, 24, 25, 50, 51},  // Initialize Wheel 1 ID & Pin Numbers; 
  {2, 4, 26, 27, 52, 53}   // Initialize Wheel 2 ID & Pin Numbers;
};

void setup() {
  
  Omni.Setup_IndoorGPS(); // INITIALIZE MARVELMIND INDOOR GPS //   
  Omni.Setup_Mag_HMC5883(); // INITIALIZE ADAFRUIT HMC5883 MAGNETOMETER // 

  // SETUP SERIAL PORT 1 //
  Serial.begin(115200, SERIAL_8N1);   //  Set up Serial Communication;
  Serial1.begin(115200, SERIAL_8N1);   //  Set up Serial Communication;
  Serial1.setTimeout(10); 

  // SETUP PWM// 
  analogWriteResolution(12);    // Set 12 bit resolution for PWM signaks;
  Wheel[0].Set_PWM(); // Set pin numbers for each wheel;
  Wheel[1].Set_PWM();
  Wheel[2].Set_PWM();

  // SETUP ENCODER IRS //
  Wheel[0].Set_Encoder(); // Prepare IRS for each wheel;
  Wheel[1].Set_Encoder();
  Wheel[2].Set_Encoder();
  
  attachInterrupt(digitalPinToInterrupt(Wheel[0].A), UpdateEncoder0, RISING); // run UpdateEncoder0() when Wheel[0].A rises from LOW to HIGH
  attachInterrupt(digitalPinToInterrupt(Wheel[1].A), UpdateEncoder1, RISING); // run UpdateEncoder1() when Wheel[1].A rises from LOW to HIGH
  attachInterrupt(digitalPinToInterrupt(Wheel[2].A), UpdateEncoder2, RISING); // run UpdateEncoder2() when Wheel[2].A rises from LOW to HIGH

  // WAIT UNTIL OMNIWHEEL IS INITIALIZED //
  
  while (!Omni.Initialized()) {
    //Serial1.println("Inicializando...");
    delay(SETUP_DELAY);
  }
  
  // FLUSH SERIAL BUFFER //
  while (Serial1.available()>0) Serial1.read();
}

void loop() {

  // OMNIWHEEL PART - POSITION SENSORING AND CONTROL// 
  Omni.timesec = 0.001 * (float)millis(); // Get current time in seconds;
  Omni.Read_Ref(); // Read Serial 1 port for position reference or commanded velocity.
  Omni.Read_IndoorGPS(); // Read position of hedgehog from Indoor GPS service;
  Omni.Read_Mag_HMC5883(); // Read Earth's magnetic field vector from Magnetometer.
  Omni.Get_Coordinates(); // Estimate Omni's X, Y, YAW coordinates from values read;

  
  if (Omni.OP_MODE == 0x00) { 
    Omni.Pos_Ctrl(); // Implement Position Control Action = Obtain required Omni velocities;    
  }
  else if (Omni.OP_MODE == 0xff) { 
    Omni.Get_Cmd_Vel();
  }

  // KINEMATIC TRANSFORMATION MATRIX //
  KinematicTransf(); // Convert required Omni's velocities to wheel velocities.
  
  // WHEEL PART - VELOCITY SENSORING AND CONTROL // 
  Wheel[0].Vel_Ctrl(); // Read velocity from encoders & Get PWM's Duty Cicle for each wheel. 
  Wheel[1].Vel_Ctrl();
  Wheel[2].Vel_Ctrl();

  Wheel[0].Drive();   // Drive Motors of each wheel to get required velocity with PWM signal.
  Wheel[1].Drive();
  Wheel[2].Drive();

  
  //Serial1.println(Omni.OP_MODE);
  // SERIAL PRINT //

  Serial1.print('a');
  Serial1.print(Omni.timesec, 3); Serial1.print(',');
  Serial1.print(Omni.pX, 3); Serial1.print(',');
  Serial1.print(Omni.pY, 3); Serial1.print(',');
  Serial1.print(Omni.Yaw, 3); Serial1.print(',');
  Serial1.print(Omni.Marvel_Yaw, 3); Serial1.print(',');
  Serial1.print(Wheel[0].enc_count); Serial1.print(',');
  Serial1.print(Wheel[1].enc_count); Serial1.print(',');
  Serial1.print(Wheel[2].enc_count); Serial1.print('\n');
  

  // DELAY //
  delay(LOOP_DELAY);
}

void KinematicTransf() {
  // SET ENCODER'S VELOCITY REFERENCE FROM OMNI'S VELOCITIES //
  Wheel[0].VelRef = 80 / (2 * PI * Wheel[0].R) * (-Omni.vY - Omni.vYaw * Omni.D);
  Wheel[1].VelRef = 80 / (2 * PI * Wheel[1].R) * (0.5 * sqrt(3) * Omni.vX + 0.5 * Omni.vY - Omni.vYaw * Omni.D);
  Wheel[2].VelRef = 80 / (2 * PI * Wheel[2].R) * (-0.5 * sqrt(3) * Omni.vX + 0.5 * Omni.vY - Omni.vYaw * Omni.D);

  // ENCODER'S VELOCITY REFERENCE SATURATION // 
  Wheel[0].VelRef = constrain(Wheel[0].VelRef,-160,160);
  Wheel[1].VelRef = constrain(Wheel[1].VelRef,-160,160);
  Wheel[2].VelRef = constrain(Wheel[2].VelRef,-160,160);   
}
