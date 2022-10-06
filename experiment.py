import doors as door
import feeder
from time import sleep
from tcp_messages import MessageServer, MessageClient, Message, Connection
from json_cpp import JsonObject, JsonList
from _thread import start_new_thread
import socket
from os import path

class Experiment:
    def __init__(self, client):
        self.pi_name = socket.gethostname()
        print(self.pi_name)
        self.feed_time = 0
        self.feeder_number = 0
        if path.exists("/home/pi/cellworld_habitat_pi/feeder.cal"):
            with open("/home/pi/cellworld_habitat_pi/feeder.cal", "r") as f:
                lines = f.readlines()
                self.feed_time = float(lines[0].replace("\n", ""))
                self.feeder_number = int(lines[1].replace("\n", ""))

        self.doors = door.Doors()
        self.exp_name = ''
        self.feeders = feeder.Feeder(self.feed_time,self.feeder_number)
        self.feeder_thread = start_new_thread(feeder.feeder_process, (self.feeders, self, client))
        print('Experiment Initialized')

    def experiment_started(self, parameters):
        print('EXP COMMAND: start experiment')
        self.exp_name = parameters.experiment_name
        print(self.exp_name)
        if self.pi_name == 'maze1':
            print('\tclosingdoor1')
            self.doors.close_door(1)
            sleep(.2)
            print('\tclosing door2')
            self.doors.close_door(2)
            sleep(.2)
            print('\tstarting feeder')
            self.feeders.active = True
        else:
            print(self.exp_name)
            print('\tclosingdoor0')
            self.doors.close_door(0)
            sleep(.2)
            print('\tclosing door3')
            self.doors.close_door(3)
            sleep(.2)
        return
        
    def episode_started(self, exp_name):
        self.exp_name = exp_name
        print('EXP COMMAND: start episode')
        print(exp_name)
        if self.pi_name == 'maze1':
            if 'R' not in self.exp_name.split('_')[-1]:
                print('\topening_door2')
                self.doors.open_door(2)
                sleep(.2)
            print('\tclosing door 1')
            self.doors.close_door(1)
            sleep(.2)
        else:
            print('\tclosing door 0')
            self.doors.close_door(0)
            sleep(.2)
            print('\topening_door3')
            self.doors.open_door(3)
            sleep(.2)
            print('\tstarting feeder')
            self.feeders.active = True
        return 
        
    def episode_finished(self, exp_name):
        print('EXP COMMAND: finish episode')
        self.exp_name = exp_name
        print(self.exp_name)
        if self.pi_name == 'maze1':
            print('\topening_door')
            self.doors.open_door(1)
            sleep(.2)
            print('\tclosing door')
            self.doors.close_door(2)
            sleep(.2)
            print('\tstarting feeder')
            self.feeders.active = True
        else:
            print('\tclosing door 3')
            self.doors.close_door(3)
            sleep(.2)
            print('\topening_door 0')
            self.doors.open_door(0)
            sleep(.2)
            print('\tstarting feeder')
        return 
        
    def experiment_finished(self, m):
        print('EXP COMMAND: finish experiment')
        if self.pi_name == 'maze1':
            print('\tclosing door 1')
            self.doors.close_door(1)
            sleep(.2)
            print('\tclosing door 2')
            self.doors.close_door(2)
            sleep(.2)
        else:
            print('\tclosing door 0')
            self.doors.close_door(0)
            sleep(.2)
            print('\tclosing door 3')
            self.doors.close_door(3)
            sleep(.2)
        return

    def prey_entered_arena(self):
        print('EXP COMMAND: prey entered arena')
        if self.pi_name == 'maze1':
            print('\tclosing door 2')
            self.doors.close_door(2)
            sleep(.2)
        return