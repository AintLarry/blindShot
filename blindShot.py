#!/usr/bin/env python3

#https://github.com/AintLarry/blindShot.git

#Imports
import time
import subprocess

import RPi.GPIO as GPIO

#GPIO 

GPIO.setmode(GPIO.BCM)
led = 18

GPIO.setup(led, GPIO.OUT)

#GPIO.output(led, GPIO.HIGH)

#Programm-Start

volume = 500
speed = 200

subprocess.call(['/usr/bin/espeak-ng', '-vde', 'Sprachausgabe gestartet.', '-a ' + str(volume), '-s ' + str(speed)])
subprocess.call(['/usr/bin/espeak-ng', '-vde', 'Bitte gebe deinen Stand ein, und bestätige mit Enter.', '-a ' + str(volume), '-s ' + str(speed)])

GPIO.output(led, GPIO.HIGH)
onrange = input()
GPIO.output(led, GPIO.LOW)

subprocess.call(['/usr/bin/espeak-ng', '-vde', 'Stand ' + onrange + 'gewählt.', '-a ' + str(volume), '-s ' + str(speed)])


#Functions

def getVarNum(type, receivedData):
	#Typelist:
	#Range, X, Y, Count, DecValue

	index = receivedData.find(type.encode())

	if(index != -1):

		index = index + len(str(type)) + 2
		string = receivedData[index:index+20]

		index = string.find(",".encode())
		string = string[:index]

		return string;
	else:
		return;

	return;

def getVarText(type, receivedData):
	#Typelist:
	#MessageVerb, IsWarmup

	index = receivedData.find(type.encode())

	if(index != -1):

		index = index + len(str(type)) + 3
		string = receivedData[index:index+20]

		index = string.find(",".encode())-1
		string = string[:index]

		return string;x

	else:
		return;
	return;

def getOrientation(x, y):

	if(x >= 0 and y >= 0):
		return "oben rechts"
	if(x < 0 and y >= 0):
		return "oben links"
	if(x >= 0 and y < 0):
		return "unten rechts"
	if(x < 0 and y < 0):
		return "unten links"

	return  "";

#Variables

shotcount = 0
globalwarmup = 1;
speak = "";


#UDP-Listener

import socket

UDP_IP = ""
UDP_PORT = 2168

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:

	data, addr = sock.recvfrom(4096)

	verb = str(getVarText("MessageVerb", data))
	verb = verb[2:-1]

	range = str(getVarNum("Range", data))
	range = range[3:-1]

	GPIO.output(led, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(led, GPIO.LOW)

	#if(verb == "Shot"):
	if(verb == "Shot" and range == onrange):

		decvalue = str(getVarNum("DecValue", data))
		y = str(getVarNum("Y", data))
		x = str(getVarNum("X", data))
		count = str(getVarNum("Count", data))

		decvalue = decvalue[2:-1]
		y = y[2:-1]
		x = x[2:-1]
		count = count[2:-1]

		orientation = getOrientation(int(x), int(y))

		shotype = "";

		warmup = str(getVarText("IsWarmup", data))
		warmup = warmup[2:-1]

		if(warmup == "ru"):
			shottype = "Probeschuss"
		else:
			shottype = "Wertungsschuss"
			if(globalwarmup == 1):
				globalwarmup = 0
				shotcount = 0

		shotcount = shotcount + 1
		count = str(shotcount)

		speak = shottype + " " + count + ", " + decvalue + " Ringe, " + orientation + "." 

		time.sleep(2)

		print(speak)


		subprocess.call(['/usr/bin/espeak-ng', '-vde', speak, '-a ' + str(volume), '-s ' + str(speed)])


