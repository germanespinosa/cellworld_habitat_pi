#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep
import sys

print(len(sys.argv))
if len(sys.argv) > 0:
	if len(sys.argv) == 2:
		delay = float(sys.argv[1])
		reps = 100
	elif len(sys.argv) == 3:
		delay = float(sys.argv[1])
		reps = int(sys.argv[2])
	else:
		delay = 0.05
		reps = 100


print(f'delay = {delay}, reps = {reps}')


input = 22
output = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(input, GPIO.IN)
GPIO.setup(output, GPIO.OUT)

for i in range(reps):
	GPIO.output(output, True)
	sleep(delay)
	GPIO.output(output, False)
	print(GPIO.input(input))
	sleep(0.5);

GPIO.cleanup()


