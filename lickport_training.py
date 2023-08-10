from gpiozero import Button, LED
import time
from os import path

class Feeder:
	def __init__(self):
		self.feed_time = 0
		self.feeder_number = 0
		if path.exists('./feeder.cal'):
			with open('./feeder.cal', 'r') as f:
				lines = f.readlines()
				self.feed_time = float(lines[0].replace('\n', ''))
				self.feeder_number = int(lines[1].replace('\n', ''))

		self.sensor = Button(22)
		self.solenoid = LED(27)
		self.time = time.time()

		self.state_loop()

	def feed(self):
		self.solenoid.on()
		time.sleep(self.feed_time)
		self.solenoid.off()

	def state_loop(self, max_reward=0.3, reward_delay=1.0, delay=0.005):
		cnt = 0
		while True:
			current_time = time.time()
			#print(self.sensor.is_pressed)
			#print(current_time - self.time)
			if (not self.sensor.is_pressed) & ((current_time - self.time) > reward_delay):
				self.feed()
				self.time = time.time()
				cnt = cnt + 1
				print(f'{cnt * 0.002:0.3f}uL dispensed')

			if (cnt * 0.002) > max_reward:
				print(f'max_reward ({max_reward}) reached... stopping.')
				break
			time.sleep(delay)

Feeder()
