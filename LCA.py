
# class Cell:
#     def __init__(self, n_states, state):
#         assert type(state) == int and 
#             type(n_states) == int and 
#             state >= 0 and 
#             state < n_states
#         self.n_states = n_states
#         self.state = state
    
#     def set_state(state):
#         assert state >= 0 and
#             state < n_states
#         self.state = state

import numpy as np

class FiniteCa1d:
    # Transition function should be defined from set of all possible neighbourhoods to set of all possible states
    def __init__(self, n_states, length, neighbourhood, transition, initial_states=None):
        assert type(neighbourhood) == np.ndarray
        assert callable(transition)

        self.l = length
        self.n_states = n_states
        self.neighbourhood = neighbourhood
        self.transition = transition
        
        if initial_states is None:
            self.cells = np.zeros(self.n_states)
        else:
            assert type(initial_states) == np.ndarray and self.validate_states(initial_states)
            self.cells = np.asarray(initial_states)

    def validate_states(self, initial_states):
        # todo
        return True

    def get_neighbour_states(Vself, index):
        neigh = (index + self.neighbourhood) % self.l
        states = list()
        for i in neigh:
            states.append(self.cells[tuple(i)])
        return states

    def generate_next_configuration(self):
        neighbourhoods = list(map(self.get_neighbour_states, range(self.l)))
        new_config = np.asarray(list(map(self.transition, neighbourhoods)))
        assert self.validate_states(new_config)
        self.cells = new_config

    def print_config(self):
        print(self.cells)

class FiniteCellularAutomata:
    def __init__(self, shape, n_states, neighbourhood, transition, init_config=None):
        self.shape = shape
        self.n_states = n_states,
        self.neighbourhood = neighbourhood
        self.transition = transition
        assert neighbourhood.shape[1] == len(self.shape)

        if init_config is None:
            self.cells = np.zeros(shape)
        else:
            assert self.validate_config(init_config)
            self.cells = init_config

    def validate_config(self, config):
        # todo
        return True

    def get_neighbour_states(self, index):
        neigh = (index + self.neighbourhood) % self.shape
        states = list()
        for i in neigh:
            states.append(self.cells[tuple(i)])
        return states

    def generate_indices(self):
        dim = len(self.shape)
        def get_indices_till(dim, shape):
            if dim == 1:
                return [(i,) for i in range(shape[dim-1])]
            else:
                inner = get_indices_till(dim-1, shape)
                outer = []
                for i in range(shape[dim-1]):
                    for x in inner:
                        outer.append((i,) + x)
                return outer
        return get_indices_till(dim, self.shape)
        
    def generate_next_configuration(self):
        # todo : generate indices of all cells
        indices = self.generate_indices()
        neighbourhoods = list(map(self.get_neighbour_states, indices))
        new_config = np.asarray(list(map(self.transition, neighbourhoods))).reshape(self.shape)
        assert self.validate_config(new_config)
        self.cells = new_config

    def get_config(self):
        return self.cells

    def print_config(self):
        print(self.cells)


class FiniteCa2d(FiniteCellularAutomata):
    def __init__(self, shape, n_states, neighbourhood, transition, init_config=None):
        super().__init__(shape, n_states, neighbourhood, transition, init_config=init_config)
        assert len(self.shape) == 2

    def get_neighbour_states(self, index):
        pass


if __name__ == "__main__":
    def transition(neighbours):
        if neighbours[0] != neighbours[1]:
            return 1
        else:
            return 0
    
    ca = FiniteCa1d(2, 10, np.asarray([0, 1]), transition, initial_states=np.asarray([0,1,0,1,1,0,0,0,1,1]))
    for i in range(3):
        ca.print_config()
        ca.generate_next_configuration()
