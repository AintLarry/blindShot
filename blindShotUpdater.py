#!/usr/bin/env python3

import time
import subprocess
import os

from ftplib import FTP

#Programm-Start
volume = 200
subprocess.call(['/usr/bin/espeak-ng', '-vde', 'Suche nach Updates.', '-a ' + str(volume), '-s 200'])

#Variablen
ftpaddr = "www.w01a0a40.kasserver.com"
ftpuser = "w01a0a40"
ftppswd = "Blumentopf1200"

#Functions

def searchForUpdates(v):
	try:
		ftp = FTP(ftpaddr)
		ftp.login(ftpuser, ftppswd)

		ftp.cwd("BlindShot")

		lf = open("/home/pi/dlv.txt", "w")
		ftp.retrlines("RETR loadableversion.txt", lf.write)
		lf.close()

		f = open("/home/pi/dlv.txt", "r")
		loadableversion = f.readline()

		if(loadableversion <= v):
			return False

		if(loadableversion > v):

			os.remove("/home/pi/version.txt")
			os.rename("/home/pi/dlv.txt", "/home/pi/version.txt")

			lf = open("/home/pi/blindShot.py", "wb")
			ftp.retrbinary("RETR blindShot.py", lf.write)
			lf.close()

			return True
	except:
			return False

def getInstalledVersion(file):
	f = open(file, "r")
	return(f.readline())


#Ausführen

print(getInstalledVersion("/home/pi/version.txt"))

if(searchForUpdates(getInstalledVersion("/home/pi/version.txt")) == False):
	print("Programm ist auf dem aktuellen Stand.")
	subprocess.call(["python3", "/home/pi/blindShot.py"])
else:
	print("Programm wurde aktualisiert.")
	subprocess.call(["python3", "/home/pi/blindShot.py"])
