import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    ExecuteProcess,
    IncludeLaunchDescription,
    RegisterEventHandler,
    TimerAction,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    pkg = get_package_share_directory("arm_description")
    gz_pkg = get_package_share_directory("gazebo_ros")

    # nn Process URDF nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
    xacro_file = os.path.join(pkg, "urdf", "arm.urdf.xacro")
    robot_description = xacro.process_file(xacro_file).toxml()
    rviz_config = os.path.join(pkg, "config", "rviz_config.rviz")

    # nn 1. Launch Gazebo (empty world) nnnnnnnnnnnnnnnnnnnn
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gz_pkg, "launch", "gazebo.launch.py")
        ),
        launch_arguments={"world": ""}.items(),
    )

    # nn 2. robot_state_publisher nnnnnnnnnnnnnnnnnnnnnnnnnn
    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": True,
            }
        ],
    )

    # nn 3. Spawn robot into Gazebo nnnnnnnnnnnnnnnnnnnnnnnn
    spawn = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic",
            "robot_description",
            "-entity",
            "arm_4dof",
            "-x",
            "0",
            "-y",
            "0",
            "-z",
            "0.01",
        ],
        output="screen",
    )

    # nn 4. Load joint_state_broadcaster nnnnnnnnnnnnnnnnnnn
    load_jsb = ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "active",
            "joint_state_broadcaster",
        ],
        output="screen",
    )

    # nn 5. Load arm_controller (after broadcaster is active)
    load_arm_ctrl = ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "active",
            "arm_controller",
        ],
        output="screen",
    )

    # nn 6. RViz nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_config],
        parameters=[{"use_sim_time": True}],
        output="screen",
    )

    # nn Event: load arm_ctrl only after broadcaster exits n
    after_jsb = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=load_jsb,
            on_exit=[load_arm_ctrl],
        )
    )

    return LaunchDescription(
        [
            gazebo,
            rsp,
            spawn,
            TimerAction(period=3.0, actions=[load_jsb]),
            after_jsb,
            TimerAction(period=2.0, actions=[rviz]),
        ]
    )
