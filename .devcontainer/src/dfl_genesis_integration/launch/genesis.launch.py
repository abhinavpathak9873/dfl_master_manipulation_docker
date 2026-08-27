"""Launch one profiled robot/tool pair through the direct Genesis bridge."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    robot = LaunchConfiguration("robot")
    model = LaunchConfiguration("model")
    tool = LaunchConfiguration("tool")
    description = Command([
        FindExecutable(name="xacro"), " ",
        PathJoinSubstitution([FindPackageShare("dfl_manipulation_toolbox"), "urdf", "dfl_robot.urdf.xacro"]),
        " robot:=", robot, " arm_model:=", model, " tool:=", tool,
        " namespace:=", robot, " control_backend:=none",
    ])
    state_publisher = Node(
        package="robot_state_publisher", executable="robot_state_publisher", namespace=robot,
        parameters=[{"robot_description": ParameterValue(description, value_type=str), "use_sim_time": True}],
        remappings=[("/tf", "tf"), ("/tf_static", "tf_static")], output="screen",
    )
    bridge = ExecuteProcess(
        cmd=["/opt/genesis-venv/bin/python", "-m", "dfl_genesis_integration.bridge",
             "--robot", robot, "--model", model, "--tool", tool,
             "--backend", LaunchConfiguration("backend"), "--headless"],
        output="screen",
    )
    sim_io = Node(
        package="dfl_manipulation_toolbox", executable="dfl-sim-io", output="screen",
        arguments=["--robot", robot, "--tool", tool], parameters=[{"use_sim_time": True}],
    )
    return LaunchDescription([
        DeclareLaunchArgument("robot", default_value="picker1", choices=["picker1", "picker2", "h2515"]),
        DeclareLaunchArgument("model", default_value="m1013", choices=["m1013", "h2515"]),
        DeclareLaunchArgument("tool", default_value="vgc10_1cup", choices=["vgc10_1cup", "vgc10_4cup", "vgp20", "2fg14"]),
        DeclareLaunchArgument("backend", default_value="auto", choices=["auto", "cuda", "cpu"]),
        state_publisher, bridge, sim_io,
    ])
