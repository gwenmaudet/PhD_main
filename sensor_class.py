import numpy as np
import random


class sensor():
    def __init__(self, mean_dif, std, prct_reception, id):  # emission frequence = nb of emission in 1 day
        self.mean_dif = mean_dif
        self.std = std
        self.prct_reception = prct_reception
        self.id = id


    def multi_simulation(self, nb_simulation, simulations):
        nb_reception = 0
        simulation = {}
        for i in range(nb_simulation):
            p = random.random()
            if p < self.prct_reception:
                val = np.random.normal(self.mean_dif, self.std)
                simulation[i] = val
                simulations[i].append(val)
        """return np.concatenate(
            (np.random.normal(self.mean, self.std, nb_reception), np.array(None * (nb_simulation - nb_reception))),
            axis=None)"""
        return simulation, simulations
