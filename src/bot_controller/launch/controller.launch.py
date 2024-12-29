from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, OpaqueFunction, IncludeLaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition, IfCondition

def noisy_controller(context,*args,**kwargs):
    use_sim_time = LaunchConfiguration("use_sim_time")
    wheel_radius = float(LaunchConfiguration("wheel_radius").perform(context))
    wheel_separation = float(LaunchConfiguration("wheel_separation").perform(context))
    wheel_radius_error = float(LaunchConfiguration("wheel_radius_error").perform(context))
    wheel_separation_error = float(LaunchConfiguration("wheel_separation_error").perform(context))

    noisy_controller_py = Node(
    package="bot_controller",
    executable="noisy_controller.py",
    parameters=[
        {"wheel_radius": wheel_radius + wheel_radius_error,
            "wheel_separation": wheel_separation + wheel_separation_error,
            "use_sim_time": use_sim_time}]
    )

    return [
        noisy_controller_py
    ]


def generate_launch_description():

    bumperbot_controller_pkg = get_package_share_directory('bot_controller')
    
    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="True",
    )
    use_simple_controller_arg = DeclareLaunchArgument(
        "use_simple_controller",
        default_value="True",
    )
    use_python_arg = DeclareLaunchArgument(
        "use_python",
        default_value="True",
    )
    wheel_radius_arg = DeclareLaunchArgument(
        "wheel_radius",
        default_value="0.033",
    )
    wheel_separation_arg = DeclareLaunchArgument(
        "wheel_separation",
        default_value="0.17",
    )
    wheel_radius_error_arg = DeclareLaunchArgument(
        "wheel_radius_error",
        default_value="0.005",
    )
    wheel_separation_error_arg = DeclareLaunchArgument(
        "wheel_separation_error",
        default_value="0.02",
    )
    
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_simple_controller = LaunchConfiguration("use_simple_controller")
    use_python = LaunchConfiguration("use_python")
    wheel_radius = LaunchConfiguration("wheel_radius")
    wheel_separation = LaunchConfiguration("wheel_separation")

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    wheel_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["bot_controller", 
                   "--controller-manager", 
                   "/controller_manager"
        ],
        condition=UnlessCondition(use_simple_controller),
    )

    simple_controller = GroupAction(
        condition=IfCondition(use_simple_controller),
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=["simple_velocity_controller", 
                           "--controller-manager", 
                           "/controller_manager"
                ]
            ),
            Node(
                package="bot_controller",
                executable="simple_controller.py",
                parameters=[
                    {"wheel_radius": wheel_radius,
                    "wheel_separation": wheel_separation,
                    "use_sim_time": use_sim_time}],
                condition=IfCondition(use_python),
            )
        ]
    )

    noisy_controller_launch=OpaqueFunction(function=noisy_controller)

    twist_mux_launch = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("twist_mux"),
            "launch",
            "twist_mux_launch.py"
        ),
        launch_arguments={
            "cmd_vel_out": "bot_controller/cmd_vel_unstamped",
            "config_locks": os.path.join(bumperbot_controller_pkg, "config", "twist_mux_locks.yaml"),
            "config_topics": os.path.join(bumperbot_controller_pkg, "config", "twist_mux_topics.yaml"),
            "config_joy": os.path.join(bumperbot_controller_pkg, "config", "twist_mux_joy.yaml"),
            "use_sim_time": LaunchConfiguration("use_sim_time"),
        }.items(),
    )

    twist_relay_node = Node(
        package="bot_controller",
        executable="twist_relay.py",  
        name="twist_relay",
        parameters=[{"use_sim_time": LaunchConfiguration("use_sim_time")}]
    )

    return LaunchDescription(
        [
            use_sim_time_arg,
            use_simple_controller_arg,
            use_python_arg,
            wheel_radius_arg,
            wheel_separation_arg,
            joint_state_broadcaster_spawner,
            wheel_controller_spawner,
            wheel_radius_error_arg,
            wheel_separation_error_arg,
            #twist_relay_node,
            #twist_mux_launch,
            #noisy_controller_launch,
            #simple_controller
        ]
    )