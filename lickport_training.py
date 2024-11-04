from gpiozero import Button, LED
import time
from os import path
import sys

class Feeder:
	def __init__(self, max_reward=0.8, reward_delay=1.0, reward_duration=0.005):
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

		print(f'reward_duration: {reward_duration:0.3f}\nmax_reward: {max_reward:0.3f}\nreward_delay: {reward_delay:0.3f}')
		self.state_loop(reward_duration, max_reward, reward_delay)

	def feed(self):
		self.solenoid.on()
		time.sleep(self.feed_time)
		self.solenoid.off()

	def state_loop(self, ml_per_reward=0.005,  max_reward=0.8, reward_delay=1.0, delay=0.005):
		cnt = 0
		print('Starting lickport training...')
		while True:
			current_time = time.time()
			#print(self.sensor.is_pressed)
			#print(current_time - self.time)
			if (not self.sensor.is_pressed) & ((current_time - self.time) > reward_delay):
				self.feed()
				self.time = time.time()
				cnt = cnt + 1
				print(f'{cnt * ml_per_reward:0.3f}mL dispensed')

			if (cnt * ml_per_reward) > max_reward:
				print(f'max_reward ({max_reward}) reached... stopping.')
				break
			time.sleep(delay)



print(sys.argv)
if len(sys.argv) > 0:
	if len(sys.argv) == 2:
                ml_per_reward = 0.005
                max_reward = float(sys.argv[1])
                reward_delay = 1.0
	elif len(sys.argv) == 3:
                ml_per_reward = 0.005
                max_reward = float(sys.argv[1])
                reward_delay = float(sys.argv[2])
	elif len(sys.argv) == 4:
                ml_per_reward = float(sys.argv[3])
                max_reward = float(sys.argv[1])
                reward_delay = float(sys.argv[2])
	else:
                ml_per_reward = 0.005
                max_reward = 0.8
                reward_delay = 1.0


Feeder(max_reward, reward_delay, ml_per_reward)
