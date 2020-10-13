import conf
import json
import sensor_class
import statistics
import math
import numpy as np
import matplotlib.pyplot as plt

def evaluation(T, simulation):
    T_prim = statistics.mean(simulation)
    std = statistics.pstdev(simulation)
    return (abs(T - T_prim) * conf.mean_sensor_constant + std * conf.std_sensor_constant)


def take_the_evaluation_parameter(elt):
    return elt['evaluation']


def sensor_evaluation():
    with open(conf.sensor_file_name) as json_file:
        sensors_caracteristics = json.load(json_file)
    sensors_list = []
    simulations = np.array([])
    for caracteristic in sensors_caracteristics:
        new_sensor = sensor_class.sensor(caracteristic['mean'], caracteristic['std'], caracteristic['id'])
        simulation = new_sensor.multi_simulation(conf.nb_simulation_per_sensor)
        simulations = np.concatenate((simulation, simulations), axis=None)
        sensors_list.append({'sensor': new_sensor, 'simulation': simulation})
    T = statistics.mean(simulations)
    for sensor in sensors_list:
        T_prim = statistics.mean(sensor['simulation'])
        std = statistics.pstdev(sensor['simulation'])
        evaluation = abs(T - T_prim) * conf.mean_sensor_constant + std * conf.std_sensor_constant
        sensor['evaluation'] = evaluation
    sensors_list = sorted(sensors_list, key=take_the_evaluation_parameter)
    return sensors_list


def find_subset_from_sensors_evaluation(confidence_interval_subset_constant, energie_consumption_subset_constant, sensors_list):
    subset_evaluation = []
    for i in range(conf.max_subset_nb):
        simulations = []
        sensors_ids = []
        for j in range(i + 1):
            simulations = np.concatenate((simulations, sensors_list[j]['simulation']), axis=None)
            sensors_ids.append(sensors_list[j]['sensor'].id)
        subset_evaluation.append({'evaluation': confidence_interval_subset_constant * (statistics.stdev(simulations) / math.sqrt(len(simulations)))
                                 + energie_consumption_subset_constant * conf.energy_consumed_per_emission * len(simulations),

                                  'ids': sensors_ids})
    subset_evaluation = sorted(subset_evaluation, key=take_the_evaluation_parameter)
    return subset_evaluation[0]





def pareto_representation_nb_sensors_required(nb_foot_step,min,max):
    sensor_list = sensor_evaluation()
    x_values = [(min + (max - min) * i / nb_foot_step) for i in range(nb_foot_step)]
    y = []
    print(x_values)
    for x in x_values:
        subset = find_subset_from_sensors_evaluation(x, 1, sensor_list)
        y.append(len(subset['ids']))
    plt.plot(x_values, y)
    plt.xlabel("ratio (confidence interval constant) / (energy consummed constant)")
    plt.ylabel("nb of active sensors")
    plt.show()
if __name__ == "__main__":
    pareto_representation_nb_sensors_required(100, 10000000, 1000000000000000)