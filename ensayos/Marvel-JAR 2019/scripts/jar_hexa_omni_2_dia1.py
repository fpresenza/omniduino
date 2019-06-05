#!/usr/bin/env python

import sys
sys.path.append("/home/fran/Repository/python_scripts/")

import time
import os
import matplotlib.pyplot as plt
import matplotlib.axes as axs
import numpy as np
from math import *
from pyquaternion import Quaternion
from DataFile import DataFile


class DataSource: 
    
    def __init__(self):
        self.omni = self.Vehicle()
        self.hexa = self.Vehicle()

    class Vehicle:
        pass


def euler_angles(q):

    if q[0] < 0:
        q = -q

    q0 = q[0]
    q1 = q[1]
    q2 = q[2]
    q3 = q[3] 
    
    roll  = atan2(2 * (q0*q1 + q2*q3), 1 - 2*(q1**2 + q2**2))
    pitch =  asin(2 * (q0*q2 - q3*q1))
    yaw   = atan2(2 * (q0*q3 + q1*q2), 1 - 2*(q2**2 + q3**2))   

    return yaw, pitch, roll



if __name__ == '__main__':

    
    """ Fuentes de datos """
    marvel = DataSource()
    opti = DataSource()


    """ Get path of data files """
    current_path = os.path.abspath(os.path.dirname(__file__))

    try:

        marvel_omni_file = str(sys.argv[1])
        marvel_hexa_file = str(sys.argv[2])
        opti_file = str(sys.argv[3])

    except:

        marvel_omni_file = "../omni_20190524_16:47:37.txt"
        marvel_hexa_file = "../hexa_omni_2.csv"
        opti_file = "../Hexa_Omni-2-2019-05-24 03.49.21 PM_005.csv"


    marvel_omni_path = os.path.join(current_path, marvel_omni_file)
    marvel_hexa_path = os.path.join(current_path, marvel_hexa_file)
    opti_path = os.path.join(current_path, opti_file)


    """ Read data """

    """ Marvelmind """

    """ Omni """

    data = DataFile(marvel_omni_path).read()

    t0 = data[0][0]

    marvel.omni.t = np.array(data[0]) - t0
    marvel.omni.x = np.array(data[1])
    marvel.omni.y = np.array(data[2])
    marvel.omni.yaw = np.array(data[3])

    raw_t = [val for val in marvel.omni.t]
    raw_x = [val for val in marvel.omni.x]
    raw_y = [val for val in marvel.omni.y]

    """ Hexa """


    

    """ OptiTrack """

    opti.info =  DataFile(opti_path).read(2, 6) 
    data =  DataFile(opti_path).read(7)

    xi = 286
    yi = 284
    qi = 280
    
    print(opti.info[xi])
    print(opti.info[yi])
    print(opti.info[qi])
    print(opti.info[qi+1])
    print(opti.info[qi+2])
    print(opti.info[qi+3])
    
    #print(data[yi][0])
    #print(data[yi][1])
    #print(data[yi][2])

    opti.omni.t = data[1][0]
    opti.omni.x = data[xi][0]
    opti.omni.y = data[yi][0]

    q = Quaternion()

    q[1] = data[qi][0]
    q[2] = data[qi+1][0]
    q[3] = data[qi+2][0]
    q[0] = data[qi+3][0]

    y, p, r = euler_angles(q)

    opti.omni.yaw = p

    for i in range(1, len(data[0])):

        if (data[xi][i] != '') and (data[yi][i] != ''):
            opti.omni.t = np.append(opti.omni.t, data[1][i])
            opti.omni.x = np.append(opti.omni.x, data[xi][i])
            opti.omni.y = np.append(opti.omni.y, data[yi][i])

            q[1] = data[qi][i]
            q[2] = data[qi+1][i]
            q[3] = data[qi+2][i]
            q[0] = data[qi+3][i]

            y, p, r = euler_angles(q)

            opti.omni.yaw = np.append(opti.omni.yaw, p)


    """ Bias correction """

    sum1 = np.zeros(3)
    sum2 = np.zeros(3)
    count1 = 0
    count2 = 0

    for i in range(len(marvel.omni.t)):

        if (marvel.omni.t[i] > 0 and marvel.omni.t[i] < 4.0):

            count1 += 1

            sum1[0] += marvel.omni.x[i]
            sum1[1] += marvel.omni.y[i]
            sum1[2] += marvel.omni.yaw[i]  

    mean1 =  sum1 / count1

    for i in range(len(opti.omni.t)):

        if (opti.omni.t[i] > 0 and opti.omni.t[i] < 4.0):

            count2 += 1

            sum2[0] += opti.omni.x[i]
            sum2[1] += opti.omni.y[i]
            sum2[2] += opti.omni.yaw[i]

    mean2 = sum2 / count2

    bias = mean2 - mean1

    marvel.omni.yaw -= mean1[2]
    opti.omni.yaw -= mean2[2]

    rot_bias = np.zeros(2)

    for i in range(len(marvel.omni.t)):

        yaw = marvel.omni.yaw[i]

        rot_bias = [cos(yaw) * bias[0] - sin(yaw) * bias[1], sin(yaw) * bias[0] + cos(yaw) * bias[1]]

        marvel.omni.x[i] += rot_bias[0]
        marvel.omni.y[i] += rot_bias[1]

        
    """ offset correction """
    marvel.omni.max_x = max(marvel.omni.x)
    # marvel.omni.max_y = max(marvel.omni.y)
    opti.omni.max_x = max(opti.omni.x)
    # opti.omni.max_y = max(opti.omni.y)
    t1 = np.zeros(2)
    t2 = np.zeros(2)
    found = [False, False, False, False]

    for i in range(len(marvel.omni.t)):

        if (marvel.omni.x[i] == marvel.omni.max_x and not found[0]):

            t1[0] = marvel.omni.t[i]
            found[0] = True
        
        # if (marvel.omni.y[i] == marvel.omni.max_y and not found[1]):

        #     t1[1] = marvel.omni.t[i]
        #     found[1] = True


    for i in range(len(opti.omni.t)):

        if (opti.omni.x[i] == opti.omni.max_x and not found[2]):

            t2[0] = opti.omni.t[i]
            found[2] = True

        # if (opti.omni.y[i] == opti.omni.max_y and not found[3]):

        #     t2[1] = opti.omni.t[i]
        #     found[3] = True


    marvel.omni.offset = (t2[0] - t1[0])
    marvel.omni.t += marvel.omni.offset 


    """ Plot data """

    """Omni x, y """
    fig1 = plt.figure(1)

    plt.subplot(211)
    plt.title("Omniduino")
    plt.plot(marvel.omni.t, marvel.omni.x, label='Marvelmind', color='y', linewidth=1)
    #plt.plot(raw_t, raw_x, label='Marvelmind RAW', color='r', linewidth=1)
    plt.plot(opti.omni.t, opti.omni.x, label='OptiTrack', color='m', linewidth=1)
    plt.ylabel('x [m]')
    plt.legend()
    plt.grid(True)

    plt.subplot(212)
    plt.plot(marvel.omni.t, marvel.omni.y, label='Marvelmind', color='y', linewidth=1)
    #plt.plot(raw_t, raw_y, label='Marvelmind RAW', color='r', linewidth=1)
    plt.plot(opti.omni.t, opti.omni.y, label='OptiTrack', color='m', linewidth=1)
    plt.ylabel('y [m]')
    plt.xlabel('t [s]')
    plt.legend()
    plt.grid(True)

    # fig2 = plt.figure(2)

    # plt.plot(marvel.omni.x, marvel.omni.y, marker='o', markersize=1.5, color='y')
    # plt.plot(opti.omni.x, opti.omni.y, marker='o', markersize=1.5, color='m')
    # plt.title("Omniduino")
    # plt.xlabel('x [m]')
    # plt.ylabel('y [m]')
    # plt.axis('scaled')

    # xmax = abs(max(marvel.omni.x, key=abs))
    # ymax = abs(max(marvel.omni.y, key=abs))

    # lim = round(max(xmax, ymax)) + 0.5

    # plt.xlim(-lim, lim)
    # plt.ylim(-lim, lim)
    # plt.xticks(np.arange(-int(lim), int(lim) + 1, 1))
    # plt.yticks(np.arange(-int(lim), int(lim) + 1, 1))
    # plt.grid(True)


    """ Omni yaw """
    fig3 = plt.figure(3)

    plt.title("Omniduino")
    plt.plot(marvel.omni.t, marvel.omni.yaw, label='Marvelmind', color='y')
    plt.plot(opti.omni.t, opti.omni.yaw, label='OptiTrack', color='m')
    plt.xlabel('t [s]')
    plt.ylabel('yaw [rad]')
    plt.legend()
    plt.grid(True)

    
    plt.show()