from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='signal_processing',
            executable='signal_parameter',
            name='signal_parameter',
            output='screen',
            parameters=[
                {'amplitude': 1.5},
                {'phase': 0.0},
                {'offset': 0.0},
                {'period': 1},
                {'sample_time': 0.01},
                {'type': 3}
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
        ),
        ExecuteProcess(
            cmd=['plotjuggler'],
            output='screen'
        )
    ])
    
