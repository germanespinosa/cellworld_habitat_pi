#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep

try:

	delay = 0.005
	input = 22
	output = 27
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(input, GPIO.IN)
	GPIO.setup(output, GPIO.OUT)

	for i in range(100):
		GPIO.output(output, True)
		sleep(delay)
		GPIO.output(output, False)
		print(GPIO.input(input))
		sleep(0.5);
	GPIO.cleanup()

except KeyboardInterrupt:
	print('Valve closed')
	GPIO.output(output, False)
	GPIO.cleanup()



