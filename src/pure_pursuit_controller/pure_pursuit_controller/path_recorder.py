import csv
import math
import os
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from nav_msgs.msg import Odometry


class PathRecorder(Node):

    def __init__(self):
        super().__init__('path_recorder')

        self.declare_parameter('filename', 'waypoints.csv')
        self.filename = self.get_parameter('filename').value

        self.waypoints = []
        self.threshold = 0.20  # meters

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            qos_profile
        )

        self.get_logger().info(
            f'Path recorder started. Saving output to: {self.filename}'
        )

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        if not self.waypoints:
            self.waypoints.append((x, y))
            self.get_logger().info(f'Recorded first point: ({x:.2f}, {y:.2f})')
            return

        previous_x, previous_y = self.waypoints[-1]
        distance = math.sqrt((x - previous_x)**2 + (y - previous_y)**2)

        if distance >= self.threshold:
            self.waypoints.append((x, y))
            self.get_logger().info(f'Recorded point: ({x:.2f}, {y:.2f})')

    def save_waypoints(self):
        output_path = os.path.expanduser(f'~/{self.filename}')
        try:
            with open(output_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['x', 'y'])
                for x, y in self.waypoints:
                    writer.writerow([x, y])

            print(f'\n[SUCCESS] Saved {len(self.waypoints)} points to {output_path}\n')
        except Exception as e:
            print(f'\n[ERROR] Failed to save waypoints: {e}\n')


def main(args=None):
    rclpy.init(args=args)
    node = PathRecorder()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.save_waypoints()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()