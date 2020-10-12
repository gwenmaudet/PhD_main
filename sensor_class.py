import numpy as np

class sensor():
    def __init__(self, mean, std, id):  # emission frequence = nb of emission in 1 day
        self.mean = mean
        self.std = std
        self.id = id
    def one_simulation(self):
        return np.random.normal(self.mean, self.std)

    def multi_simulation(self, nb_simulation):
        return np.random.normal(self.mean, self.std, nb_simulation)