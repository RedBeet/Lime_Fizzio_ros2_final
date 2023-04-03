import rclpy
import math

# from urdf_parser_py.urdf import URDF

from rclpy.node import Node
from rclpy.qos import QoSProfile

# from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

from .motor import Motor
class NanoSaur(Node):

    def __init__(self):
        super().__init__('lime_fizzio')
        
        self.timer_period = 1. / 5
        self.get_logger().debug(f"timer {self.timer_period}")
        
        # Get RPM motors
        # self.declare_parameter("rpm")
        # self.rpm = self.get_parameter("rpm").value
        self.rpm = 266
        self.get_logger().debug(f"RPM motors {self.rpm}")

        self.motor = Motor(self.rpm)

        self.velsubscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.drive_callback,
            10)

        self.ultrasonicsubscription = self.create_subscription(
            Bool,
            'sensor_ultrasonic',
            self.ultrasonic_callback,
            10)

        # Node started
        self.get_logger().info("Hello Lime Fizzio!")

        self.radius = 0.1
        self.wheel_separation = 0.3

    def convert_speed(self, v, w):
        half_wheel_separation = self.wheel_separation / 2.
        vr = v + half_wheel_separation * w
        vl = v - half_wheel_separation * w
        rr = vr / self.radius
        rl = vl / self.radius
        return [rr, rl]

    def drive_callback(self, msg):
        # Store linear velocity and angular velocity
        v = msg.linear.x
        w = msg.angular.z
        # Convert linear and angular velocity to radiant motor speed
        self.get_logger().debug(f"v={v} w={w}")
        r = self.convert_speed(v, w)
        self.get_logger().debug(f"rad {r}")
        self.get_logger().info(f"v = {v}, w = {w}")
        max_speed = self.rpm
        # Constrain between -max_speed << speed << max_speed.
        self.r = [max(-max_speed, min(max_speed, r[0])), max(-max_speed, min(max_speed, r[1]))]
        # Send a warning message if speed is over 
        if r[0] != self.r[0]:
            self.get_logger().warning(f"ref speed over {r[0] - self.r[0]}")
        if r[1] != self.r[1]:
            self.get_logger().warning(f"ref speed over {r[1] - self.r[1]}")
        # Convert speed to motor speed in RPM
        rpmr = self.r[0] * 60. / (2 * math.pi)
        rpml = self.r[1] * 60. / (2 * math.pi)
        # Set to max RPM available
        self.get_logger().info(f"RPM R={rpmr} L={rpml}")
        self.motor.set_speed(rpmr, rpml)

    def ultrasonic_callback(self, msg):
        if msg:
            self.motor.set_speed(0,0)

def main(args=None):
    rclpy.init(args=args)

    nanosaur = NanoSaur()
    try:
        rclpy.spin(nanosaur)
    except KeyboardInterrupt:
        pass
    # Destroy the node explicitly
    nanosaur.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
# EOF
