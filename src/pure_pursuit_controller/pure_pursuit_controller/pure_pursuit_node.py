import csv
import math
import os
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class PurePursuitNode(Node):

    def __init__(self):
        super().__init__('pure_pursuit_node')

        # Parameters
        self.declare_parameter('waypoints_file', '~/waypoints.csv')
        self.declare_parameter('wheelbase', 2.86)       # L (meters, standard Prius ~2.86m)
        self.declare_parameter('target_velocity', 3.0)   # v_x (m/s)
        self.declare_parameter('lookahead_k', 0.8)       # k parameter for P = k * v_x
        self.declare_parameter('min_lookahead', 1.0)     # Minimum P (meters)

        # Retrieve parameters
        csv_path = os.path.expanduser(self.get_parameter('waypoints_file').value)
        self.L = self.get_parameter('wheelbase').value
        self.v_x = self.get_parameter('target_velocity').value
        self.k = self.get_parameter('lookahead_k').value
        self.min_lookahead = self.get_parameter('min_lookahead').value

        # Calculate look-ahead distance: P = k * v_x
        self.P = max(self.k * self.v_x, self.min_lookahead)

        # State Variables
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0
        self.odom_received = False
        self.target_idx = 0

        # Load Waypoints
        self.waypoints = self.load_waypoints(csv_path)

        # QoS configuration matching Gazebo /odom output
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # ROS 2 Interfaces
        self.sub_odom = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            qos_profile
        )

        self.pub_cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)

        # Control Loop Timer (10 Hz = 0.1 sec)
        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info(
            f'Pure Pursuit Node initialized. Lookahead P: {self.P:.2f}m, Target V: {self.v_x}m/s'
        )

    def load_waypoints(self, filepath):
        waypoints = []
        if not os.path.exists(filepath):
            self.get_logger().error(f'Waypoints file not found: {filepath}')
            return waypoints

        try:
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip CSV header ['x', 'y']
                for row in reader:
                    if row and len(row) >= 2:
                        waypoints.append((float(row[0]), float(row[1])))
            self.get_logger().info(f'Successfully loaded {len(waypoints)} waypoints.')
        except Exception as e:
            self.get_logger().error(f'Failed to parse waypoints CSV: {e}')

        return waypoints

    def odom_callback(self, msg: Odometry):
        # 1. State Estimation (Position)
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        # Extract Quaternion components
        q_x = msg.pose.pose.orientation.x
        q_y = msg.pose.pose.orientation.y
        q_z = msg.pose.pose.orientation.z
        q_w = msg.pose.pose.orientation.w

        # 2. Planar Euler Yaw conversion: theta = atan2(2(q_w*q_z + q_x*q_y), 1 - 2(q_y^2 + q_z^2))
        siny_cosp = 2.0 * (q_w * q_z + q_x * q_y)
        cosy_cosp = 1.0 - 2.0 * (q_y * q_y + q_z * q_z)
        self.current_yaw = math.atan2(siny_cosp, cosy_cosp)

        self.odom_received = True

    def control_loop(self):
        if not self.odom_received or not self.waypoints:
            return

        # Stop command payload initialization
        cmd = Twist()

        # Check if route completed
        if self.target_idx >= len(self.waypoints):
            self.get_logger().info('Reached final waypoint. Stopping vehicle.', once=True)
            self.pub_cmd_vel.publish(cmd)
            return

        # Find target look-ahead waypoint
        target_pt = None
        for i in range(self.target_idx, len(self.waypoints)):
            wx, wy = self.waypoints[i]
            dist = math.sqrt((wx - self.current_x)**2 + (wy - self.current_y)**2)
            if dist >= self.P:
                self.target_idx = i
                target_pt = (wx, wy)
                break

        # If near end and remaining path is smaller than P, target the last point
        if target_pt is None:
            target_pt = self.waypoints[-1]
            last_dist = math.sqrt(
                (target_pt[0] - self.current_x)**2 + (target_pt[1] - self.current_y)**2
            )
            if last_dist < 0.5:
                self.get_logger().info('Goal reached!')
                self.pub_cmd_vel.publish(cmd)
                return

        tx, ty = target_pt

        # Transform target point to Vehicle Local Frame
        dx = tx - self.current_x
        dy = ty - self.current_y

        # Alpha / Heading Angle Error (phi) in vehicle local frame
        # phi = atan2(dy, dx) - current_yaw
        local_x = math.cos(self.current_yaw) * dx + math.sin(self.current_yaw) * dy
        local_y = -math.sin(self.current_yaw) * dx + math.cos(self.current_yaw) * dy

        phi = math.atan2(local_y, local_x)

        # Pure Pursuit Steering Angle Formula: delta = atan2(2 * L * sin(phi), P)
        delta = math.atan2(2.0 * self.L * math.sin(phi), self.P)

        # Kinematic Bicycle Model Conversion: theta_dot = v * tan(delta) / L
        theta_dot = (self.v_x * math.tan(delta)) / self.L

        # Construct and publish /cmd_vel
        cmd.linear.x = self.v_x
        cmd.angular.z = theta_dot
        self.pub_cmd_vel.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = PurePursuitNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Emergency stop on shutdown
        stop_cmd = Twist()
        node.pub_cmd_vel.publish(stop_cmd)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()