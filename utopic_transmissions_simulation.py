import conf
import json
import sensor_class
import statistics
import math
import numpy as np
import matplotlib.pyplot as plt

def proportion_of_an_interval_into_another_one(inter1, inter2): #proportion of the inter1 into the inter 2
    inter2_len = (inter2[1] - inter2[0])
    if inter1[1]<inter2[0] or inter1[0]>inter2[1]:
        return 0
    elif inter1[0] > inter2[0] and inter1[1]<inter2[1]:
        return (inter1[1] - inter1[0]) * 100 / inter2_len
    elif inter1[0] < inter2[0] and inter1[1] > inter2[1]:
        return 100
    elif inter1[0] < inter2[0]:
        return (inter1[1] - inter2[0]) / inter2_len
    elif inter1[1] > inter2[1]:
        return (inter2[1] - inter1[0]) / inter2_len
    else:
        print("ERROR")
        return



def sensor_evaluation(inter1, simulation):
    T_prim = statistics.mean(simulation)
    std_prim = statistics.stdev(simulation)
    prop = 1.96 * std_prim / math.sqrt(len(simulation))
    inter2 = (T_prim - prop, T_prim + prop)
    print(inter2)
    return proportion_of_an_interval_into_another_one(inter1, inter2)


def take_the_evaluation_parameter(elt):
    return elt['evaluation']


def sensor_simulation():
    with open(conf.sensor_file_name) as json_file:
        sensors_caracteristics = json.load(json_file)
    sensors_list = []
    simulations = np.array([])
    for caracteristic in sensors_caracteristics:
        new_sensor = sensor_class.sensor(caracteristic['mean'], caracteristic['std'], caracteristic['prct_reception'], caracteristic['id'])
        simulation = new_sensor.multi_simulation(conf.nb_simulation_per_sensor)
        simulations = np.concatenate((simulation, simulations), axis=None)
        sensors_list.append({'sensor': new_sensor, 'simulation': simulation})
    T = statistics.mean(simulations)
    std = statistics.stdev(simulations)
    prop = 1.96 * std / math.sqrt(len(simulations))
    inter1 = (T - prop, T + prop)
    print(inter1)
    for sensor in sensors_list:
        evaluation = sensor_evaluation(inter1, sensor['simulation'])
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
                                 + energie_consumption_subset_constant * conf.energy_consumed_per_emission *  (i + 1) * conf.nb_simulation_per_sensor,

                                  'ids': sensors_ids})
    subset_evaluation = sorted(subset_evaluation, key=take_the_evaluation_parameter)
    return subset_evaluation[0]





def pareto_representation_nb_sensors_required(nb_foot_step,min,max):
    sensor_list = sensor_simulation()
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