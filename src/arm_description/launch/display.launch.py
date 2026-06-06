import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    pkg = get_package_share_directory("arm_description")

    # nn Process xacro → URDF string nnnnnnnnnnnnnnnnnnnnnn
    xacro_file = os.path.join(pkg, "urdf", "arm.urdf.xacro")
    robot_description = xacro.process_file(xacro_file).toxml()

    # nn RViz config nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
    rviz_config = os.path.join(pkg, "config", "rviz_config.rviz")

    return LaunchDescription(
        [
            # 1. robot_state_publisher — publishes /tf from URDF
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[{"robot_description": robot_description}],
            ),
            # 2. joint_state_publisher_gui — sliders for each joint
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher_gui",
                output="screen",
            ),
            # 3. RViz2
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=["-d", rviz_config],
            ),
        ]
    )
