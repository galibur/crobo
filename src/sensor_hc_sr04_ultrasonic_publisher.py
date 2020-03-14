#!/usr/bin/python

import rospy
from std_msgs.msg import String

import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 11
GPIO_ECHO = 9
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO_TRIGGER2 = 10
GPIO_ECHO2 = 12
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

rospy.init_node('sensor_hc_sr04_ultrasonic_crobo_publisher')
pub = rospy.Publisher('system', String, queue_size=10)

msg_str = String()

id = 1
id2 = 2


def distanz(trigger, echo):
	# setze Trigger auf HIGH
	GPIO.output(trigger, True)

	# setze Trigger nach 0.01ms aus LOW
	time.sleep(0.00001)
	GPIO.output(trigger, False)

	StartZeit = time.time()
	StopZeit = time.time()

	# speichere Startzeit
	while GPIO.input(echo) == 0:
		StartZeit = time.time()

	# speichere Ankunftszeit
	while GPIO.input(echo) == 1:
		StopZeit = time.time()

	# Zeit Differenz zwischen Start und Ankunft
	TimeElapsed = StopZeit - StartZeit
	# mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
	# und durch 2 teilen, da hin und zurueck
	distanz = (TimeElapsed * 34300) / 2

	return distanz


# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

while not rospy.is_shutdown():
       	abstand = distanz(GPIO_TRIGGER, GPIO_ECHO)
	msg_str = '{"hc_sr04_distance_' + str(id) + '":' + str(abstand) + '}'
	pub.publish(msg_str)

       	abstand = distanz(GPIO_TRIGGER2, GPIO_ECHO2)
	msg_str = '{"hc_sr04_distance_' + str(id2) + '":' + str(abstand) + '}'
	pub.publish(msg_str)

	time.sleep(1)

sys.exit(1)
