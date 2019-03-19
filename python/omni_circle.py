import time
import serial
import math
import os
from datetime import datetime

#################################
# CLEAR SCREEN
os.system('clear')

#################################
# SET UP SERIAL PORT

s = serial.Serial()
s.port = '/dev/ttyUSB0'
s.baudrate = 115200
s.bytesize = 8
s.parity = 'N'
s.stopbits = 1
s.timeout = 0.1
s.open()

#################################
# CREATE FILE TO SAVE DATA

# Get path of data files
current_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(current_path, "ensayos/")

# Set format of file name
FORMAT = '%Y%m%d_%H:%M'
f_name = '%s_%s%s' % ("Omni", datetime.now().strftime(FORMAT), ".txt")

# Write file name in "names_file.txt"
names = open(os.path.join(data_path, "names_file.txt"), "a+", encoding='utf-8')
names.write(f_name + "\n")
names.close()

# Creat file to write data in pre-set path
f_path = os.path.join(data_path, f_name)
f = open(f_path, "a+", encoding='utf-8')
f.close()

#################################
# GET TRAJECTORY PARAMETERS FROM USER

# READ INPUT FOR CENTER
correct_input = False
while not correct_input:
    Cx = input("Enter \'x\' coordinate of center in m [Enter: 0]: ")
    Cy = input("Enter \'y\' coordinate of center in m [Enter: 0]: ")
    try:
        if Cx == '':
            Cx = 0
        if Cy == '':
            Cy = 0
        Cx = float(Cx)
        Cy = float(Cy)
        correct_input = True
    except:
        print("Invalid data type")

# READ INPUT FOR VELOCITY
correct_input = False
while not correct_input:
    V = input("Enter linear velocity in m/s (<=0.3): ")
    try:
        V = float(V)
        if V > 0.3:
            print("Velocity to big")
        elif V <= 0:
            print("Zero or negative velocity not allowed")
        else:
            correct_input = True
    except:
        print("Invalid data type")

# READ INPUT FOR RADIUS
correct_input = False
while not correct_input:
    R = input("Enter radius of circle in m (<2): ")
    try:
        R = float(R)
        if R>2:
            print("Radius to big")
        elif R<=0:
            print("Zero or negative radius not allowed")
        else:
            correct_input = True
    except:
        print("Invalid data type")

# READ INPUT FOR HEADING BEHAVIOR
correct_input = False
follower = 0
while not correct_input:
    heading = input("Insert heading angle in grad: ")
    mode = input("Follow trajectory [y/N]: ")
    try:
        if heading == '':
            heading = 0
        heading = float(heading) * math.pi/180
        correct_input = True
        if mode == 'y' or mode == 'Y':
            follower = 1
        elif mode == 'n' or mode == 'N' or mode == '':
            follower = 0
        else:
            print("Invalid input")
            correct_input = False
    except:
        print("Invalid data type")

# READ INPUT FOR TOTAL NUMBER OF LAPS
correct_input = False
while not correct_input:
    m = input("Enter total number of laps (>0) [Enter: 1]: ")
    try:
        if m == '':
            m = 1
        m = float(m)
        if m<=0:
            print("Zero or negative number of laps not allowed")
        else:
            correct_input = True
    except:
        print("Invalid data type")

#################################
# PLACE OMNIDUINO IN ORIGIN OF TRAJECTORY

pXRef = round(R * math.cos(0) + Cx, 3)
pYRef = round(R * math.sin(0) + Cy, 3)
YawRef = heading * 180/math.pi
preAngle = heading
YawLap = 0
print("\tX = ", pXRef)
print("\tY = ", pYRef)
print("\tYaw = ", YawRef)


set_ref = "p" + "x" + str(pXRef) + "y" + str(pYRef) + "w" + str(YawRef) + "r" +"\n"
i=0
while i < 5:
    s.flushInput()
    s.write(set_ref.encode())
    i += 1
s.flushOutput()

#################################
# INITIALIZE VARIABLES, INIT TIMER & FLUSH INPUT BUFFER

Period = (2*math.pi)/(V/R)

omni_t = []
omni_px = []
omni_py = []
omni_yaw = []

#################################3
# BEGIN ROUTINE

os.system('clear')
while True:
    cmd = input("\nPress Enter to Start:")
    try:
        if cmd == '':
            break
    except:
        pass
print("Total simulation time: ", round(m*Period, 2), "s")
print("Running simulation...")
new_data = False
s.flushInput()
ts = 0
init_time = time.time()

while ts < m*Period:
    # GET OMNI POSITION REFERENCE
    ts = time.time() - init_time
    pXRef = round(R * math.cos((V/R) * ts) + Cx, 3)
    pYRef = round(R * math.sin((V/R) * ts) + Cy, 3)

    Angle = heading + follower * V/R * ts

    if Angle - preAngle < -5:
        YawLap += 1
    elif Angle - preAngle > 5:
        YawLap -= 1

    preAngle = Angle
    YawRef = (Angle + YawLap * 2 * math.pi) * 180 / math.pi
    YawRef = round(YawRef, 3)


    # SEND OMNI POSITION REFERENCE
    set_ref = "p" + "x" + str(pXRef) + "y" + str(pYRef) + "w" + str(YawRef) + "r" + "\n"
    s.write(set_ref.encode())

    # READ DATA FROM OMNIDUINO & APPEND TO FILE
    while s.in_waiting > 0:
        data_in_raw = s.readline()  # Read raw data from Serial Port
        data_in_str = data_in_raw.decode("utf-8")[:-2]
        ref_str = str(pXRef) + "," + str(pYRef) + "," + str(YawRef)
        data2file = data_in_str + "," + ref_str + "\n"

        try:
            f = open(f_path, "a+", encoding='utf-8')
            f.write(data2file)  # Append data to .txt file
            f.close()
        except:
            print("Unable to write text file.")

    time.sleep(0.025)

eof_str = str("\t\n")
f = open(f_path, "a+", encoding='utf-8')
f.write(eof_str)
f.close()

print("Simulation finished...")

s.flushInput()
s.flushOutput()
s.close()
