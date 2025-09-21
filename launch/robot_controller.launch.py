from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    #Path to robot_urdf/launch/gazebo.launch.py
    gazebo_launch = os.path.join(
        get_package_share_directory('robot_urdf'),
        'launch',
        'gazebo.launch.py'
    )

    return LaunchDescription([
        Node(
            package='robot_controller',
            executable='controller',
            name='robot_controller',
            output='screen'
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gazebo_launch)
        )
    ])
