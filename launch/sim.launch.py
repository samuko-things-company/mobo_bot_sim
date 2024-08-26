import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
 
def generate_launch_description():
 
  # Set the path to the Gazebo ROS package
  gazebo_pkg = get_package_share_directory('gazebo_ros')
   
  # Set the path to this package.
  my_pkg=get_package_share_directory('mobo_bot_sim')
  my_robot_view_pkg = get_package_share_directory('mobo_bot_rviz')
 
  # Set the path to the world file
  world_file_name = 'test_world.world'
  world_path = os.path.join(my_pkg, 'world', world_file_name)

  use_rviz = 'False' # you can change to 'True' or 'False'
 
  ########### YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE ##############  
  # Launch configuration variables specific to simulation
  headless = LaunchConfiguration('headless')
  use_sim_time = LaunchConfiguration('use_sim_time')
  use_simulator = LaunchConfiguration('use_simulator')
  world = LaunchConfiguration('world')
  view_robot_in_rviz = LaunchConfiguration('view_robot_in_rviz')
 
  declare_headless_cmd = DeclareLaunchArgument(
    name='headless',
    default_value='False',
    description='Whether to run only gzserver')
     
  declare_use_sim_time_cmd = DeclareLaunchArgument(
    name='use_sim_time',
    default_value='True',
    description='Use simulation (Gazebo) clock if true')
 
  declare_use_simulator_cmd = DeclareLaunchArgument(
    name='use_simulator',
    default_value='True',
    description='Whether to start the simulator')
 
  declare_world_cmd = DeclareLaunchArgument(
    name='world',
    default_value=world_path,
    description='Full path to the world model file to load')
  
  declare_view_robot_in_rviz_cmd = DeclareLaunchArgument(
        'view_robot_in_rviz',
        default_value=use_rviz,
        description='whether to run run rviz or not')
    
  # Specify the actions
   
  # Start Gazebo server
  start_gazebo_server_cmd = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(gazebo_pkg, 'launch', 'gzserver.launch.py')),
    condition=IfCondition(use_simulator),
    launch_arguments={'world': world}.items())
 
  # Start Gazebo client    
  start_gazebo_client_cmd = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(gazebo_pkg, 'launch', 'gzclient.launch.py')),
    condition=IfCondition(PythonExpression([use_simulator, ' and not ', headless])))
 

  rsp = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([os.path.join(my_pkg,'launch','rsp.launch.py')]), 
    launch_arguments={'use_sim_time': use_sim_time}.items())
  
  view_robot = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [os.path.join(my_robot_view_pkg,'launch','sim.launch.py')]
            ), 
            condition=IfCondition(view_robot_in_rviz)
    )
  

  robot_name = 'mobo_bot'
  # initial spawn position
  x_pos = 0; y_pos = 0; z_pos = 0
  #initial spawn orientation
  roll = 0; pitch = 0; yaw = 0
  
  # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
  spawn_entity = Node(
      package='gazebo_ros', 
      executable='spawn_entity.py',
      arguments=[
          '-topic', '/robot_description',
          '-entity', robot_name,
          '-x', str(x_pos), '-y', str(y_pos), '-z', str(z_pos),
          '-R', str(roll), '-P', str(pitch), '-Y', str(yaw)
          ],
      output='screen')
  
  # Create the launch description
  ld = LaunchDescription()
 
  # add the necessary declared launch arguments to the launch description
  ld.add_action(declare_headless_cmd)
  ld.add_action(declare_use_sim_time_cmd)
  ld.add_action(declare_use_simulator_cmd)
  ld.add_action(declare_world_cmd)
  ld.add_action(declare_view_robot_in_rviz_cmd)
 
  # Add the nodes to the launch description
  ld.add_action(rsp)
  ld.add_action(view_robot)
  ld.add_action(start_gazebo_server_cmd)
  ld.add_action(start_gazebo_client_cmd)
  ld.add_action(spawn_entity)
 
  return ld