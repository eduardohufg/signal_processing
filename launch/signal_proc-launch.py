from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='signal_processing',
            executable='sin_sender',
            name='sin_sender',
            output='screen'
        ),
        Node( 
            package='signal_processing',
            executable='process',
            name='process',
            output='screen'
        ),
        Node(
            package='rqt_plot',
            executable='rqt_plot',
            name='rqt_plot',
            arguments=['/signal/data', 'proc_signal/data']
        )
    ])