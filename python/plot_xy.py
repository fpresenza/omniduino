import time
import os
import matplotlib.pyplot as plt

#################################
# CLEAR SCREEN
os.system('clear')

#################################
# GET NAME OF DATA FILE AND OPEN

# Get path of data files
current_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(current_path, "ensayos/")

# Read file name for user or assign to last file created
correct_input = False
while not correct_input:
    f_name = input("Enter file name to save data [Enter: last file created]: ")
    try:
        if f_name == '':

            # Get last file created name
            names = open(os.path.join(data_path, "names_file.txt"), "r+", encoding='utf-8')
            f_name = names.readlines()[-1][:-1]
            names.close()

            # Get last file created path
            f_path = os.path.join(data_path, f_name)
        else:
            f_path = os.path.join(data_path, f_name)


        correct_input = True
    except:
        print("Invalid file name. ")

#################################
# SET FIGURE PARAMETERS
# Set plot to animated
plt.ion()

# Initialize variables
pXRef = []
pYRef = []
omni_px = []
omni_py = []

fig1 = plt.figure()
fig1.suptitle('Real Time Robot Position', fontsize='18', fontweight='bold')
plt.xlabel('x [m]', fontsize='14')
plt.ylabel('y [m]', fontsize='14')
plt.axes().grid(True)
line1, = plt.plot(pYRef, color='red', marker='x')
line2, = plt.plot(omni_py, color='blue', marker='o')


#################################
# READ DATA FROM FILE
f = open(f_path, "r+", encoding='utf-8')
while True:
    if f.readable():
        line = f.readline() # Read raw data from file
        if line == '':
            continue
        elif line == "\t\n":
            break
        else:
            try:
                # Convert raw data to string list
                if isinstance(line, str):
                    values = line[:-1].split(",")
                    #print(values)

                    # Create float lists of variables to plot
                    try:
                        omni_px.append(float(values[1]))
                    except:
                        pass
                    try:
                        omni_py.append(float(values[2]))
                    except:
                        pass
                    try:
                        pXRef.append(float(values[4]))
                    except:
                        pass
                    try:
                        pYRef.append(float(values[5]))
                    except:
                        pass
                    print(omni_px[-1], omni_py[-1], pXRef[-1], pYRef[-1])

                    # Define plot lines
                    # Line 1
                    line1.set_xdata(pXRef[-20:-1])
                    line1.set_ydata(pYRef[-20:-1])
                    # Line 2
                    line2.set_xdata(omni_px[-20:-1])
                    line2.set_ydata(omni_py[-20:-1])

                    xmin = min(-1, min(pXRef) * 1.25, min(omni_px) * 1.25)
                    xmax = max(1,  max(pXRef) * 1.25, max(omni_px) * 1.25)
                    ymin = min(-1, min(pYRef) * 1.25, min(omni_py) * 1.25)
                    ymax = max(1,  max(pYRef) * 1.25, max(omni_py) * 1.25)

                    plt.xlim(xmin, xmax)
                    plt.ylim(ymin, ymax)
                    fig1.canvas.draw()
                else:
                    print("Non-string data.")
            except:
                "Unable to plot."
                pass
    else:
        print("File not readable.")
    time.sleep(0.05)
f.close()