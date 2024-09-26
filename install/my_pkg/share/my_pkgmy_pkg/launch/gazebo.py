import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.descriptions import Parameter

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gazebo_ros',
            executable='gazebo',
            name='gazebo',
            output='screen',
            arguments=['-s', 'libgazebo_ros_factory.so']
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': open('/home/looubuntu/ros2_ws/src/my_pkg/urdf/car_SLDASM.urdf').read()}]
        ),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_entity',
            output='screen',
            arguments=['-entity', 'my_robot', '-file', '/home/looubuntu/ros2_ws/src/my_pkg/urdf/car_SLDASM.urdf']
        ),
    ])
