import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, PointCloud2
from laser_geometry import LaserProjection
from rclpy.qos import QoSProfile, QoSReliabilityPolicy


class Scan_to_cloud(Node):
    def __init__(self):
        super().__init__('scan_to_cloud')
        qos_profile = QoSProfile(depth=10, reliability=QoSReliabilityPolicy.BEST_EFFORT)
        self.sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, qos_profile)
        self.pub = self.create_publisher(PointCloud2, 'cloud', qos_profile)

    def scan_callback(self, msg):
        projector = LaserProjection()
        cloud = projector.projectLaser(msg)
        self.pub.publish(cloud)

def main(args=None):
    rclpy.init(args=args)
    scan_to_cloud = Scan_to_cloud()
    rclpy.spin(scan_to_cloud)
    scan_to_cloud.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()