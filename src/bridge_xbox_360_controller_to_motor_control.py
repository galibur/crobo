#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

import rospy
from std_msgs.msg import String

import json

node_name = "bridge_xbox_360_controller_to_motor_control"

subscriber_channel = "/user_input"
publisher_channel = "/crobo_control_commands"

print 'start node'

def makeCmd(function, value):
	msg = '{"function":"' + str(function) + '","speed":"' + str(value) + '"}'
	print(msg)

def getXboxControllerInput(msg):

	#print(msg.data)
	cmd = json.loads(msg.data)
	if str(cmd['user_input']) == "xbox":
		#print(str(cmd))
		key = str(cmd['key'])
		val = str(cmd['val'])

		#if val == "0.0" or val == "0":
		#	makeCmd("stop", 0)

		if key == "LEFT_TRIGGER":
			makeCmd("rotateLeft",val)
		
		elif key == "RIGHT_TRIGGER":
			makeCmd("rotateRight",val)
	
		elif key == "UP":
			makeCmd("forward",val)
	
		elif key == "DOWN":
			makeCmd("backward",val)
	
		elif key == "LEFT":
			makeCmd("turnLeft",val)
	
		elif key == "RIGHT":
			makeCmd("turnRight",val)
	
	

rospy.init_node(node_name)
sub = rospy.Subscriber(subscriber_channel, String, getXboxControllerInput)

rospy.spin()

