
import numpy as np
from PIL import Image

class FiniteCellularAutomata:

    # neighbourhood is a list of relative indices in CA
    # Transition function takes len(neighbourhood) number of states and returns a state

    def __init__(self, shape, n_states, neighbourhood, transition, init_config=None, mode="normal"):
        self.mode = mode
        self.shape = shape
        self.n_states = n_states
        if mode == "normal":
            self.neighbourhood = neighbourhood
            self.transition = transition
            assert self.neighbourhood.shape[1] == len(self.shape)
        elif mode == "composition":
            self.all_neighs = neighbourhood
            self.all_trans = transition
        

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
            dimlen = shape[-dim]
            if dim == 1:
                return [(i,) for i in range(dimlen)]
            else:
                inner = get_indices_till(dim-1, shape)
                outer = []
                for i in range(dimlen):
                    for x in inner:
                        outer.append((i,) + x)
                return outer
        return get_indices_till(dim, self.shape)
        
    def generate_next_configuration(self):
        # todo : generate indices of all cells
        if self.mode == "normal":
            indices = self.generate_indices()
            neighbourhoods = list(map(self.get_neighbour_states, indices))
            new_config = np.asarray(list(map(self.transition, neighbourhoods))).reshape(self.shape)
            assert self.validate_config(new_config)
            self.cells = new_config
        elif self.mode == "composition":
            indices = self.generate_indices()
            for i in range(len(self.all_neighs)-1,-1,-1):
                self.neighbourhood = self.all_neighs[i]
                self.transition = self.all_trans[i]
                neighbourhoods = list(map(self.get_neighbour_states, indices))
                new_config = np.asarray(list(map(self.transition, neighbourhoods))).reshape(self.shape)
                assert self.validate_config(new_config)
                self.cells = new_config

    def get_config(self):
        return self.cells

    def show_config(self):
        if self.n_states == 2:
            im = Image.fromarray(self.cells, mode="1")
            im.show()

    def print_config(self):
        print(self.cells)

