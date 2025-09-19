#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class RobotController(Node):
	def __init__(self):
		super().__init__("robot_controller")
		
		self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
		
		self.odom_sub = self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
		
		timer_period = 0.1	
		self.timer = self.create_timer(timer_period, self.timer_callback)
		
		self.position = None
		self.orientation = None
		self.vel_msg = Twist()
		
	def odom_callback(self, msg: Odometry):
		self.position = msg.pose.pose.position
		self.orientation = msg.pose.pose.orientation
		self.get_logger().info(f'Odom -> x: {self.position.x:.2f}, y: {self.position.y:.2f}')
		
		if self.position.x > 9.0:
			self.vel_msg.linear.x = 1.0
			self.vel_msg.angular.z = 1.0
		elif self.position.x < 1.5:
			self.vel_msg.linear.x = 1.0
			self.vel_msg.angular.z = -1.0
		else:
			self.vel_msg.linear.x = 1.0
			self.vel_msg.angular.z = 0.0
		
	def timer_callback(self):
		self.cmd_pub.publish(self.vel_msg)

def main(args=None):
	rclpy.init(args=args)
	node = RobotController()
	rclpy.spin(node)
	rclpy.shutdown()
	
if __name__ == '__name__':
	main()
