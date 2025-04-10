
ros2 launch description gazebo.launch.py

ros2 launch bot_controller controller.launch.py

velocity commands - 
ros2 topic pub /bot_controller/cmd_vel geometry_msgs/msg/TwistStamped "header:
  stamp:
    sec: 0
    nanosec: 0
  frame_id: ''
twist:
  linear:
    x: 0.0
    y: 0.0
    z: 0.0
  angular:
    x: 0.0
    y: 0.0
    z: 0.0" 

Keyboard teleop - with simple_controller
ros2 run key_teleop key_teleop --ros-args -r key_vel:=bot_controller/cmd_vel -p twist_stamped_enabled:=True



with diff_drive_controller : 
ros2 launch bot_controller controller.launch.py use_simple_controller:=False

ros2 run key_teleop key_teleop --ros-args -r key_vel:=bot_controller/cmd_vel -p twist_stamped_enabled:=True

reading odometry data - can be read from both keyboard teleop and velocity commands 
ros2 topic echo /bot_controller/odom --no-arr  
[--no-arr means there is no covariance matrix will be displayed hence leading to cleaner data representation]

launch gazebo with custom world
ros2 launch description gazebo.launch.py world_name:=small_house

launch noisy_controller :
launch plotjuggler using ros2 run plotjuggler plotjuggler
to visualise the velocity plots of noisy and ideal odometry measurements

use kalman filter to filter out noisy angular velocity by running kalman_filter.py node
ros2 run bot_localization kalman_filter.py

this can be plotted in plotjuggler for visualisation

now to use twist_mux use only this command to use keyboard teleop
ros2 run key_teleop key_teleop --ros-args -r key_vel:=input_joy/cmd_vel_stamped -p twist_stamped_enabled:=True

publish safety_stop msgs
ros2 topic pub /safety_stop std_msgs/msg/Bool "data: false" 

use safety_stop node - 
ros2 run bot_utils safety_stop.py

for running map_server - 
ros2 launch bot_localization global_localization.launch.py
rviz2
ros2 lifecycle set /map_server 1
ros2 lifecycle set /map_server 3

run mapping with known poses using occupancy grid mapping
ros2 run bot_mapping mapping_with_known_poses.py 

launch slam_toolbox
ros2 launch bot_mapping slam.launch.py