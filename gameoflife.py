from LCA import FiniteCellularAutomata
import numpy as np
import os
import time

neighbourhood = np.asarray([[0,0], [-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1, -1], [1, 0], [1,1]])

def transition_func(states):
    cell = states[0]
    nb = sum(states[1:])
    if cell == 1:
        if nb < 2:
            return 0
        elif nb > 3:
            return 0
        else:
            return 1
    if cell == 0:
        if nb == 3:
            return 1
        else:
            return 0

shape = (16,16)

n_states = 2

# Glider configuration
init_config = np.zeros(shape)
init_config[0,1] = 1
init_config[1,2] = 1
init_config[2,2] = 1
init_config[2,1] = 1
init_config[2,0] = 1

ca = FiniteCellularAutomata(shape, n_states, neighbourhood, transition_func, init_config)

while True:
    ca.generate_next_configuration()
    os.system('clear')
    ca.print_config()
    time.sleep(0.1)