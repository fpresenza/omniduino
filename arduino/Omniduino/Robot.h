#ifndef _ROBOT_H
#define _ROBOT_H

////////////////// ROBOT CLASS DECLARATION ///////////////////

class Robot {
  private:  
    bool              Init_Ref;
    struct sensor_data {
        float         Raw_X, Raw_Y, Raw_Z;
        bool          Updated; // flag of new data received
    } IndoorGPS, Mag;
    
  public:
    float             timesec; // Store current time in [s].
    const float       D = 0.116; // distance between centroid and wheel center.
    float             pX, pY, Yaw;
    float             pXRef, pYRef, YawRef;    
    float             vX, vY, vYaw;
    bool              new_pos_ref[3];

    Robot(); // default constructor.
    bool Initialized();
    void Read_PosRef();
    void Setup_IndoorGPS();
    void Read_IndoorGPS();
    void Setup_Mag_HMC5883();
    void Read_Mag_HMC5883();
    void Get_Coordinates();
    void Pos_Ctrl();
};

#endif
