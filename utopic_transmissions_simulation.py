import conf
import json
import sensor_class
import statistics
import math
import numpy as np
import matplotlib.pyplot as plt
import distance_functions


def take_the_evaluation_parameter(elt):
    return elt['evaluation']


def sensor_simulation():
    with open(conf.sensor_file_name) as json_file:
        sensors_caracteristics = json.load(json_file)
    sensors_list = []
    simulations = {i: [] for i in range(conf.nb_simulation_per_experiment)}
    for caracteristic in sensors_caracteristics:
        new_sensor = sensor_class.sensor(caracteristic['mean'], caracteristic['std'], caracteristic['prct_reception'], caracteristic['id'])
        simulation, simulations = new_sensor.multi_simulation(conf.nb_simulation_per_experiment, simulations)
        sensors_list.append({'sensor': new_sensor, 'simulation': simulation})
    sims_values = simulations.values()
    #T = statistics.mean(simulations)
    # std = statistics.pstdev(simulations)
    # prop = 1.96 * std / math.sqrt(len(simulations))
    # inter1 = (T - prop, T + prop)
    for sensor in sensors_list:
        if conf.sensor_evaluation == 'Dynamic_time_warping':
            evaluation, cost_matrix, acc_cost_matrix, path = distance_functions.Dynamic_time_warping()
        """elif conf.sensor_evaluation == 'inter_inclusions_of_confidence_intervals':
            evaluation = distance_functions.inter_inclusions_of_confidence_intervals(inter1, sensor['simulation'])"""
        sensor['evaluation'] = evaluation
    sensors_list = sorted(sensors_list, key=take_the_evaluation_parameter, reverse=True)
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
                                 + energie_consumption_subset_constant * conf.energy_consumed_per_emission *  (i + 1) * conf.nb_simulation_per_experiment,

                                  'ids': sensors_ids})
    subset_evaluation = sorted(subset_evaluation, key=take_the_evaluation_parameter)
    return subset_evaluation[0]





def pareto_representation_nb_sensors_required(nb_foot_step,min,max):
    sensor_list = sensor_simulation()
    for sensor in sensor_list:
        print(sensor['evaluation'])
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
    pareto_representation_nb_sensors_required(1000, 100000, 10000000)
    """sensor_list = sensor_simulation()
    print(find_subset_from_sensors_evaluation(100000, 0.01, sensor_list))"""