#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, TwistStamped
import matplotlib.pyplot as plt


def plot_callback(pose):

    global t, x, y, yaw

    tsecs = pose.header.stamp.secs
    tnsecs = pose.header.stamp.nsecs

    t.append(tsecs + tnsecs*10**(-9))
    x.append(pose.twist.linear.x)
    y.append(pose.twist.linear.y)
    yaw.append(pose.twist.angular.z)

    plt.figure(1)
    plt.plot(x, y, color='blue', marker='.', markersize=4)
    #plt.axis([-5, 5, -5, 5])
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.xlabel('x [m]', fontsize='12')
    plt.ylabel('y [m]', fontsize='12')
    plt.grid(True)
    plt.draw()
    plt.pause(0.001)

    plt.figure(2)
    plt.plot(t, x, color='g', marker='')
    plt.ylim(-5, 5)
    plt.ylabel('x [m]', fontsize='12')
    plt.xlabel('t [s]', fontsize='12')
    plt.grid(True)
    plt.draw()
    plt.pause(0.001)

    plt.figure(3)
    plt.plot(t, y, color='m', marker='')
    plt.ylim(-5, 5)
    plt.ylabel('y [m]', fontsize='12')
    plt.xlabel('t [s]', fontsize='12')
    plt.grid(True)
    plt.draw()
    plt.pause(0.001)   
    

if __name__ == '__main__':

    """ Inicializar nodo """
    rospy.init_node('omni_plot')

    """ subscribes to /omni_pose topic where omni_serial node publishes """
    cmd_vel_sub = rospy.Subscriber(name='omni_pose', data_class=TwistStamped, callback=plot_callback, queue_size=1)

    rospy.loginfo("OMNIDUINO PLOT succesfully initialized.")


    """ Plot Config """
    plt.ion()
    plt.show()
    t = []
    x = []
    y = []
    yaw = []

    rospy.spin()





