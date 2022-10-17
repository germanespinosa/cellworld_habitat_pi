import os
from gpiozero import Button, LED
from time import sleep
import requests 
from _thread import start_new_thread
from os import path
from tcp_messages import MessageServer, MessageClient, Message, Connection

def feeder_process(feeder, experiment):
    feeder.active = False
    while True: #loops forever
        while not feeder.active:
            pass
        print("\tfeeder enabled")
        while feeder.active: #wait until the mouse touches the feeder
            if not feeder.sensor.is_pressed:
                feeder.feed()
                feeder.active = False
                feeder.report_feeder(experiment)
                break
        print("\tfeeder disabled")
class Feeder:
    def __init__(self, feed_time, feeder_number):
        self.feeding_time = feed_time #60ms
        self.sensor = Button(22)
        self.number = feeder_number
        self.solenoid = LED(27)
        self.active = False
        self.finish = False
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
            
    def report_feeder(self, experiment):
        if experiment.pi_name == 'maze1':
            if not experiment.active_exp_name == experiment.exp_name:
                print(f'\t active experiment still running, finishing active experiment: {experiment.active_exp_name}')
                experiment.client.finish_experiment(experiment.active_exp_name)
            if experiment.client.is_active(experiment.exp_name):
                print(f'\tstarting episode: {experiment.exp_name}')
                print(experiment.client.start_episode(experiment.exp_name))
            else:
                print(f'\tfinishing experiment: {experiment.exp_name}')
                experiment.experiment_finished(experiment.exp_name)
        else:
            print(f'\tfinishing episode: {experiment.active_exp_name}')
            experiment.client.finish_episode()
            
    def feed(self, feeding_time=None):
        if feeding_time is None:
            feeding_time = self.feeding_time
        self.solenoid.on()
        sleep(feeding_time)
        self.solenoid.off()

    def cancel(self):
        self.active = False
        self.finish = True

