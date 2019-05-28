import time
import os
import matplotlib.pyplot as plt
import matplotlib.axes as axs
import numpy as np
import sys
from math import *

class DataFile: # Clase para guardar los datos leídos

    def __init__(self, data_path):
        self.path = data_path

    def read(self, start_line=0, end_line=10000):

        with open(self.path, 'r+') as f:
            
            for i in range(start_line + 1):
                line = f.readline()

            try:
                elements = line[:-1].split(",")
                p = [[] for elem in elements]

            except:
                elements = ['info']
                p = [[]]
 
            for _ in range(end_line - start_line):

                line = f.readline()
                if line == '':
                    break

                values = line[:-1].split(",")

                for i in range(len(elements)):
                    try:
                        p[i].append(float(values[i]))
                    except:
                        p[i].append(str(values[i]))


        return np.array(p)


class DataSource: 
    
    def __init__(self):
        self.omni = self.Vehicle()
        self.hexa = self.Vehicle()

    class Vehicle:
        pass



if __name__ == '__main__':

    
    """ Fuentes de datos """
    marvel = DataSource()
    opti = DataSource()


    """ Get path of data files """
    current_path = os.path.abspath(os.path.dirname(__file__))

    marvel_omni_file = str(sys.argv[1])
    marvel_omni_path = os.path.join(current_path, marvel_omni_file)

    opti_file = str(sys.argv[2])
    opti_path = os.path.join(current_path, opti_file)


    """ Read data """

    """ Marvelmind """
    t, x, y, yaw, n1, n2, n3 = DataFile(marvel_omni_path).read()

    marvel.omni.t = t - t[0]
    marvel.omni.x = x
    marvel.omni.y = y
    marvel.omni.yaw = yaw

    raw_t = [val for val in marvel.omni.t]
    raw_x = [val for val in marvel.omni.x]
    raw_y = [val for val in marvel.omni.y]

    """ OptiTrack """

    opti.info =  DataFile(opti_path).read(2, 6)
    

    data =  DataFile(opti_path).read(6)

    xi = 286
    yi = 284
    yawi = 282
    
    #print(opti.info[yawi])
    
    #print(data[yi][0])
    #print(data[yi][1])
    #print(data[yi][2])


    opti.omni.offset = float(data[0][0])
    opti.omni.t = float(data[1][0]) - opti.omni.offset
    opti.omni.x = float(data[xi][0])
    opti.omni.y = float(data[yi][0])
    opti.omni.yaw = float(data[yawi][0])

    for i in range(1, len(data[0])):

        if (data[xi][i] != '') and (data[yi][i] != ''):
            opti.omni.t = np.append(opti.omni.t, float(data[1][i]))
            opti.omni.x = np.append(opti.omni.x, float(data[xi][i]))
            opti.omni.y = np.append(opti.omni.y, float(data[yi][i]))
            opti.omni.yaw = np.append(opti.omni.yaw, float(data[yawi][i]))


    """ Bias correction """

    sum1 = np.zeros(3)
    sum2 = np.zeros(3)
    count1 = 0
    count2 = 0

    for i in range(len(marvel.omni.t)):

        if (marvel.omni.t[i] > 50.0 and marvel.omni.t[i] < 55.0):

            count1 += 1

            sum1[0] += marvel.omni.x[i]
            sum1[1] += marvel.omni.y[i]
            sum1[2] += marvel.omni.yaw[i]  

    mean1 =  sum1 / count1

    for i in range(len(opti.omni.t)):

        if (opti.omni.t[i] > 50.0 and opti.omni.t[i] < 55.0):

            count2 += 1

            sum2[0] += opti.omni.x[i]
            sum2[1] += opti.omni.y[i]
            sum2[2] += opti.omni.yaw[i]

    mean2 = sum2 / count2

    bias = mean2 - mean1

    # #dist = sqrt(bias[0]**2 + bias[1]**2)
    # #print(dist)

    marvel.omni.yaw -= mean1[2]
    opti.omni.yaw = pi*(-opti.omni.yaw + mean2[2])

    
    rot_bias = np.zeros(2)

    for i in range(len(marvel.omni.t)):

        yaw = marvel.omni.yaw[i]

        rot_bias = [cos(yaw) * bias[0] - sin(yaw) * bias[1], sin(yaw) * bias[0] + cos(yaw) * bias[1]]

        marvel.omni.x[i] = marvel.omni.x[i] + rot_bias[0]
        marvel.omni.y[i] = marvel.omni.y[i] + rot_bias[1]

        
    """ offset correction """
    marvel.omni.max_x = max(marvel.omni.x)
    marvel.omni.max_y = max(marvel.omni.y)
    opti.omni.max_x = max(opti.omni.x)
    opti.omni.max_y = max(opti.omni.y)
    t1 = np.zeros(2)
    t2 = np.zeros(2)

    for i in range(len(marvel.omni.t)):

        if (marvel.omni.x[i] == marvel.omni.max_x):

            t1[0] = marvel.omni.t[i]
        
        if (marvel.omni.y[i] == marvel.omni.max_y):

            t1[1] = marvel.omni.t[i]


    for i in range(len(opti.omni.t)):

        if (opti.omni.x[i] == opti.omni.max_x):

            t2[0] = opti.omni.t[i]

        if (opti.omni.y[i] == opti.omni.max_y):

            t2[1] = opti.omni.t[i]


    marvel.omni.offset = (t2[0] + t2[1] - t1[0] - t1[1]) / 2
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

    # fig3 = plt.figure(3)

    # plt.title("Omniduino")
    # plt.plot(marvel.omni.t, marvel.omni.yaw, label='Marvelmind', color='y')
    # plt.plot(opti.omni.t, opti.omni.yaw, label='OptiTrack', color='m')
    # plt.xlabel('t [s]')
    # plt.ylabel('yaw [rad]')
    # plt.legend()
    # plt.grid(True)

    
    plt.show()