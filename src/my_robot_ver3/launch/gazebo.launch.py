import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.event_handlers import OnProcessExit

def generate_launch_description():
    model_arg = DeclareLaunchArgument(name='model', description='Absolute path to robot urdf file')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    use_sim_time = LaunchConfiguration('use_sim_time') 
    package_name = 'my_robot_ver3'
    pkg_share = FindPackageShare(package=package_name).find(package_name)
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros') 

    # Sửa đường dẫn tới room.world
    world_file_path = '/home/looubuntu/ros2_ws/src/my_robot_ver3/world/room.world' # Đường dẫn đầy đủ
    world = LaunchConfiguration('world')
    world_path = world_file_path  # Sử dụng đường dẫn trực tiếp

    # Declare launch arguments
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    # Get package directories
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_share = FindPackageShare(package='my_robot_ver3').find('my_robot_ver3')

    # Path to URDF file
    urdf_file_name = 'my_robot_ver3.urdf'
    urdf = os.path.join(pkg_share, 'urdf', urdf_file_name)

    # Read URDF file
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    # Define nodes
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time'), 'robot_description': robot_desc}],
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
    )

    declare_world_cmd = DeclareLaunchArgument(
        name='room',
        default_value=world_path,
        description='Full path to the world model file to load'
        )

    # Spawn robot in Gazebo
    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            "-topic", "/robot_description",
            "-entity", 'my_robot_ver3',
            "-x", '0.0',
            "-y", '0.0',
            "-z", '0.05',
            "-Y", '0.0'
        ],
        output='screen'
    )

    # Start Gazebo
    gazebo = ExecuteProcess(
        cmd=['gazebo', world_path, '--verbose', '-s', 'libgazebo_ros_factory.so', '-s', 'libgazebo_ros_init.so'],
        output='screen'
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        rviz2,
        robot_state_publisher_node,
        joint_state_publisher_node,
        spawn,
        gazebo
    ])
