import conf


import numpy as np
import random
from math import *
import statistics
import json
import os
from scipy import stats

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

        self.nb_of_values_required = ceil(pow(conf.quantille_gauss * self.std / conf.delta_theta, 2)) #threshold for mnimum number of values

    def one_simulation(self, t, temp):
        p = random.random()
        if p < self.prct_reception:
            reception = np.random.normal(temp, self.std)
            # self.receptions.append([t, reception])
            return [t, reception]
        else:
            return None

    def set_reception(self, receptions):
        self.receptions = receptions

    """def get_modelised_value(self):
        n = len(self.receptions)

        if n >= self.nb_of_values_required:
            if n ==1:
                return self.receptions[0], n
            else:
                return get_mean_first_value(self.receptions[n - self.nb_of_values_required: n]), self.nb_of_values_required
        else:
            return None"""


class sensors():
    def __init__(self, sensor_set=[]):
        self.sensors = {}
        self.receptions = {}
        for sensor in sensor_set:
            self.sensors[sensor.id] = sensor
            self.receptions[sensor.id] = []
    def add_sensor(self, sensor, reception=[]):
        self.sensors[sensor.id] = sensor
        self.receptions[sensor.id] = reception

    def get_response_from_gate_at_instant_t(self, t, temp):
        simulations = {}
        for i in self.sensors:
            sensor = self.sensors[i]
            if t % sensor.emission_periode == sensor.first_emssion:
                simulation = sensor.one_simulation(t, temp)
                if simulation is not None:
                    simulations[i] = simulation
        return simulations

    """def get_modelised_value_at_time_t(self, t):
        value_modelisation = []
        for sensor in self.sensors:

            reception = [item for item in sensors.receptions[i] if item[0] == t]
            if not reception:
                reception = None
            else:
                reception = reception[0]
                modeled_value = sensor.get_modelised_value()
                if modeled_value is not None:
                    value_modelisation.append(modeled_value)

        if len(value_modelisation) >= 1:
            value_modelisation = sorted(value_modelisation, key=lambda tup: tup[1])
            return value_modelisation[0][0]
        return None"""

    def get_values_in_intervals_from_sensors_knowing_sigma(self, t_prim, t, id):
        values = []
        for reception in self.receptions[id]:
            if reception[0] >= t_prim and  reception[0] <= t:
                values.append([self.sensors[id].std, reception[1]])
        return values

    def get_values_in_intervals_from_sensors_without_knowing_sigma(self, t_prim, t, id):
        values = []
        for reception in self.receptions[id]:
            if reception[0] >= t_prim and  reception[0] <= t:
                values.append(reception[1])
        return values
    def get_modelised_value_at_time_t(self, t, knowing_sigma=True):
        if knowing_sigma:
            return self.get_modelised_value_at_time_t_knowing_sigma(t)
        else:
            return self.get_modelised_value_at_time_t_without_knowing_sigma(t)

    def get_modelised_value_at_time_t_knowing_sigma(self, t):
        modeled_value = 0
        for t_prim in range(t-1, 0, -1):
            values = []
            for id in self.sensors:
                new_values = self.get_values_in_intervals_from_sensors_knowing_sigma( t_prim, t, id)
                values = values + new_values
            if len(values) > 0:
                sig = 0
                modeled_value = 0
                for val in values:
                    sig += pow(val[0], 2)
                    modeled_value += val[1]
                sig = sqrt(sig / pow(len(values), 2))
                modeled_value /= len(values)
                if 2 * conf.quantille_gauss *sig < conf.delta_theta:
                    return modeled_value
        return modeled_value

    def get_modelised_value_at_time_t_without_knowing_sigma(self, t):
        modeled_value = 0
        for t_prim in range(t-1, 0, -1):
            values = []
            for id in self.sensors:
                new_values = self.get_values_in_intervals_from_sensors_without_knowing_sigma(t_prim, t, id)
                values = values + new_values
            if len(values) > 1:
                sig = statistics.stdev(values)
                modeled_value = statistics.mean(values)
                t_quantille = stats.t.ppf(conf.t_test_percentage, len(values) - 1)
                if 2 * t_quantille *sig / sqrt(len(values)) < conf.delta_theta:
                    return modeled_value
        return modeled_value


    def write_in_a_json_file_the_sensor_responses(self):
        if os.path.isfile(conf.sensor_with_reception_file_name):
            os.remove(conf.sensor_with_reception_file_name)
            #print("RECEPTION FILE REMOVED !")
        receptions_file = []
        for i in self.sensors:

            receptions_file.append({'receptions': self.receptions[i],
                                     'std': self.sensors[i].std, 'id': i})
        with open(conf.sensor_with_reception_file_name, 'w+') as outfile:
            json.dump(receptions_file, outfile, indent=4)
            #print("NEW RECEPTION FILE CREATED")
