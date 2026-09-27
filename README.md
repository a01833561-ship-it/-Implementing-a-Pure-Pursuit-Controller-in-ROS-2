
# Pure Pursuit Autonomous Controller for ROS 2 Jazzy

An autonomous trajectory-tracking implementation using the kinematic bicycle model for a Prius vehicle in Gazebo.
Usage Workflow
Step 1: Record Reference Waypoints
Terminal 1: Launch Gazebo Simulation
Bash
cd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch prius_bringup gz_sim.launch.py
Terminal 2: Run Path Recorder
Bash
cd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run pure_pursuit_controller path_recorder
Drive and Save Reference Path
Drive the vehicle around in Gazebo (via teleop or simulation GUI).

Once your route is mapped, select Terminal 2 (path_recorder) and press Ctrl + C to save ~/waypoints.csv.

Select Terminal 1 (gz_sim) and press Ctrl + C to stop the simulation.

Step 2: Autonomous Tracking Run
In this step, pure_pursuit_node reads ~/waypoints.csv and drives the vehicle automatically while path_recorder logs the executed path.

Terminal 1: Launch Controller & Simulation Concurrently
Bash
cd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch pure_pursuit_controller pure_pursuit.launch.py
(Optional) If pure_pursuit.launch.py does not include path_recorder, start it manually in Terminal 2:

Bash
cd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run pure_pursuit_controller path_recorder --ros-args -p filename:=actual_trajectory.csv
Complete Route and Save
Allow the vehicle to complete the trajectory automatically.

Press Ctrl + C in the running terminal(s) to shut down the nodes and write ~/actual_trajectory.csv.

Step 3: Performance Evaluation
Compute the Mean Cross-Track Error (CTE) and generate comparison plots between the reference and actual trajectories.

Execute Evaluation Script
Bash
python3 ~/git_ws/evaluate_tracking.py
Results & Artifacts
Terminal Output: Displays numerical tracking error metrics (Mean CTE).

Plot Display: Opens an interactive Matplotlib window showing the trajectory overlay.

Saved Artifacts: Generates high-resolution performance plots at docs/images/trajectory_comparison.png and docs/images/overlay_trajectory_plot.png.
