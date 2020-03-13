#!/usr/bin/env python

import RPi.GPIO as GPIO          
from time import sleep
import rospy
from std_msgs.msg import String

GPIO.setmode(GPIO.BCM)

class Motor():
	def __init__(self, en, in1, in2, speed_min, speed_max, speed_current, pwm_freq):
		self.en = en
		self.in1 = in1
		self.in2 = in2
		self.speed_min = speed_min
		self.speed_max = speed_max
		self.speed_current = speed_current
		self.pwm_freq = pwm_freq

		GPIO.setup(self.in1,GPIO.OUT)
		GPIO.setup(self.in2,GPIO.OUT)
		GPIO.setup(self.en,GPIO.OUT)
		GPIO.output(self.in1,GPIO.LOW)
		GPIO.output(self.in2,GPIO.LOW)
		self.p = GPIO.PWM(self.en,self.pwm_freq)
		self.p.start(25)

	def forward(self, speed):
		#print 'fw'
		self.setSpeed(speed)
		GPIO.output(self.in1,GPIO.HIGH)
		GPIO.output(self.in2,GPIO.LOW)

	def backward(self, speed):
		#print 'backward'
		self.setSpeed(speed)
		GPIO.output(self.in2,GPIO.HIGH)
		GPIO.output(self.in1,GPIO.LOW)

	def stop(self):
		#print 'stop'
		GPIO.output(self.in1,GPIO.LOW)
		GPIO.output(self.in2,GPIO.LOW)
	
	def setSpeed(self, speed):
		self.speed_current = speed
        	self.p.ChangeDutyCycle(self.speed_current)


class Crobo():
	def __init__(self):

		self.motor = {}
		self.motor[0] = Motor(25, 24, 23, 0, 100, 100, 50)
		self.motor[1] = Motor(22, 27, 17, 0, 100, 100, 50)

		self.motor[2] = Motor(5, 19, 13, 0, 100, 100, 50)
		self.motor[3] = Motor(26, 20, 21, 0, 100, 100, 50)

	def moveForward(self, speed):
		print 'move forward'
		for i in range(4):
			self.motor[i].forward(speed)

	def moveBackward(self, speed):
		print 'move backward'
		for i in range(4):
			self.motor[i].backward(speed)

	def turnLeft(self, speed):
		print 'turn left'
		self.motor[1].forward(speed)
		self.motor[3].forward(speed)
		self.motor[0].stop()
		self.motor[2].stop()

	def turnRight(self, speed):
		print 'turn right'
		self.motor[0].forward(speed)
		self.motor[2].forward(speed)
		self.motor[1].stop()
		self.motor[3].stop()

	def rotateLeft(self, speed):
		print 'rotate left'
		self.motor[0].forward(speed)
		self.motor[2].forward(speed)

		self.motor[1].backward(speed)
		self.motor[3].backward(speed)
		
	def rotateRight(self, speed):
		print 'rorate right'
		self.motor[0].backward(speed)
		self.motor[2].backward(speed)

		self.motor[1].forward(speed)
		self.motor[3].forward(speed)

	def stop(self):
		print 'stop'
		for i in range(4):
			self.motor[i].stop()
			

def executeMotorCommand(msg):

	print msg.data
	crobo = Crobo()

	crobo.moveForward(100)
	sleep(2)
	crobo.stop()
	sleep(2)
	crobo.rotateLeft(59)
	sleep(2)
	crobo.rotateRight(59)
	sleep(2)
	crobo.turnLeft(59)
	sleep(2)
	crobo.turnRight(59)
	sleep(2)
	crobo.stop()

print 'start node'
rospy.init_node('crobo_motor_control_subscriber')
sub = rospy.Subscriber('/crobo_control_commands', String, executeMotorCommand)

rospy.spin()


GPIO.cleanup()
