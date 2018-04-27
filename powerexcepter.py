from sensor_msgs.msg import JointState
import rospy
a=[]
c=[]
class Powerexcepter():
	def __init__(self):
		rospy.init_node('motor_eye',anonymous=False)
		rospy.loginfo("ctrl c for stop")
		
		self.position=rospy.Publisher('arm_node/arm_command',JointState,queue_size=10)
		r=rospy.Rate(10);
		self.ex_force=rospy.Subscriber("arm_joint_states",JointState, self.callback)
		
		while not rospy.is_shutdown():
			
			if not hasattr(self,'data'):
				r.sleep()
				continue
			
			armpos=self.control()
			#armpos=JointState()
			#armpos.position=[-30.0]
			#armpos.name=['j1_joint']
			self.position.publish(armpos)
			r.sleep()

		
			
			

	def callback(self,data):
		self.data=data.position
		#print self.data[0]
		
	
	def control(self):
		clock_condition=False
		counter_clock_condition=False

		#print self.data[0]
		
		armpos=JointState()
		a.append(self.data[0])
		b=a[len(a)-1]-a[len(a)-2]
		
		
		if b<0:
			rospy.loginfo("clock condition")
			clock_condition=True
			
		elif b>0:
			rospy.loginfo("counter clock condition")
			counter_clock_condition=True
				
			

		if clock_condition:
			armpos.name=['j1_joint']
			armpos.position=[self.data[0]-10.0]
			
		elif counter_clock_condition:
			armpos.name=['j1_joint']
			armpos.position=[self.data[0]+10.0]
			
		return armpos
		

if __name__ == '__main__':
	Powerexcepter()
