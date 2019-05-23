#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

import serial
import os
from datetime import datetime

import codecs



def cmd_vel_callback(cmd_vel):

    #rospy.loginfo("[OMNI] new command published on /cmd_vel topic")
    rospy.loginfo("[OMNI] new command published on /cmd_vel topic: x = {:.2f},  y = {:.2f},  yaw = {:.2f}".format(cmd_vel.linear.x, cmd_vel.linear.y, cmd_vel.angular.z))

    cmd_vel_x = "{:.2f}".format(cmd_vel.linear.x)
    cmd_vel_y = "{:.2f}".format(cmd_vel.linear.y)
    cmd_vel_yaw = "{:.2f}".format(cmd_vel.angular.z)

    data_out = "r" + "v" + cmd_vel_x + "," + cmd_vel_y + "," + cmd_vel_yaw + "\n"

    s.write(data_out.encode())


""" Inicializar nodo """
rospy.init_node('omni_serial')

""" Set up serial port """
s = serial.Serial()
s.port = '/dev/ttyUSB0'
s.baudrate = 115200
s.bytesize = 8
s.parity = 'N'
s.stopbits = 1
s.timeout = 0.1
s.open()
s.flushInput()
s.flushOutput()
s.write("rv0,0,0".encode())

""" Set textfile to save data """

# Get path of data files
current_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(current_path, "../data")

# Set format of file name
FORMAT = '%Y%m%d_%H:%M'
f_name = '%s_%s%s' % ("omni", datetime.now().strftime(FORMAT), ".txt")

# Creat file to write data in pre-set path
f_path = os.path.join(data_path, f_name)
f = open(f_path, "a+")
f.close()


""" subscribes to /cmd_vel topic where teleop_twist_joy node publishes """
cmd_vel_sub = rospy.Subscriber(name='cmd_vel', data_class=Twist, callback=cmd_vel_callback, queue_size=1)

rospy.loginfo("OMNIDUINO succesfully initialized.")





""" Wait for data in serial buffer """ 
rate = rospy.Rate(20)

while not rospy.is_shutdown():

    if s.in_waiting > 0:

        if s.read(1) != 'a':
            s.readline()
            continue

        if s.read(1) != 'p':
            s.readline()
            continue

        data_in = s.readline()  # Read raw data from Serial Port

        print(data_in)

        try:
            f = open(f_path, 'a+')
            f.write(data_in)
            f.close()
        except:
            rospy.loginfo("Unable to write text file.")

    
    rate.sleep()

s.close()
rospy.loginfo("OMNIDUINO serial communication shut down.")
