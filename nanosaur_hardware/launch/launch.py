#!/usr/bin/env python3

import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

# this is the function launch  system will look for
def generate_launch_description():

    lime_fizzio_node = Node(
        package='nanosaur_hardware',
        executable='nanosaur',
        parameters=[],
        arguments=[],
        output="screen",
    )

    arduino_sensor_node = Node(
        package='arduino_sensor',
        executable='arduino_sensor',
        parameters=[],
        arguments=[],
        output="screen",
    )

    teleop_node = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        parameters=[],
        arguments=[],
        output="screen",
    )

    # create and return launch description object
    return LaunchDescription(
        [
            lime_fizzio_node,
            arduino_sensor_node,
            teleop_node,
        ]
    )