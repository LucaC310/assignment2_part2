#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_srvs.srv import SetBool

FT_TO_M = 0.305  # 1 ft/s = 0.305 m/s

class RobotController(Node):
	def __init__(self):
		super().__init__("robot_controller")
		
		# Publisher initialisation for velocity commands
		self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
		
		# Publisher for linear velocity in ft/s
		self.lin_vel_ft_pub = self.create_publisher(Twist, "/linear_velocity_ft", 10)
		
		# Subscriber initialisation for odometry feedback
		self.odom_sub = self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
		
		# Service to modify angular velocity
		self.angular_srv = self.create_service(SetBool, "/set_angular_direction", self.set_angular_callback)
		
		timer_period = 0.1	
		self.timer = self.create_timer(timer_period, self.timer_callback)
		
		self.position = None
		self.orientation = None
		self.vel_msg = Twist()

	def odom_callback(self, msg: Odometry):
		self.position = msg.pose.pose.position
		self.orientation = msg.pose.pose.orientation
		
		# Movement logic
		if self.position.x > 9.0:
			self.vel_msg.linear.x = 1.0
			self.vel_msg.angular.z = 1.0
		elif self.position.x < 2.0:
			self.vel_msg.linear.x = 1.0
			self.vel_msg.angular.z = -1.0
		else:
			self.vel_msg.linear.x = 1.0
			self.vel_msg.angular.z = 0.0
		
		# Publish linear velocity in ft/s
		vel_ft = Twist()
		vel_ft.linear.x = self.vel_msg.linear.x / FT_TO_M
		self.lin_vel_ft_pub.publish(vel_ft)

	def set_angular_callback(self, request, response):
		if request.data:
			self.vel_msg.angular.z = 1.0
			response.message = "Angular velocity set to +1.0 rad/s"
		else:
			self.vel_msg.angular.z = -1.0
			response.message = "Angular velocity set to -1.0 rad/s"

		response.success = True
		return response
		
	def timer_callback(self):
		self.cmd_pub.publish(self.vel_msg)

def main(args=None):
	rclpy.init(args=args)
	node = RobotController()
	rclpy.spin(node)
	rclpy.shutdown()
	
if __name__ == '__main__':
	main()

