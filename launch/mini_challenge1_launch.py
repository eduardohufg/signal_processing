from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='signal_processing',
            executable='signal_generator',
            name='signal_generator',
            output='screen',
            parameters=[
                {'amplitude': 1.0},
                {'phase': 0.0},
                {'offset': 0.0},
                {'period': 2},
                {'sample_time': 0.1},
                {'type': 1}
            ]   
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
    
