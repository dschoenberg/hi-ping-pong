#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
import RPi.GPIO as GPIO
import time
import rotary_encoder
import urllib2
import json
import requests
import sys
from subprocess import Popen, PIPE

GPIO.setmode(GPIO.BOARD)

lcd = Adafruit_CharLCD()

winnerPin1 = 10
winnerPin2 = 12
loserPin1 = 16
loserPin2 = 18
submitPin = 7

playerList = None
winnerIndex = 0
loserIndex = 0

def writeMessage(message):
	global lcd
	lcd.clear()
	lcd.message(message)

def getWinner():
	return playerList[winnerIndex]

def getLoser():
	return playerList[loserIndex]

def getPlayerName(player):
	first = player["firstName"][:1]
	last = player["lastName"]
	return (first + '.' + last)

def updateDisplay():
	winner = getPlayerName(getWinner())
	loser = getPlayerName(getLoser())
	print('winner: ' + winner)
	print('loser:  ' + loser)

	writeMessage('winner: ' + winner + '\nloser: ' + loser)

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
	if winnerIndex == loserIndex:
		updateWinner(forward)

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
	if loserIndex == winnerIndex:
		updateLoser(forward)
	
	updateDisplay()

submitting = False
def submitGame(pin):
	global submitting
	print('submitting game...')
	print('winner: ' + playerList[winnerIndex]['_id'])
	print('loser:  ' + playerList[loserIndex]['_id'])

	data = {
		'winner':playerList[winnerIndex]['_id'],
		'loser':playerList[loserIndex]['_id']
	}

	if not submitting:
		submitting = True #I regret nothing!
		req = requests.post("http://hi-ping-pong.herokuapp.com/match", data=data)
		print(req)
		submitting = False

def getPlayers():
	global playerList, lcd
	print('requesting players')
	writeMessage('requesting players')

	url = "http://hi-ping-pong.herokuapp.com/players"
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	f = opener.open(req)
	playerList = json.loads(f.read())
	#print(str(playerList))
	print(str(len(playerList)) + ' players loaded')
	writeMessage(str(len(playerList)) + ' players loaded')

	time.sleep(3)
	updateDisplay()

def getIP():
	cmd = "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output.strip()

if __name__ == "__main__":
	writeMessage('Welcome\n' + getIP())
	
	getPlayers()
	rotary_encoder.decoder(GPIO, winnerPin1, winnerPin2, updateWinner)
	rotary_encoder.decoder(GPIO, loserPin1, loserPin2, updateLoser)
	
	GPIO.setup(submitPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(submitPin, GPIO.FALLING, submitGame)
	
	while True:
		try:
			time.sleep(1e6)
		except KeyboardInterrupt:
			lcd.clear()
			lcd.message('Shutting down')
			GPIO.cleanup()
			sys.exit()


