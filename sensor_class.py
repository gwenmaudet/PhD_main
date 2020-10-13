import numpy as np
import random
class sensor():
    def __init__(self, mean, std,prct_reception, id):  # emission frequence = nb of emission in 1 day
        self.mean = mean
        self.std = std
        self.prct_reception = prct_reception
        self.id = id
    def one_simulation(self):
        p = random.random()
        if p < self.prct_reception:
            return np.random.normal(self.mean, self.std)
        else:
            return None
    def multi_simulation(self, nb_simulation):
        nb_reception = 0
        for i in range (nb_simulation):
            p = random.random()
        return np.random.normal(self.mean, self.std, nb_simulation)