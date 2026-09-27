# Pure Pursuit Path Tracking

ROS 2 Jazzy project for recording a reference path, autonomously following it with Pure Pursuit, and evaluating tracking performance.

## Step 1: Record Reference Path

### 1. Terminal 1: Launch Gazebo Simulation

**Directory:** `~/git_ws`

```bash
cd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch prius_bringup gz_sim.launch.py
2. Terminal 2: Run Path Recorder

Directory: ~/git_ws

cd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run pure_pursuit_controller path_recorder

The recorder saves the reference path to:

~/waypoints.csv
3. Drive and Save Reference Path

Drive the vehicle around the desired route in Gazebo.

When finished:

Select Terminal 2.
Press Ctrl + C to stop recording.
The reference path is saved as ~/waypoints.csv.
Select Terminal 1.
Press Ctrl + C to stop the simulation.
Step 2: Autonomous Tracking Run

The Pure Pursuit controller reads ~/waypoints.csv and automatically drives the vehicle while recording the executed trajectory.

1. Terminal 1: Launch Controller and Simulation

Directory: ~/git_ws

cd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch pure_pursuit_controller pure_pursuit.launch.py

If pure_pursuit.launch.py does not include path_recorder, run it manually in Terminal 2:

cd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run pure_pursuit_controller path_recorder --ros-args -p filename:=actual_trajectory.csv
2. Complete Route and Save File

Allow the vehicle to complete the route automatically.

Press Ctrl + C in the running terminal(s) to stop the nodes.

The executed trajectory is saved as:

~/actual_trajectory.csv
Step 3: Performance Evaluation

The evaluation script calculates the Mean Cross-Track Error (CTE) and generates a trajectory comparison plot.

1. Run Evaluation Script

Directory: ~

cd ~
python3 evaluate_tracking.py

If evaluate_tracking.py is inside the workspace:

python3 ~/git_ws/evaluate_tracking.py
2. View Results

The terminal displays the Mean Cross-Track Error (CTE).

A Matplotlib window shows the comparison between:

Reference path: waypoints.csv
Actual trajectory: actual_trajectory.csv

The high-resolution plot is saved as:

~/trajectory_comparison.png
Output Files
File	Description
~/waypoints.csv	Reference path
~/actual_trajectory.csv	Actual autonomous trajectory
~/trajectory_comparison.png	Trajectory comparison plot
