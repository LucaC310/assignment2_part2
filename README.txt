# Robot Controller (ROS2)

This repository contains a **ROS2 package** that provides a node called `controller`.

## Related Repository

This project works together with [robot_urdf (ros2 branch)](https://github.com/CarmineD8/robot_urdf/tree/ros2), which provides the robot description used in simulation.

## Overview

The `controller` node implements a simple movement logic to control a robot spawned by the `robot_urdf` package inside a **Gazebo** simulation.

The movement logic defines a repeating trajectory:

- Starting from the spawn position '(2, 2)', the robot moves along the x-axis until it reaches `x = 9.0`.
- When `x > 9.0`, the robot turns in a circular arc and moves back along the x-axis until `x = 2.0`.
- When `x < 2.0`, the robot again turns in a circular arc and repeats the pattern.

## Launch

To start the full simulation, a launch file is provided: `robot_controller.launch.py`.

Running this launch file will:

- Start the `gazebo.launch.py` file
- Launch the `controller` node simultaneously
