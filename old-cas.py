import numpy as np

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
