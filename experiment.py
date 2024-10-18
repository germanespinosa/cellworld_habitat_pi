from cellworld import Cell_group_builder
import doors as door
import feeder
import sequence
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
        self.ep_active = False
        self.active_exp_name = ''
        self.client = client
        self.ep_count = 0

        self.feed_time = 0
        self.feeder_number = 0
        if path.exists("./feeder.cal"):
            with open("./feeder.cal", "r") as f:
                lines = f.readlines()
                self.feed_time = float(lines[0].replace("\n", ""))
                self.feeder_number = int(lines[1].replace("\n", ""))

        self.doors = door.Doors()
        self.exp_name = ''
        self.reward_sequence = Cell_group_builder()
        self.reward_cells = Cell_group_builder()
        self.reward_index = None
        self.cell_id = None
        self.feeders = feeder.Feeder(self.feed_time, self.feeder_number, self)
        self.feeder_thread = start_new_thread(feeder.feeder_process, (self.feeders,))
        print('Experiment Initialized')

    def experiment_started(self, parameters):
        print('EXP COMMAND: start experiment')
        self.exp_name = parameters.experiment_name
        self.reward_cells = parameters.rewards_cells
        print(f'\t{self.exp_name}')
        print(f'\treward_cells: {self.reward_cells}')
        if not self.ep_active:
            if self.pi_name == 'maze1':
                print('\tclosing door2')
                self.doors.close_door(2)
                sleep(.2)
                print('\tstarting feeder')
                self.feeders.active = True
            else:
                self.cell_id = self.reward_cells[self.feeder_number - 200]
                print(f'\tMY cell_id: {self.cell_id}')
                print('\tdisabling feeder')
                self.feeders.active = False
        else:
            if self.pi_name == 'maze1':
                print('EPISODE IS STILL ACTIVE')
                print(f'\tFinishing episode for {self.active_exp_name}')
                self.client.finish_episode()
        return
        
    def episode_started(self, parameters):
        print('EXP COMMAND: start episode')
        self.ep_active = True
        self.active_exp_name = parameters.experiment_name
        print(f'\t{self.active_exp_name}')
        self.reward_sequence = parameters.rewards_sequence
        print(f'\t{self.reward_sequence}')
        self.reward_index = 0
        if self.pi_name == 'maze1':
            print('\tclosing door 1')
            self.doors.close_door(1)
            if 'R' not in self.exp_name.split('_')[-1]:
                print('\topening_door2')
                self.doors.open_door(2)
                sleep(.2)
            print('\tdisabling feeder')
            self.feeders.active = False
        else:
            print(f'\tcurrent sequence index: {self.reward_index} / {len(self.reward_sequence) - 1}')
            current_cell_id = self.reward_sequence[self.reward_index]
            if self.reward_sequence[self.reward_index] == self.cell_id:
                print(f'\tMY cell_id ({self.cell_id}) == CURRENT cell_id ({self.reward_sequence[self.reward_index]})')
                print('\tstarting feeder')
                self.feeders.active = True
            else:
                print(f'\tMY cell_id ({self.cell_id}) != CURRENT cell_id ({self.reward_sequence[self.reward_index]})')
                print('\tdisabling feeder')
                self.feeders.active = False
        return 

    def reward_reached(self):
        print('EXP COMMAND: reward_reached')
        self.reward_index += 1
        print(f'\t{self.reward_sequence}')
        print(f'\tcurrent sequence index: {self.reward_index} / {len(self.reward_sequence)-1}')
        if self.reward_index >= len(self.reward_sequence):
            print(f'\tlast reward reached')
            if self.pi_name == 'maze1':
                print('\topening_door2')
                self.doors.open_door(2)
                print('\tstarting feeder')
                self.feeders.active = True
            else:
                print('\tdisabling feeder')
                self.feeders.active = False
        else:
            if self.reward_sequence[self.reward_index] == self.cell_id:
                print(f'\tMY cell_id ({self.cell_id}) == CURRENT cell_id ({self.reward_sequence[self.reward_index]})')
                print('\tstarting feeder')
                self.feeders.active = True
            else:
                print(f'\tMY cell_id ({self.cell_id}) != CURRENT cell_id ({self.reward_sequence[self.reward_index]})')
                print('\tdisabling feeder')
                self.feeders.active = False
    def episode_finished(self, exp_name):
        print('EXP COMMAND: finish episode')
        self.ep_active = False
        self.active_exp_name = exp_name
        print(f'\t{exp_name}')
        return 
        
    def experiment_finished(self, exp_name):
        print('EXP COMMAND: finish experiment')
        print(f'\t{exp_name}')
        if self.pi_name == 'maze1':
            print('\tclosing door 2')
            self.doors.close_door(2)
            sleep(.2)
        return

    def prey_entered_arena(self):
        print('EXP COMMAND: prey entered arena')
        if self.pi_name == 'maze1':
            print('\tclosing door 2')
            self.doors.close_door(2)
            sleep(.2)
        return

    def experiment_resumed(self, parameters):
        print('EXP COMMAND: experiment resumed')
        self.exp_name = parameters.experiment_name
        print(f'\t{self.exp_name}')
        if self.pi_name == 'maze1':
            self.feeders.active = True
        else:
            self.feeders.active = False
        return
