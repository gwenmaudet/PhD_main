import conf
import sensor_class
import sensor_caracteristic_generation


import json
import random
import time
import math
import statistics
from scipy import stats
import time


def create_input_from_all_sensors_for_constant_input_with_json_file_sensors(nb_sensors):
    # sensor_caracteristic_generation.create_sensors_caracteristic_storage(conf.nb_sensors)
    with open(conf.sensor_file_name) as json_file:
        sensors_json = json.load(json_file)
    sensors_json = random.sample(sensors_json, nb_sensors)
    sensors = sensor_class.sensors()
    sensor_list = []
    for sensor_json in sensors_json:
        new_sensor = sensor_class.sensor(std=sensor_json['std'], prct_reception=sensor_json['prct_reception'],
                                         id=sensor_json['id'], emission_periode=sensor_json['emssion_period'],first_emssion=sensor_json['first_emssion'])
        sensor_list.append(new_sensor)
    sensors = sensor_class.sensors(sensor_list)
    """beggining of the simulation"""
    for t in range(0, conf.time_of_exp):
        temp = conf.theoritical_temperature(t)
        simulations = sensors.get_response_from_gate_at_instant_t(t, temp)
        for i in simulations:

            sensors.receptions[i].append(simulations[i])
    sensors.write_in_a_json_file_the_sensor_responses()

def return_inputs_from_sensors(nb_sensors):
    with open(conf.sensor_file_name) as json_file:
        sensors_json = json.load(json_file)
    sensors_json = random.sample(sensors_json, nb_sensors)
    receptions = []
    for sensor_json in sensors_json:
        new_sensor = sensor_class.sensor(std=sensor_json['std'], prct_reception=sensor_json['prct_reception'],
                                         id=sensor_json['id'], emission_periode=sensor_json['emssion_period'],
                                         first_emssion=sensor_json['first_emssion'])
        t = sensor_json['first_emssion']
        while t < conf.time_of_exp:
            recep = new_sensor.one_simulation(t, conf.theoritical_temperature(t))
            if recep is not None:
                receptions.append(recep)
            t += sensor_json['emssion_period']

    return sorted(receptions, key=lambda tup: tup[0])


def compute_metric(input, model):
        area = 0
        memory = 0
        for t in range (0, 10):
            if model[t] is not None:
                memory = model[t]
        for t in range (10, conf.time_of_exp):
            if model[t] is not None:
                memory = model[t]
            area += math.fabs(model[t] - input[t])
        return area

def get_modelised_value_at_time_t(receptions, t):
    modeled_value = 0
    values = []
    ind = len(receptions) - 1
    get_to_the_point = False
    while get_to_the_point is False and ind >= 0:
        if receptions[ind][0] == t:
            get_to_the_point = True
        else:
            ind -= 1
    get_to_the_point = False
    while get_to_the_point is False and ind >= 0:
        if receptions[ind][0] == t-1:
            get_to_the_point = True
        else:
            values.append(receptions[ind][1])
            ind -= 1

    for t_prim in range(t-1, 0, -1):
        get_to_the_point = False
        while get_to_the_point is False and ind >= 0:
            if receptions[ind][0] == t_prim:
                get_to_the_point = True
            else:
                values.append(receptions[ind][1])
                ind -= 1
        if len(values) > 1:
            sig = statistics.stdev(values)
            modeled_value = statistics.mean(values)
            t_quantille = stats.t.ppf(conf.t_test_percentage, len(values) - 1)
            if 2 * t_quantille * sig / math.sqrt(len(values)) < conf.delta_theta:
                return modeled_value
    return modeled_value

def simulation_for_sensor_sample(nb_sensors):
    receptions = return_inputs_from_sensors(nb_sensors)
    input = [None] * conf.time_of_exp
    model = [None] * conf.time_of_exp
    for t in range (0, len(input)):
        input[t] = conf.theoritical_temperature(t)
        value_modelised = get_modelised_value_at_time_t(receptions, t)
        model[t] = value_modelised
    metric = compute_metric(input, model)
    return metric
    """to_print = "\\addplot coordinates{"
    for t in range(0, len(input)):
        to_print += ' (' + str(t) + ', ' + str(input[t]) + ') '
    to_print += ' };'
    print(to_print)
    to_print = "\\addplot coordinates{"
    #to_print = "\\addplot+[error bars/.cd,y dir=both,y explicit]coordinates{"
    for t in range(0, conf.time_of_exp):
        if model[t] is not None:
            to_print += "(" + str(t) + ',' + str(round(model[t], 3)) + ')'
            #to_print += "(" + str(t) + ',' + str(round(model[t], 3)) + ')+-(0,' + str(round(conf.delta_theta, 3)) + ') '
    to_print += ' };'

    print(to_print)"""


def sample_for_different_nb_of_sensors():
    sample_results = {}
    for sam in conf.sensor_sample:
        sample_results[sam] = []

    sensor_caracteristic_generation.create_sensors_caracteristic_storage(conf.nb_sensors)
    for sam in conf.sensor_sample:
        for iter in range (conf.nb_of_iteration):
            metric = simulation_for_sensor_sample(sam)
            sample_results[sam].append(metric)
        print("one sample is done")
    to_print = "\\begin{tikzpicture}\n\\begin{axis}[boxplot/draw direction=y,width=1.0\\textwidth" \
               "legend entries = {"
    for sam in conf.sensor_sample:
        to_print += str(sam) + ','
    to_print += "},\n legend to name={legend},\n name=border]"
    for sam in sample_results:
        to_print += "\\addplot+[boxplot]\n table[row sep=\\\\,y index=0] {"
        for info in sample_results[sam]:
            to_print += str(info) + ' \\\\'
        to_print += '\n }; \\addlegendentry{' + str(sam) + ' sensors}\n'
    to_print += "\\end{axis}\n \\node[below right] at (border.north east) {\\ref{legend}}; \n\\end{tikzpicture}"
    print(to_print)



if __name__ == "__main__":
    # sensor_caracteristic_generation.create_sensors_caracteristic_storage(conf.nb_sensors)
    #create_sensors_and_input_from_all_sensors_for_constant_input()
    sample_for_different_nb_of_sensors()