#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import rotary_encoder
import urllib2
import json

GPIO.setmode(GPIO.BOARD)

winnerPin1 = 10
winnerPin2 = 12
loserPin1 = 3
loserPin2 = 5
submitPin = 7

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

def updateLoser(forward):
	global loserIndex

	if forward:
		loserIndex = loserIndex + 1
		if loserIndex >= len(playerList):
			loserIndex = 0
	else:
		loserIndex = loserIndex - 1
		if loserIndex < 0:
			loserIndex = len(playerList) - 1
	updateDisplay()

def submitGame():
	print('submitting game...')

def getPlayers():
	global playerList
	url = "http://hi-ping-pong.herokuapp.com/players"
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	f = opener.open(req)
	playerList = json.loads(f.read())
	print(str(len(playerList)) + ' players loaded')

if __name__ == "__main__":
	getPlayers()
	rotary_encoder.decoder(GPIO, winnerPin1, winnerPin2, updateWinner)
	rotary_encoder.decoder(GPIO, loserPin1, loserPin2, updateLoser)
	GPIO.add_event_detect(submitPin, GPIO.FALLING, submitGame)
	while True:
		time.sleep(1e6)

