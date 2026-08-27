"""Launch one profiled robot/tool pair in Gazebo Harmonic."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    robot = LaunchConfiguration("robot")
    model = LaunchConfiguration("model")
    tool = LaunchConfiguration("tool")
    world = LaunchConfiguration("world")
    description = Command([
        FindExecutable(name="xacro"), " ",
        PathJoinSubstitution([FindPackageShare("dfl_manipulation_toolbox"), "urdf", "dfl_robot.urdf.xacro"]),
        " robot:=", robot, " arm_model:=", model, " tool:=", tool,
        " namespace:=", robot, " control_backend:=gazebo",
    ])
    parameters = [{"robot_description": ParameterValue(description, value_type=str), "use_sim_time": True}]
    start_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare("ros_gz_sim"), "/launch/gz_sim.launch.py"]),
        launch_arguments={"gz_args": ["-r -s -v 3 ", world]}.items(),
        condition=IfCondition(LaunchConfiguration("start_gazebo")),
    )
    state_publisher = Node(
        package="robot_state_publisher", executable="robot_state_publisher", namespace=robot,
        parameters=parameters, output="screen", remappings=[("/tf", "tf"), ("/tf_static", "tf_static")],
    )
    spawn = Node(
        package="ros_gz_sim", executable="create", namespace=robot, output="screen",
        arguments=["-topic", "robot_description", "-name", robot, "-allow_renaming", "false",
                   "-x", LaunchConfiguration("x"), "-y", LaunchConfiguration("y"), "-z", LaunchConfiguration("z")],
    )
    controller = Node(
        package="controller_manager", executable="spawner", namespace=robot, output="screen",
        arguments=["dsr_position_controller", "--controller-manager", "controller_manager", "--controller-manager-timeout", "30"],
    )
    joint_states = Node(
        package="controller_manager", executable="spawner", namespace=robot, output="screen",
        arguments=["joint_state_broadcaster", "--controller-manager", "controller_manager", "--controller-manager-timeout", "30"],
    )
    clock_bridge = Node(
        package="ros_gz_bridge", executable="parameter_bridge", output="screen",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"],
        condition=IfCondition(LaunchConfiguration("start_gazebo")),
    )
    adapter = Node(
        package="dfl_manipulation_toolbox", executable="dfl-trajectory-adapter",
        arguments=["--robot", robot], output="screen", parameters=[{"use_sim_time": True}],
    )
    sim_io = Node(
        package="dfl_manipulation_toolbox", executable="dfl-sim-io",
        arguments=["--robot", robot, "--tool", tool, "--publish-camera"], output="screen",
        parameters=[{"use_sim_time": False}],
    )
    return LaunchDescription([
        DeclareLaunchArgument("robot", default_value="picker1", choices=["picker1", "picker2", "h2515"]),
        DeclareLaunchArgument("model", default_value="m1013", choices=["m1013", "h2515"]),
        DeclareLaunchArgument("tool", default_value="vgc10_1cup", choices=["vgc10_1cup", "vgc10_4cup", "vgp20", "2fg14"]),
        DeclareLaunchArgument("x", default_value="0.0"), DeclareLaunchArgument("y", default_value="0.0"),
        DeclareLaunchArgument("z", default_value="0.0"), DeclareLaunchArgument("start_gazebo", default_value="true"),
        DeclareLaunchArgument("world", default_value=PathJoinSubstitution([FindPackageShare("dfl_manipulation_toolbox"), "scenes", "empty", "world.sdf"])),
        start_gazebo,
        state_publisher, spawn, clock_bridge, TimerAction(period=4.0, actions=[joint_states, controller]),
        TimerAction(period=6.0, actions=[adapter, sim_io]),
    ])
