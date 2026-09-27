# Pure Pursuit Path Tracking

ROS 2 Jazzy project for recording a reference path, autonomously following it with Pure Pursuit, and evaluating tracking performance.

## Step 1: Record Reference Path

### Terminal 1: Launch Gazebo Simulation

`bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch prius_bringup gz_sim.launch.py`


### Terminal 2: Run Path Recorder 

`cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install 
source install/setup.bash
ros2 run pure_pursuit_controller path_recorder`

### Drive and Save Reference Path

Drive the vehicle around the desired route in Gazebo. 
Then Press Ctrl + C to stop recording. The reference path is saved as ~/waypoints.csv. 
Select Terminal 1, Press Ctrl + C to stop the simulation. 

## Step 2: Autonomous Tracking Run
The Pure Pursuit controller reads ~/waypoints.csv and automatically drives the vehicle while recording the executed trajectory.

Terminal 1: Launch Controller and Simulation

`source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch pure_pursuit_controller pure_pursuit.launch.py`

The vehicle will complete the route automatically and be saved as `~/actual_trajectory.csv`

## Step 3: Performance Evaluation

The evaluation script calculates the Mean Cross-Track Error (CTE) and generates a trajectory comparison plot.
`cd ~/ros2_ws 
python3 evaluate_tracking.py`

The terminal displays the Mean Cross-Track Error (CTE).

A Matplotlib window shows the comparison between  Reference path (`waypoints.csv`) and `actual_trajectory.csv` .

The plot is saved as `~/trajectory_comparison.png` in `/docs/images`
