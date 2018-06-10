#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import threading
import sys

btn1 = 10
btn2 = 12

GPIO.setmode(GPIO.BOARD)

GPIO.setup(btn1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btn2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0

last_state = GPIO.HIGH

def handle(pin):
	global last_state, counter
	state1 = GPIO.input(btn1)
	state2 = GPIO.input(btn2)
	#print('handle' + str(state1) + ', ' + str(state2))
	if state1 != last_state:
		if state1 != state2:
			counter += 1
		else:
			counter -= 1
		print counter
	last_state = state1

GPIO.add_event_detect(btn1, GPIO.BOTH, handle)

print('off we go')
while True:
	time.sleep(1)
