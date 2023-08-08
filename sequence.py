import matplotlib.pyplot
import random
from cellworld import Cell_group_builder
from json_cpp import JsonList

class Sequence:
    def rand_no_consec_rep(self, reward_cells):
        seq_len = 1
        reward_sequence = [0 for s in range(seq_len)]
        cell = random.choice(list(reward_cells))
        reward_sequence[0] = cell

        for i in range(seq_len-1):
            non_consec_list = reward_cells.copy()
            non_consec_list.pop(reward_cells.index(cell))
            cell = random.choice(non_consec_list)
            reward_sequence[i+1] = cell
        return Cell_group_builder(JsonList(reward_sequence))
