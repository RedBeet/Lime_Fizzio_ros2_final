#TODO: line27 false to true

# !/usr/bin/env/ python3
import rclpy
from rclpy.node import Node
from tutorial_interfaces.msg import Dht11, Heights
from geometry_msgs.msg import Twist
from .ardData import ArduinoData

class arduinoPublisher(Node):
    def __init__(self):
        super().__init__("arduino_sensor")
        self.publisher1 = self.create_publisher(Dht11, "/sensor_dht11", 10)
        self.publisher2 = self.create_publisher(Heights, "/sensor_ultrasonic", 10)
        timer_period = 0.5 #seconds
        self.timer = self.create_timer(timer_period, self.publish_callback)
        self.get_logger().info(
             'Ultrasonic node Started, get heights data from ultrasonic sensor \n'
        )
        self.ardData = ArduinoData()
    
        self.velsubscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.vel_callback,
            10)

    def publish_callback(self):
        height_msg = Heights()
        humitemp_msg = Dht11()
        upside, downside, humi, temp = map(float, self.ardData.getArduino().split())
        self.get_logger().info(f"height: {upside} {downside}")
        height_msg.upside = upside
        height_msg.downside = downside
        humitemp_msg.humi = humi
        humitemp_msg.temp = temp
        self.publisher2.publish(height_msg)
        self.publisher1.publish(humitemp_msg)

    def vel_callback(self, msg):
        self.ardData.subVelocity(msg.linear.x, msg.angular.z)

    
def main(args=None):
    rclpy.init(args=args)

    arduino_publisher = arduinoPublisher()
    rclpy.spin(arduino_publisher)

    arduino_publisher.get_logger().info('\n====Stop Publishing====')
    arduino_publisher.destroy_node()
    rclpy.shutdown()

