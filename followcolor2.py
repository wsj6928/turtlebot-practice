import rospy
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
from math import radians

class Followcolor():
	def __init__(self):
		rospy.init_node('robot_eye',anonymous=False)
		rospy.loginfo("ctrl c for stop")
		rospy.on_shutdown(self.shutdown)
		self.cmd_vel=rospy.Publisher('cmd_vel',Twist,queue_size=10)
		r=rospy.Rate(10);
		self.camera=rospy.Subscriber("std_msgs",Int64, self.callback)

		while not rospy.is_shutdown():
			
			if not hasattr(self,'data'):
				r.sleep()
				continue

			move_cmd=self.control()
			self.cmd_vel.publish(move_cmd)
			r.sleep()

	def callback(self,data):
		self.data=data.data
		
	def control(self):

		turn_left_condition=False
		turn_right_condition=False
		
		#print self.data
		
		
		if self.data<260:
			turn_left_condition=True
		elif self.data>400:
			turn_right_condition=True

		move_cmd=Twist()
		if turn_left_condition:
			rospy.loginfo("turning left")
			move_cmd.angular.z=radians(80)
			
	
		elif turn_right_condition:
			rospy.loginfo("turning right")
			move_cmd.angular.z=radians(-80)
			
		else:
			rospy.loginfo("going straight")
			move_cmd.linear.x=0
		return move_cmd

	def shutdown(self):	
		rospy.loginfo("stop turtle")
		self.cmd_vel.publish(Twist())
		rospy.sleep(1)

if __name__ == '__main__':
	Followcolor()
