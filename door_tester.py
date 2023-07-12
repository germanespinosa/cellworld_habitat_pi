#!/usr/bin/python3

from gpiozero import Button
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

B1 = Button(26, pull_up=None, active_state=False)
B2 = Button(20, pull_up=None, active_state=False)

#while True:
#	if B1.is_pressed:
#		print('b1')
#	if B2.is_pressed:
#		print('b2')
#	if not B1.is_pressed and not B2.is_pressed:
#		print('0')
#	sleep(0.005)

b1p = 0
b2p = 0
while True:
	if B1.is_pressed:
		b1p = 1
	else:
		b1p = 0
	if B2.is_pressed:
		b2p = 1
	else:
		b2p = 0
	print([b1p,b2p])
	sleep(0.1)

