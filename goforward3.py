import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import radians

class GoForward3():
	def __init__(self):
		
		rospy.init_node('GoForward3',anonymous=False)
		rospy.loginfo("to stop tutle ctrl c")
		rospy.on_shutdown(self.shutdown)
		self.cmd_vel=rospy.Publisher('cmd_vel', Twist, queue_size=10)
		r=rospy.Rate(10);
		self.scan=rospy.Subscriber('/scan',LaserScan,self.callback)

		move_cmd=Twist()
		move_cmd.linear.x=0.2

		back_cmd=Twist()
		back_cmd.linear.x=-0.1

		turn_cmd=Twist()
		turn_cmd.linear.x=0
		turn_cmd.angular.z=radians(-45)
		
		while not rospy.is_shutdown():
			
			
			if not hasattr(self,'ranges'):
				
				r.sleep()
				continue
			
			back_condition=False
			for degree, x in enumerate(self.ranges):
				if x < 0.2 and x > 0.01:
					print 'obstacle detacting %d degree, range %f'%(degree, x)
					back_conditon=True
					break
				if back_condition:
					rospy.loginfo("going back")
					for i in range(0,10):
						self.cmd_vel.publish(back_cmd)
						r.sleep()

					rospy.loginfo("turning")
					for i in range(0,5):
						self.cmd_vel.publish(turn_cmd)
						r.sleep()

				else :
					self.cmd_vel.publish(move_cmd)

				
			
	def callback(self, data):
		
		#print type(data.ranges)
		#print len(data.ranges)
		self.ranges=data.ranges

		

		

	def shutdown(self):
		
		rospy.loginfo("stop turtlebot")
		self.cmd_vel.publish(Twist())
		rospy.sleep(1)

if __name__=='__main__':
	
	#try:
	#	GoForward3()
	#except:
	#	rospy.loginfo("Goforad node terminated")
	GoForward3()
