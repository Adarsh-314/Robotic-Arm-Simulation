# 4-DOF Robotic Arm Simulation

A ROS 2-based 4-degree-of-freedom robotic arm simulation built around the `arm_description` package. This project includes:

- a URDF/xacro robot model with inertial, visual, and collision definitions
- a Gazebo simulation launch file with `gazebo_ros2_control`
- RViz display configuration for live robot visualization
- a position controller package for interactive joint angle commands
- ROS 2 controller configuration for `joint_state_broadcaster` and `JointGroupPositionController`

## Project Overview

The simulated arm has 4 actively controlled revolute joints:

1. `joint1` — base yaw
2. `joint2` — shoulder pitch
3. `joint3` — elbow pitch
4. `joint4` — wrist pitch

The arm is defined in `src/arm_description/urdf/arm.urdf.xacro` and is loaded into Gazebo and RViz through ROS 2 launch files.

## Repository Structure

```
ros2_ws/
  README.md
  src/
    arm_description/
      CMakeLists.txt
      package.xml
      config/
        arm_controllers.yaml
        rviz_config.rviz
      launch/
        gazebo.launch.py
        display.launch.py
      scripts/
        arm_controller.py
      urdf/
        arm.urdf.xacro
```

## Key Components

### URDF Model

File: `src/arm_description/urdf/arm.urdf.xacro`

- Defines a 4-DOF robotic arm welded to a base
- Uses `xacro` macros to compute inertia for cylindrical links
- Sets realistic joint limits and dynamics
- Includes a `gazebo_ros2_control` plugin for simulation hardware interface
- Exposes ROS 2 control interfaces for command and state

### Controller Configuration

File: `src/arm_description/config/arm_controllers.yaml`

- Configures `controller_manager` update rate
- Loads `joint_state_broadcaster`
- Loads `arm_controller` as a `position_controllers/JointGroupPositionController`
- Maps joint position commands to the four joints

### RViz Configuration

File: `src/arm_description/config/rviz_config.rviz`

- Preconfigured `Grid`, `RobotModel`, and `TF` displays
- Fixed frame set to `world`
- Designed to show the robot model from the `/robot_description` topic

### Launch Files

- `src/arm_description/launch/gazebo.launch.py` — starts Gazebo, spawns the arm, loads controllers, and opens RViz
- `src/arm_description/launch/display.launch.py` — launches RViz and joint state publisher GUI for offline URDF inspection

### Interactive Controller

File: `src/arm_description/scripts/arm_controller.py`

- Provides a CLI to command the arm by specifying joint angles in degrees
- Publishes joint commands to `/arm_controller/commands`
- Validates joint angles against configured limits
- Supports `home` and `quit` commands

## Features

- Gazebo-based physics simulation with ROS 2 control
- Live RViz visualization of robot state
- Joint-level interactive control via Python CLI
- Modular package layout ready for extension
- ROS 2-native launch architecture

## Dependencies

This package requires a ROS 2 installation with support for:

- `ament_cmake`
- `rclpy`
- `std_msgs`
- `sensor_msgs`
- `geometry_msgs`
- `trajectory_msgs`
- `robot_state_publisher`
- `joint_state_publisher`
- `joint_state_publisher_gui`
- `xacro`
- `gazebo_ros`
- `gazebo_ros2_control`
- `ros2_control`
- `ros2_controllers`
- `controller_manager`

Additional recommended dependencies:

- a desktop install of ROS 2 with Gazebo support
- Python 3.10+ for `rclpy` scripts
- `colcon` build tools

Install missing packages using your ROS 2 distro package manager, for example:

```bash
sudo apt update
sudo apt install ros-<ros2-distro>-desktop ros-<ros2-distro>-gazebo-ros-pkgs ros-<ros2-distro>-gazebo-ros2-control
```

## Clone the Repository

To use this project on a different machine, clone the repository and create a ROS 2 workspace:

```bash
cd ~/projects
git clone https://github.com/Adarsh-314/Robotic-Arm-Simulation.git arm_description_ws
cd arm_description_ws
```

If the source tree already contains `ros2_ws`, use the workspace root directly:

```bash
cd /path/to/ros2_ws
```

## Quick Start

From the workspace root, source the ROS 2 environment and build the package:

```bash
source /opt/ros/<ros2-distro>/setup.bash
colcon build --packages-select arm_description
```

Once the build is complete, source the workspace overlay:

```bash
source install/setup.bash
```

## Launching on a New Device

After cloning and building, run the full simulation with:

```bash
ros2 launch arm_description gazebo.launch.py
```

If you only want to inspect the URDF and control joints manually in RViz:

```bash
ros2 launch arm_description display.launch.py
```

## Running the Simulation

### Run the Gazebo + RViz simulation

```bash
ros2 launch arm_description gazebo.launch.py
```

This launch file will:

- start Gazebo with an empty world
- process the arm URDF and publish `/robot_description`
- spawn the robot model in Gazebo
- load `joint_state_broadcaster`
- load `arm_controller`
- open RViz with the provided configuration

### Run the URDF display and joint GUI

```bash
ros2 launch arm_description display.launch.py
```

This is useful for inspecting the robot model and moving joints manually with the joint state publisher GUI.

## Interactive Arm Control

Run the controller CLI after sourcing the workspace:

```bash
ros2 run arm_description arm_controller.py
```

Example interaction:

- `0, 45, -30, 20` — send four joint angles in degrees
- `home` — move all joints to `0°`
- `quit` — exit the CLI

Joint limits enforced by the CLI:

- `joint1` (base yaw): `-180°` to `180°`
- `joint2` (shoulder): `-90°` to `90°`
- `joint3` (elbow): `-90°` to `90°`
- `joint4` (wrist): `-90°` to `90°`

## How It Works

1. The URDF file defines the robot geometry, joints, and physical properties.
2. The Gazebo ROS 2 control plugin exposes robotic joints to the `ros2_control` framework.
3. `joint_state_broadcaster` publishes current joint states.
4. `JointGroupPositionController` accepts joint position commands from the CLI script.
5. RViz visualizes the robot model using the `robot_description` topic.

## Useful ROS 2 Topics and Commands

- `/robot_description` — URDF string published by `robot_state_publisher`
- `/tf` — transform tree published by `robot_state_publisher`
- `/arm_controller/commands` — position commands published by the interactive script

Controller commands:

```bash
ros2 control list_controllers
ros2 control load_controller --set-state active joint_state_broadcaster
ros2 control load_controller --set-state active arm_controller
```

## Extending the Project

Potential next steps:

- add a gripper end effector
- add force/torque sensors or cameras
- implement trajectory following with `FollowJointTrajectoryController`
- add a motion planning stack such as MoveIt 2

## License

This project is configured for `Apache-2.0` as specified in `src/arm_description/package.xml`.

## Notes for GitHub

If you are publishing this project to GitHub, follow these steps:

```bash
git init
git add .
git commit -m "Add 4-DOF robotic arm simulation project"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

If the repository already exists, clone it on another machine with:

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

Then create a ROS 2 workspace if needed, or use the package directly in `src/` if the repository contains `ros2_ws`.

- Add this `README.md` to the root of your workspace
- Commit the file and push it to your repository
- If you want, add a GitHub `LICENSE` and `.gitignore` for ROS workspaces
