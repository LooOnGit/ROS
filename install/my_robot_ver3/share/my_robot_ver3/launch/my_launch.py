from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    nodes = []

    nodes.append(        Node(
            package='my_robot_ver3',
            namespace='vd1',
            executable='control',
            output = 'screen',
            name='sim2'
        ))
    
    # for i in range(0,10):
    #     nodes.append(Node(
    #         package='turtlesim',
    #         namespace=f'tt{i+1}',
    #         executable='turtlesim_node',
    #         output='screen',
    #         name=f'loo{i+1}'
    #     ))
    return LaunchDescription(nodes)
