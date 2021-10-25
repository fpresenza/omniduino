#!/usr/bin/env python3

import serial
import os
from datetime import datetime

import rospy
from geometry_msgs.msg import Twist, TwistStamped
import rosbag


def cmd_vel_callback(cmd_vel):

    rospy.loginfo("[OMNI] new command published on /cmd_vel topic: x = {:.2f},  y = {:.2f},  yaw = {:.2f}".format(cmd_vel.linear.x, cmd_vel.linear.y, cmd_vel.angular.z))

    cmd_vel_x = "{:.2f}".format(cmd_vel.linear.x)
    cmd_vel_y = "{:.2f}".format(cmd_vel.linear.y)
    cmd_vel_yaw = "{:.2f}".format(cmd_vel.angular.z)

    data_out = "r" + "v" + cmd_vel_x + "," + cmd_vel_y + "," + cmd_vel_yaw + "\n"

    s.write(data_out.encode())


if __name__ == '__main__':

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

    """ Get path of data files """
    current_path = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(current_path, "../data")

    """ Set format of file name """
    #FORMAT = '%Y%m%d_%H:%M'
    FORMAT = '%Y%m%d_%H:%M:%S'

    #f_name = '%s_%s%s' % ("omni", datetime.now().strftime(FORMAT), ".txt")
    f_name = '%s_%s%s' % ("omni", datetime.now().strftime(FORMAT), ".txt")

    """ Create file to write data in pre-set path """
    f_path = os.path.join(data_path, f_name)
    f = open(f_path, "a+")
    f.close()

    """ Creat bag file """
    bag = rosbag.Bag('test.bag', 'w')

    """ subscribes to /cmd_vel topic where teleop_twist_joy node publishes """
    cmd_vel_sub = rospy.Subscriber(name='cmd_vel', data_class=Twist, callback=cmd_vel_callback, queue_size=1)

    """ publishes to /omni_pose topic """
    pose_pub = rospy.Publisher(name='omni_pose', data_class=TwistStamped, queue_size=1, latch=True)

    rospy.loginfo("OMNIDUINO succesfully initialized.")


    #i = 0.0

    """ Wait for data in serial buffer """ 
    rate = rospy.Rate(20)

    while not rospy.is_shutdown():

        if s.in_waiting > 0:

            if s.read(1) != 'a':
                s.readline()
                continue

            data_in = s.readline()  # Read raw data from Serial Port

        #if True:

            #data_in = "0.55,1.11,2.22,3.33,4,7,2\n"

            print(data_in)

            try:
                f = open(f_path, 'a+')
                f.write(data_in)
                f.close()
            except:
                rospy.loginfo("Unable to write text file.")
            
            values = data_in[:-1].split(',')
            #print(values)

            #values[0] = float(values[0]) +  float(i/10) #  comentar

            pose = TwistStamped()

            timestamp = float(values[0])

            tsecs = int(timestamp)
            msecs = (timestamp - tsecs)

            pose.header.stamp.secs = float(values[0])
            pose.header.stamp.nsecs = msecs * 10**9
            pose.twist.linear.x = float(values[1])  # + i/100
            pose.twist.linear.y = float(values[2])  #+ i/100
            pose.twist.angular.z = float(values[3])

            pose_pub.publish(pose)

            bag.write('omni_pose', pose)

            #i += 1        

            #if i == 500:    break    
        
        rate.sleep()

    bag.close()
    s.close()
    rospy.loginfo("OMNIDUINO serial communication shut down.")
