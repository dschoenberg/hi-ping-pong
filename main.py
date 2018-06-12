#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import threading
import sys
import rotary_encoder



import urllib2
import json

btn1 = 10
btn2 = 12

GPIO.setmode(GPIO.BOARD)

playerList = None
winnerIndex = 0
loserIndex = 0

def updateDisplay():
	print('winner: ' + playerList[winnerIndex]["firstName"] + ' ' + playerList[winnerIndex]["lastName"])

def updateWinner(forward):
	global winnerIndex

	if forward:
		winnerIndex = winnerIndex + 1
		if winnerIndex >= len(playerList):
			winnerIndex = 0
	else:
		winnerIndex = winnerIndex - 1
		if winnerIndex < 0:
			winnerIndex = len(playerList) - 1
	updateDisplay()

def getPlayers():
	global playerList
	url = "http://hi-ping-pong.herokuapp.com/players"
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	f = opener.open(req)
	playerList = json.loads(f.read())

if __name__ == "__main__":
	print('off we go')
	getPlayers()
	decoder = rotary_encoder.decoder(GPIO, 10, 12, updateWinner)
	while True:
		time.sleep(1e6)

