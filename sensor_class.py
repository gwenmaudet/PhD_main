import numpy as np
import random


class sensor():
    def __init__(self, mean, std, prct_reception, id, emission_periode=10, emssion_sending_beggining=0):  # emission frequence = nb of emission in 1 day
        self.mean = mean
        self.std = std
        self.prct_reception = prct_reception
        self.id = id
        self.emission_periode =emission_periode
        self.emssion_sending_beggining = emssion_sending_beggining
    def one_simulation(self):
        p = random.random()
        if p < self.prct_reception:
            return np.random.normal(self.mean, self.std)
        else:
            return None

    def multi_simulation(self, nb_simulation):
        nb_reception = 0
        for i in range(nb_simulation):
            p = random.random()
            if p < self.prct_reception:
                nb_reception += 1
        """return np.concatenate(
            (np.random.normal(self.mean, self.std, nb_reception), np.array(None * (nb_simulation - nb_reception))),
            axis=None)"""
        return np.random.normal(self.mean, self.std, nb_reception)
