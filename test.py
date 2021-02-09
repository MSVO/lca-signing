from LCA import FiniteCellularAutomata
import numpy as np

ca = FiniteCellularAutomata((8,8,2), 2, np.asarray([[0,1,0]]), lambda x: 0)
print(ca.generate_indices())