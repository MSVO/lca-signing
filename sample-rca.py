import numpy as np
from LCA import FiniteCellularAutomata

k = 3
n_states = 4
shape = (1,1,3)

rca_neighbours = np.asarray([
    [[0,0,0], [0,0,1]],
    # [[0,0,0], [0,-1,0]],
    # [[0,0,0], [-1,0,0]]
])

rca_neighbours_3d = [

]

reversible_transitions = []

def f1(states):
    matrix = np.asarray([
        [1, 0, 3, 2],
        [0, 2, 2, 3],
        [3, 1, 1, 0],
        [2, 3, 0, 1]
    ])
    return matrix[states[0],states[1]]

def f1_inv(states):
    return f1(states)

reversible_transitions.append([f1, f1_inv])

def f2(states):
    matrix = np.asarray([
        [0, 1, 0, 2],
        [1, 0, 2, 3],
        [3, 3, 1, 0],
        [2, 2, 3, 1]
    ])
    return matrix[states[0],states[1]]

def f2_inv(states):
    return f2(states)

# reversible_transitions.append([f2, f2_inv])

def f3(states):
    matrix = np.asarray([
        [2, 1, 3, 0],
        [3, 0, 1, 2],
        [0, 3, 2, 1],
        [1, 2, 0, 3]
    ])
    return matrix[states[0],states[1]]

def f3_inv(states):
    return f3(states)

# reversible_transitions.append([f3, f3_inv])

reversible_transitions = np.asarray(reversible_transitions)

# init_config = np.random.randint(0,high=n_states,size=shape)
init_config = np.asarray([
    [[2, 0, 3]]
])

ca = FiniteCellularAutomata(shape,n_states,rca_neighbours,reversible_transitions[:,0],init_config=init_config,mode="composition")
ca.print_config()
org = ca.get_config()

i = 0
for i in range(0,5):
    ca.generate_next_configuration()
    print(ca.get_config())
print(i)

# TODO check if f1,f2,f3 are reversible