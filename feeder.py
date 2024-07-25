import os
from gpiozero import Button, LED
from time import sleep
from sequence import Sequence
import requests 
from _thread import start_new_thread
from os import path
from tcp_messages import MessageServer, MessageClient, Message, Connection

def feeder_process(feeder):
    feeder.active = False
    while True: #loops forever
        while not feeder.active:
            pass
        print(f'\tfeeder enabled, feeder.active = {feeder.active}')
        while feeder.active: #wait until the mouse touches the feeder
            if not feeder.sensor.is_pressed:
                print("\tfeeder reached, giving water reward")
                feeder.feed()
                feeder.active = False
                try:
                    feeder.report_feeder()
                except Exception as ME:
                    print('ERROR: feeder.report_feeder not working')
                    print(ME)
        print("\tfeeder disabled")

class Feeder:
    def __init__(self, feed_time, feeder_number, experiment):
        self.feeding_time = feed_time #60ms
        self.sensor = Button(22)
        self.number = feeder_number
        self.solenoid = LED(27)
        self.active = False
        self.finish = False
        self.experiment = experiment
        self.sequence = Sequence()
        # if not self.sensor.is_pressed:
            # self.sensor = Button(22)
            # self.number = 2

    def status(self):
        return {"feeder_number": self.number, "state": "enabled" if self.active else "disabled", "feeding_time": self.feeding_time}

    def test(self, feed_time, reps, wait_time):
        for i in range(reps):
            self.feed(feed_time)
            sleep(wait_time)

    def save_calibration(self, feed_time):
        self.feeding_time = feed_time
        with open("feeder.cal", "w") as f:
            f.write(str(self.feeding_time) + "\n")
            f.write(str(self.number) + "\n")
            
    def report_feeder(self):
        print('\t Starting report_feeder')
        if self.experiment.pi_name == 'maze1':
            if self.experiment.active_exp_name != self.experiment.exp_name and self.experiment.active_exp_name != '':
                print(f'\tActive experiment still running. Finishing active experiment: {self.experiment.active_exp_name}')
                self.experiment.client.finish_experiment(self.experiment.active_exp_name)
            if self.experiment.client.is_active(self.experiment.exp_name):
                if self.experiment.ep_active:
                    print(f'\tfinishing episode: {self.experiment.active_exp_name}')
                    self.experiment.client.finish_episode()
                    sleep(.2)
                print(f'\tstarting episode: {self.experiment.exp_name}')
                rewards_sequence = self.sequence.empty()
                self.experiment.client.start_episode(self.experiment.exp_name, rewards_sequence)
            else:
                if self.experiment.ep_active:
                    print(f'\tfinishing episode: {self.experiment.active_exp_name}')
                    self.experiment.client.finish_episode()
                    sleep(.2)
                print(f'\tfinishing experiment: {self.experiment.exp_name}')
                self.experiment.experiment_finished(self.experiment.exp_name)
                self.experiment.client.finish_experiment(self.experiment.exp_name)
                self.experiment.active_exp_name = ''
            
    def feed(self, feeding_time=None):
        if feeding_time is None:
            feeding_time = self.feeding_time
        self.solenoid.on()
        sleep(feeding_time)
        self.solenoid.off()

    def cancel(self):
        self.active = False
        self.finish = True

