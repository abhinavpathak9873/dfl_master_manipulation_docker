"""Launch Picker 1 and Picker 2 into one Gazebo world with isolated ROS names."""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    launch_file = PathJoinSubstitution(
        [FindPackageShare("dfl_manipulation_toolbox"), "launch", "gazebo.launch.py"]
    )
    picker1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(launch_file),
        launch_arguments={"robot": "picker1", "model": "m1013", "tool": "vgc10_1cup", "y": "-1.0", "start_gazebo": "true"}.items(),
    )
    picker2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(launch_file),
        launch_arguments={"robot": "picker2", "model": "m1013", "tool": "2fg14", "y": "1.0", "start_gazebo": "false"}.items(),
    )
    return LaunchDescription([picker1, picker2])
