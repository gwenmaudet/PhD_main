import conf


import numpy as np
import random
from math import *
import statistics
import json
import os
"""
       ----TOOLS----
"""
def get_mean_first_value(list):
    first_values = [val[0] for val in list]
    return statistics.mean(first_values)




class sensor():
    def __init__(self, std=0, prct_reception=0, id=0, emission_periode=None, first_emssion=None, receptions=[]):  # emission frequence = nb of emission in 1 day
        self.std = std
        self.prct_reception = prct_reception
        self.id = id
        self.emission_periode =emission_periode
        self.first_emssion = first_emssion
        self.receptions = receptions

        self.nb_of_values_required = ceil(pow(conf.quantille_gauss * self.std / conf.delta_theta, 2)) #threshold for mnimum number of values

    def one_simulation(self, t, temp):
        p = random.random()
        if p < self.prct_reception:
            reception = np.random.normal(temp, self.std)
            self.receptions.append([t, reception])
            print('-------')
            print(self.id)
            print(self.receptions)
            return reception
        else:
            return None

    def set_reception(self,receptions):
        self.receptions = receptions


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

    def get_modelised_value(self):
        n = len(self.receptions)

        if n >= self.nb_of_values_required:
            if n ==1:
                return self.receptions[0], n
            else:
                return get_mean_first_value(self.receptions[n - self.nb_of_values_required: n]), self.nb_of_values_required
        else:
            return None

class sensors():

    def __init__(self, sensor_set=[]):
        self.sensors = []
        for sensor in sensor_set:
            self.sensors.append(sensor)

    def add_sensor(self, sensor):
        self.sensors.append(sensor)


    def get_response_from_gate_at_instant_t(self, t, temp):
        for i in range (len(self.sensors)):
            sensor = self.sensors[i]
            print(str(sensor.id))
            print(str(sensor.receptions))
            if t % sensor.emission_periode == sensor.first_emssion:
                    print(sensor.one_simulation(t, temp))
            print("#####")

    def get_modelised_value_at_time_t(self,t):
        value_modelisation = []
        for sensor in self.sensors:

            reception = [item for item in sensor.receptions if item[0] == t]
            if not reception:
                reception = None
            else:
                print('yo')
                print(reception)
                print('ploup')
                reception = reception[0]
                modeled_value = sensor.get_modelised_value()
                if modeled_value is not None:
                    value_modelisation.append(modeled_value)

        if len(value_modelisation) >= 1:
            value_modelisation = sorted(value_modelisation, key=lambda tup: tup[1])
            return value_modelisation[0][0]
        return None

    def write_in_a_json_file_the_sensor_responses(self):
        if os.path.isfile(conf.sensor_with_reception_file_name):
            os.remove(conf.sensor_with_reception_file_name)
            print("RECEPTION FILE REMOVED !")
        receptions = []
        for sensor in self.sensors:
            receptions.append({'receptions': sensor.receptions,
                                     'std': sensor.std, 'id': sensor.id})
        with open(conf.sensor_with_reception_file_name, 'w+') as outfile:
            json.dump(receptions, outfile, indent=4)
            print("NEW RECEPTION FILE CREATED")
