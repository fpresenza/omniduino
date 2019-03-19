clear all;
clc
% Variable compleja
    s = tf('s');
    
% Parámetros físicos

    WR = 0.024; %% wheel radius in meters (24 mm).
    D = 0.116; %% distance between centroid and wheel center.
  
% Matriz de transformación

    T = 80/(2*pi*WR) * [0, -1, -D; 0.5.*sqrt(3), 0.5, -D; -0.5*sqrt(3), 0.5, -D];
    
% Planta

    Gp = 1/s;
    
% Realimentación 

    H = 1;
    
% Sample time
 
    Ts = 0.125;
    
% Referencia

    pos_ref = [0; 0; pi/2];
    
% Controlador

    PROP_GAIN = [1.5 1.5 1.5];
    INT_GAIN = [1.25 1.25 0.001];
    DER_GAIN = 2;
    
% Límites de saturación

    UPPR_SAT_LIM = [0.0625 0.0625 10];
    LOW_SAT_LIM = [-0.0625 -0.0625 -10];
    
% Retardo de la transferencia mecánica
    
    Tr = 0.015;
    
% Trayectoria

    R = 0.5; % Amplitud
    V = 0.35 % Velocidad
    phaseX = pi/2; 
    phaseY = 0;
    centerX = 0
    centerY = 0
    omega = V/R;
    periodo = 2*pi/omega
