#ifndef _ROBOT_H
#define _ROBOT_H

////////////////// ROBOT CLASS DECLARATION ///////////////////

class Robot {
  private:  
    bool              Init_Pos_Ref;
    bool              Init_Cmd_Vel;
    struct sensor_data {
        float         Raw_X, Raw_Y, Raw_Z;
        bool          Updated; // flag of new data received
    } IndoorGPS, Mag;
    
  public:
    float             timesec; // Store current time in [s].
    const float       D = 0.116; // distance between centroid and wheel center.
    float             pX, pY, Yaw;
    float             pXRef, pYRef, YawRef;
    float             Cmd_Vel_X, Cmd_Vel_Y, Cmd_Vel_Yaw;
    float             vX, vY, vYaw;
    bool              new_ref[3];
    bool              new_pos_ref;
    String            OP_MODE;

    Robot(); // default constructor.
    bool Initialized();
    void Read_Ref();
    void Setup_IndoorGPS();
    void Read_IndoorGPS();
    void Setup_Mag_HMC5883();
    void Read_Mag_HMC5883();
    void Get_Coordinates();
    void Pos_Ctrl();
    void Get_Cmd_Vel();
};

#endif
