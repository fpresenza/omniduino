# OmniDuino: control and estimation for an omnidirectional mobile robot

OmniDuino is an experimental software stack developed for a three-wheeled
omnidirectional ground robot. It combines embedded motor control, onboard
sensing, serial communication, ROS 1 integration, trajectory generation, and
data analysis.

This repository documents a laboratory prototype developed in 2019. It is
provided for reproducibility and as an example of end-to-end robotic-system
integration; it is not a maintained general-purpose robot driver.

## Implemented components

- position and velocity control for a three-wheel omnidirectional platform;
- encoder-based wheel-speed estimation and closed-loop motor control;
- pose estimation using Marvelmind ultrasonic positioning and an HMC5883
  magnetometer;
- serial exchange of velocity commands and telemetry;
- ROS 1 nodes publishing robot pose and subscribing to `cmd_vel`;
- joystick teleoperation;
- circular-trajectory experiments and data logging; and
- MATLAB/Simulink models and Python analysis scripts.

## Repository structure

```text
arduino/            Embedded firmware and sensor/motor interfaces
matlab/             MATLAB and Simulink models
memoria_de_calculo/ Hardware configuration material
paquetes_ros/
  joy_serial/       Project-specific ROS/serial bridge
  teleop_twist_joy/ Third-party Clearpath Robotics package (BSD licensed)
python/             Stand-alone experiment and plotting scripts
```

## Hardware assumptions

The firmware was written for the original laboratory platform and assumes:

- three independently driven omni wheels with encoders;
- a controller compatible with the pin mapping in `arduino/main.ino`;
- Marvelmind ultrasonic indoor positioning;
- an HMC5883 magnetometer; and
- a serial connection at 115200 baud.

Review all pin assignments, motor directions, controller gains, serial devices,
and safety limits before connecting different hardware.

## Software requirements

- Arduino IDE and the libraries required by the included sensors;
- ROS 1 (the current branch targets ROS Noetic);
- ROS packages `rospy`, `geometry_msgs`, `rosbag`, and `joy`;
- Python with `pyserial`, NumPy, and Matplotlib; and
- MATLAB/Simulink for the supplied model.

## Arduino firmware

The Arduino IDE requires the sketch and its local source files to be stored in
a directory with the same name as the `.ino` file. Copy the contents of
`arduino/` into a sketch directory, select the correct target board and serial
port, check the pin mapping, and upload `main.ino`.

## ROS 1 setup

Copy the project-specific package into a catkin workspace and build it:

```bash
mkdir -p ~/catkin_ws/src
cp -r paquetes_ros/joy_serial ~/catkin_ws/src/
cd ~/catkin_ws
catkin_make
source devel/setup.bash
python -m pip install pyserial
```

Update the serial device in `joy_serial/src/omni_serial.py` if the robot is not
available at `/dev/ttyUSB0`. The supplied launch file can then be inspected and
run with:

```bash
roslaunch joy_serial omniduino.launch
```

The repository also contains a historical copy of `teleop_twist_joy`. Prefer
installing the maintained ROS package through your ROS distribution rather than
copying that directory into a new workspace.

## Safety

Test with the wheels raised or motors disconnected first. Verify emergency-stop
behaviour, velocity saturation, motor directions, sensor calibration, and the
reference frame before running the robot on the ground.

## Authorship and third-party software

The OmniDuino-specific firmware, ROS bridge, models, and experiment scripts were
developed by J. Francisco Presenza and collaborators. The bundled
`teleop_twist_joy` package is third-party software from Clearpath Robotics and
retains its BSD licence and authorship information. The Adafruit sensor
interface and HMC5883 driver likewise retain their Apache-2.0 and BSD notices,
respectively.

## Licence

The licence for the OmniDuino-specific code must be stated in a root `LICENSE`
file. Third-party components retain their original licences; see
`paquetes_ros/teleop_twist_joy/LICENSE.txt` and the notices in the relevant
source files.
