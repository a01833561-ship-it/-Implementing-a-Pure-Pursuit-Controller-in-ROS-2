
## Trajectory Performance & Overlay Plots

### Reference vs. Executed Trajectory
![Trajectory Comparison](docs/images/trajectory_comparison.png)

Step 1: Manual Mapping Run (Generate waypoints.csv)In this step, you manually drive the Prius in Gazebo while path_recorder.py saves your reference route.1.Terminal 1: Launch Gazebo Simulation:Directory: ~/git_ws.Source your workspace and start the Prius simulation:Bashcd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch prius_bringup gz_sim.launch.py
2.Terminal 2: Run Path Recorder:Directory: ~/git_ws.Open a second terminal to start recording the ground-truth path (defaults to saving ~/waypoints.csv):Bashcd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run pure_pursuit_controller path_recorder
3.Drive and Save Reference Path:Directory: ~/git_ws.Drive the vehicle around in Gazebo (via teleop or simulation GUI). Once you've mapped your route:Select Terminal 2 (path_recorder).Press Ctrl + C to stop recording and write ~/waypoints.csv.Select Terminal 1 (gz_sim) and press Ctrl + C to stop the simulation.Step 2: Autonomous Tracking Run (Generate actual_trajectory.csv)In this step, pure_pursuit_node reads ~/waypoints.csv and drives the car automatically, while path_recorder saves the executed path.1.Terminal 1: Launch Controller & Simulation Concurrently:Directory: ~/git_ws.Launch the simulation alongside the controller and recorder:Bashcd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch pure_pursuit_controller pure_pursuit.launch.py
If your launch file does NOT include path_recorder inside pure_pursuit.launch.py, start it manually in Terminal 2:Bashcd ~/git_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run pure_pursuit_controller path_recorder --ros-args -p filename:=actual_trajectory.csv
2.Complete Route and Save File:Directory: ~/git_ws.Allow the car to complete the path automatically. Once finished:Press Ctrl + C in your running terminal(s) to shut down the node and save ~/actual_trajectory.csv.Step 3: Performance Evaluation (evaluate_tracking.py)Compute the Mean Cross-Track Error (CTE) and generate the overlay plot comparing both files.1.Terminal 1: Execute Python Evaluation Script:Directory: ~/.Run the evaluation script from your terminal:Bashcd ~
python3 evaluate_tracking.py
(If evaluate_tracking.py is saved inside your workspace directory, run python3 ~/git_ws/evaluate_tracking.py instead)2.View Results and Generated Artifacts:Directory: ~/.The terminal will output the Mean Cross-Track Error (CTE) metrics and pop up a Matplotlib window displaying the trajectory overlay. A high-resolution figure will also be saved to ~/trajectory_comparison.png.
