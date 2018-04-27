#from goforward2.py, the "stop action" initiated when the robot detacted the obstacle
#changed to "going back in circle action"

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import radians

class GoForward5():
	def __init__(self):
		rospy.init_node('GoForward5',anonymous=False)
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
		self.ranges=data.ranges

	def control(self):
		stop_condition=False		
		for degree, x in enumerate(self.ranges):
			if x < 0.15 and x > 0.01:
				print 'stop for degree %d, range %f'%(degree, x)
				stop_condition=True
				break
		move_cmd =Twist()
		if stop_condition:
			move_cmd.linear.x=-0.05
			move_cmd.angular.z=radians(-20)
		else :
			move_cmd.linear.x=0.2
		return move_cmd

	def shutdown(self):
		rospy.loginfo("stop turtlebot")
		self.cmd_vel.publish(Twist())
		rospy.sleep(1)

if __name__=='__main__':
	#try:
	#	GoForward5()
	#except:
	#	rospy.loginfo("Goforad node terminated")
	GoForward5()
