#going back or left

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import radians

class GoForward7():
	def __init__(self):
		rospy.init_node('GoForward7',anonymous=False)
		rospy.loginfo("to stop tutle ctrl c")
		rospy.on_shutdown(self.shutdown)
		self.cmd_vel=rospy.Publisher('cmd_vel', Twist, queue_size=10)
		r=rospy.Rate(10);
		self.scan=rospy.Subscriber('/scan',LaserScan,self.callback)

		while not rospy.is_shutdown():
		

			if not hasattr(self,'ranges'):
				
				r.sleep()
				continue
			

			move_cmd=self.control()
			
			self.cmd_vel.publish(move_cmd)
			r.sleep()
			
	def callback(self, data):
		#print type(data.ranges)
		#print len(data.ranges)
		self.range=data.ranges

	def control(self):
		back_left_condition=False
		back_right_condition=False
		
		for degree, x in enumerate(self.range):
			if x < 0.15 and x > 0.01 and degree <50:
				print 'stop for degree %d, range %f'%(degree, x)
				back_left_condition=True
				break

			elif x < 0.15 and x > 0.01 and degree >310:
				print 'stop for degree %d, range %f'%(degree, x)
				back_right_condition=True
				break

		move_cmd =Twist()
		if back_left_condition:
			rospy.loginfo("going back left")
			move_cmd.linear.x=-0.05
			move_cmd.angular.z=radians(-20)
		
		elif back_right_condition:
			rospy.loginfo("going back right")
			move_cmd.linear.x=-0.05
			move_cmd.angular.z=radians(20)
		
		else :
			move_cmd.linear.x=0.2
		return move_cmd

	def shutdown(self):
		rospy.loginfo("stop turtlebot")
		self.cmd_vel.publish(Twist())
		rospy.sleep(1)

if __name__=='__main__':
	#try:
	#	GoForward7()
	#except:
	#	rospy.loginfo("Goforad node terminated")
	GoForward7()
