from LCA import FiniteCellularAutomata
import numpy as np

def transition_func(nbhood_states):
    return sum(nbhood_states) % 2

init_config = np.asarray([1,0,0,0,0,0,0,0]).reshape((2,4)).astype(int)
ca = FiniteCellularAutomata((2,4), 2, np.asarray([[1,0], [0,1]]), transition_func, init_config=init_config)
ca.print_config()
for i in range(10):
    ca.generate_next_configuration()
    ca.print_config()
