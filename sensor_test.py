import os
from gpiozero import Button, LED
from time import sleep

sensor = Button(22)
while (True):
    print(sensor.is_pressed)
