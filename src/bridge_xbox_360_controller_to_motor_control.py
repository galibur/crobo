#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

import rospy
from std_msgs.msg import String

import json

node_name = "bridge_xbox_360_controller_to_motor_control"

print 'start node'

def getXboxControllerInput(msg):

	print(msg.data)

rospy.init_node(node_name)
sub = rospy.Subscriber('/user_input', String, getXboxControllerInput)

rospy.spin()

