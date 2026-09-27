import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Load CSV files from Home Directory
ref_path = os.path.expanduser('~/waypoints.csv')
act_path = os.path.expanduser('~/actual_trajectory.csv')

df_ref = pd.read_csv(ref_path)
df_act = pd.read_csv(act_path)

# Compute Mean Cross-Track Error (Minimum distance from each actual point to any reference point)
errors = []
for _, act_row in df_act.iterrows():
    act_pt = np.array([act_row['x'], act_row['y']])
    ref_pts = df_ref[['x', 'y']].values
    
    # Euclidean distance to all reference waypoints
    distances = np.linalg.norm(ref_pts - act_pt, axis=1)
    min_dist = np.min(distances)
    errors.append(min_dist)

mean_cte = np.mean(errors)
max_cte = np.max(errors)

print(f"--- Tracking Performance Report ---")
print(f"Mean Cross-Track Error (CTE): {mean_cte:.4f} meters")
print(f"Max Cross-Track Error (CTE):  {max_cte:.4f} meters")

# Plot Reference vs. Actual Trajectory
plt.figure(figsize=(10, 6))
plt.plot(df_ref['x'], df_ref['y'], 'k--', label='Reference Trajectory (waypoints.csv)', linewidth=2)
plt.plot(df_act['x'], df_act['y'], 'r-', label='Executed Trajectory (actual_trajectory.csv)', linewidth=1.5)

plt.title(f'Pure Pursuit Trajectory Tracking\nMean CTE: {mean_cte:.3f} m')
plt.xlabel('X Position [m]')
plt.ylabel('Y Position [m]')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.savefig(os.path.expanduser('~/trajectory_comparison.png'))
plt.show()