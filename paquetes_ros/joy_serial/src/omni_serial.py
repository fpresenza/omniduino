#!/usr/bin/env python

import rospy
import serial
from geometry_msgs.msg import Twist # Twist


def cmd_vel_callback(cmd_vel):

    rospy.loginfo("[OMNI] new command published on /cmd_vel topic")
    rospy.loginfo("[OMNI] cmd_vel: x = %s \t y = %s \t yaw = %s", cmd_vel.linear.x, cmd_vel.linear.y, cmd_vel.angular.z)

    cmd_vel_x = "{:.2f}".format(cmd_vel.linear.x)
    cmd_vel_y = "{:.2f}".format(cmd_vel.linear.y)
    cmd_vel_yaw = "{:.2f}".format(cmd_vel.angular.z)

    data = "r" + "v" + cmd_vel_x + "," + cmd_vel_y + "," + cmd_vel_yaw + "\n"

    s.write(data.encode())

    #print data
    #print len(data)


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

""" subscribes to /cmd_vel topic where teleop_twist_joy node publishes """
cmd_vel_sub = rospy.Subscriber(name='cmd_vel', data_class=Twist, callback=cmd_vel_callback, queue_size=1)

rospy.loginfo("OMNIDUINO succesfully initialized.")

""" Spin """ 
rospy.spin()
