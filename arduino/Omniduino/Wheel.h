#ifndef _WHEEL_H
#define _WHEEL_H

////////////////// WHEEL CLASS DECLARATION ///////////////////

class Wheel {
  private:
    byte             ID; 
    byte             ENABLE, IN_1, IN_2;
    
  public:
    float            VelErrorInt;
    float            Duty;
    byte             A, B;
    const float      R = 0.024; // wheel radius in meters (24 mm).
    float            Vel, VelRef;
    
    Wheel(byte, byte, byte, byte, byte, byte);
    void Set_PWM();
    void Set_Encoder();
    void GetVel();
    void Vel_Ctrl();
    void Drive();
};

#endif
