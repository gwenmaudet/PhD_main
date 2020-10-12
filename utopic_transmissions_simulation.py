import conf
import json
import sensor_class
import statistics
import math
import numpy as np

def sensor_evaluation(T, simulation):
    T_prim = statistics.mean(simulation)
    std = statistics.pstdev(simulation)
    return (abs(T - T_prim) * conf.mean_sensor_constant + std * conf.std_sensor_constant)


def take_the_evaluation_parameter(elt):
    return elt['evaluation']

def main():
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
        evalutation = sensor_evaluation(T, sensor['simulation'])
        sensor['evaluation'] = evalutation
    sensors_list = sorted(sensors_list, key=take_the_evaluation_parameter)
    # print(sensors_list)
    subset_evaluation = []
    for i in range(conf.max_subset_nb):
        simulations = []
        sensors_ids = []
        for j in range(i+1):
            simulations = np.concatenate((simulations, sensors_list[j]['simulation']), axis=None)
            sensors_ids.append(sensors_list[j]['sensor'].id)
        subset_evaluation.append({'evaluation': conf.confidence_interval_subset_constant * (statistics.stdev(simulations) / math.sqrt(len(simulations)))
                                 + conf.energy_consummed_per_emission * len(simulations),

                                  'ids': sensors_ids})
        print("one is done")
    subset_evaluation = sorted(subset_evaluation, key=take_the_evaluation_parameter)
    print('\n\n\n')
    print(subset_evaluation)
    print('\n\n\n')
    print(subset_evaluation[0])
if __name__ == "__main__":
    main()