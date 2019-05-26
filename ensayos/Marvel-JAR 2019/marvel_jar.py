import time
import os
import matplotlib.pyplot as plt
import matplotlib.axes as axs
import numpy as np
import sys

class DataFile: # Clase para guardar los datos leídos

    def __init__(self, data_path):
        self.path = data_path

    def read(self, tags_line=1):

        with open(self.path, 'r+') as f:
            
            for i in range(tags_line):
                line = f.readline()

            elements = line[:-1].split(",")
            p = [[] for _ in elements]

            while True:
                line = f.readline()
                if line == '':
                    break

                values = line[:-1].split(",")

                for i in range(len(elements)):
                    try:
                        p[i].append(float(values[i]))
                    except:
                        p[i].append('')


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

    start = t[0]
    marvel.omni.t = t - start
    marvel.omni.x = x
    marvel.omni.y = y

    """ OptiTrack """
    data =  DataFile(opti_path).read(7)

    xi = 314
    yi = 316
 
    start = float(data[0][0])
    opti.omni.t = float(data[1][0]) - start
    opti.omni.x = float(data[xi][0])
    opti.omni.y = float(data[yi][0])


    for i in range(1, len(data[0])):

        if (data[xi][i] != '') and (data[yi][i] != ''):
            opti.omni.t = np.append(opti.omni.t, float(data[1][i]))
            opti.omni.x = np.append(opti.omni.x, float(data[xi][i]))
            opti.omni.y = np.append(opti.omni.y, float(data[yi][i]))


    """ Plot data """

    """Omni x, y """
    fig1 = plt.figure(1)

    plt.subplot(211)
    plt.title("Omniduino")
    plt.plot(marvel.omni.t, marvel.omni.x, label='Marvelmind', color='y')
    plt.plot(opti.omni.t, opti.omni.x, label='OptiTrack', color='m')
    plt.ylabel('x [m]')
    plt.legend()
    plt.grid(True)

    plt.subplot(212)
    plt.plot(marvel.omni.t, marvel.omni.y, label='Marvelmind', color='y')
    plt.plot(opti.omni.t, opti.omni.y, label='OptiTrack', color='m')
    plt.ylabel('y [m]')
    plt.xlabel('t [s]')
    plt.legend()
    plt.grid(True)

    # fig2 = plt.figure(2)

    # plt.plot(marvel.omni.x, marvel.omni.y, marker='o', markersize=3, color='g', )
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

    
    plt.show()