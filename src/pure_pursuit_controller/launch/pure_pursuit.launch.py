import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Path to prius_bringup launch file
    prius_bringup_dir = get_package_share_directory('prius_bringup')
    gz_sim_launch_path = os.path.join(prius_bringup_dir, 'launch', 'gz_sim.launch.py')

    # 1. Simulation Launch Description
    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_sim_launch_path)
    )

    # 2. Pure Pursuit Controller Node
    pure_pursuit_node = Node(
        package='pure_pursuit_controller',
        executable='pure_pursuit_node',
        name='pure_pursuit_node',
        output='screen',
        parameters=[{
            'waypoints_file': '~/waypoints.csv',
            'wheelbase': 2.86,
            'target_velocity': 2.0,
            'lookahead_k': 0.8,
            'min_lookahead': 1.0
        }]
    )

    # 3. Path Recorder Node writes a separate trajectory CSV with the filename parameter set
    path_recorder_node = Node(
        package='pure_pursuit_controller',
        executable='path_recorder',
        name='actual_path_recorder',
        output='screen',
        parameters=[{
        'filename': 'actual_trajectory.csv'  # <--- ROS 2 sets this automatically
        }]
    )

    return LaunchDescription([
        gz_sim_launch,
        pure_pursuit_node,
        path_recorder_node
    ])