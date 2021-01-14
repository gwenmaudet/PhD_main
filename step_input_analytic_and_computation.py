import sensor_caracteristic_generation
import conf

import math
import random
import json
import numpy as np
import statistics
# input
D_T = 1200
D_thet = 5

# sensors
sigma = 1

nb_sensors = 50

T = 10

# precision

k = 2.576
d_thet = 1


m = math.ceil(math.pow(2 * k * sigma / d_thet, 2))
cst = D_T * sigma * math.sqrt(2 / math.pi) / (2 * math.sqrt(m))
# iteration for simulation

nb_simulation = 200
sigmin = 0.5
sigmax = 1.5
m_min = math.ceil(math.pow(2 * k * sigmin / ( d_thet ), 2))



# samples legnth and others
number_of_samples = 100
number_of_time_for_a_sample = 50

"""basic functions"""

def m_fct(sigma):
    return math.ceil(math.pow(2 * k * sigma / d_thet, 2))
# time function
def f(t):
    if t < D_T / 2:
        return D_thet
    else:
        return 0


# function for defining the minimum value necessary for getting the output


def A_nb_sensors(nb_sensors):
    res = (cst + (1 / nb_sensors) * T * (D_thet * m / 2 - math.sqrt(m) * sigma * math.sqrt(2 / math.pi)))
    return res

def A_sigma(sigma):
    m = math.ceil(math.pow(2 * k * sigma / d_thet, 2))
    cst = D_T * sigma * math.sqrt(2 / math.pi) / (2 * math.sqrt(m))
    res = (cst + (1 / nb_sensors) * T * (D_thet * m / 2 - math.sqrt(m) * sigma * math.sqrt(2 / math.pi)))
    return round(res, 3)

def plot_graphs_nb_sensors():
    to_print = '\\addplot [mark=none] coordinates {'
    for i in range(1, 50):
        to_print += '(' + str(i) + ', ' + str(round(A_nb_sensors(i), 1)) + ') '
    to_print += '};'
    print(to_print)

def plot_graphs_sigma():
    to_print = '\\addplot [mark=none] coordinates {'
    i = sigmin
    while i < sigmax:
        to_print += '(' + str(round(i, 5)) + ', ' + str(round(A_sigma(i), 1)) + ') '
        i += 0.01
    to_print += '};'
    print(to_print)

def get_receptions(sensors):
    n = len(sensors)
    i = 0
    tmax = D_T * n / T
    receptions = [0] * math.ceil(tmax)
    input = [0] * math.ceil(tmax)
    for sensor in sensors: #segmentation of the time where reception[t] t in N , represent the time t * T / n
        sensor['first_emission'] = i
        i += 1
        t = sensor['first_emission']
        while t < tmax:
            receptions[t] = [np.random.normal(f(t * T / n), sensor['std']),
                             sensor['std']]
            input[t] = f(t * T / n)
            t += n
    return receptions, input


def modelise_out_for_one_t(receptions, t):
    for t_prim in range(t - m_min, 0, -1):
        sigma = 0
        for t_sec in range(t_prim, t + 1):
            sigma += math.pow(receptions[t_sec][1], 2)
        sigma = math.sqrt(sigma / math.pow(t - t_prim + 1, 2))

        if (2 * k * sigma < d_thet):
            modeled_value = 0
            for t_sec in range(t_prim, t + 1):
                modeled_value += receptions[t_sec][0]
            return modeled_value / (t + 1 - t_prim)
    return 0

def modelise_output_from_receptions(receptions):
    output = [0] * math.ceil(len(receptions))
    for t in range(m_min, len(output)):
        output[t] = modelise_out_for_one_t(receptions, t)
    return output


def compute_area(input, output, n):
    area = 0
    for i in range(len(output)//2, len(output) - 1):
        if (output[i] - input[i])*(output[i+1] - input[i+1]) > 0:
            area += abs((output[i+1] - output[i]) * T/(2*n)) + min(abs(output[i]- input[i]), abs(output[i+1]- input[i+1])) * T / n
        else:
            area += abs(output[i] - output[i+1]) * T/ (2 * n)
        #area += abs(output[i] - input[i]) * T / n

    return area


def get_mean_mean_evaluation_for_a_sample(sample_length):
    with open(conf.sensor_file_name) as json_file:
        sensors_json_tot = json.load(json_file)
    areas = [0] * number_of_samples
    for i in range(number_of_samples):
        sensors_json = random.sample(sensors_json_tot, sample_length)
        areas_for_one_sample = []
        for j in range(number_of_time_for_a_sample):
            receptions, input = get_receptions(sensors_json)
            output = modelise_output_from_receptions(receptions)
            areas_for_one_sample.append(compute_area(input, output, sample_length))
        areas[i] = statistics.mean(areas_for_one_sample)
    """sensors_json = [sensors_json_tot[0]]
    areas_for_one_sample = []
    print("ploc" + str(m_fct(sensors_json[0]['std'])))
    for j in range(number_of_time_for_a_sample):
        receptions, input = get_receptions(sensors_json)
        output = modelise_output_from_receptions(receptions)
        areas_for_one_sample.append(compute_area(input, output, sample_length))
    areas[0] = statistics.mean(areas_for_one_sample)

    sensors_json = [sensors_json_tot[49]]
    print("ploc" + str(m_fct(sensors_json[0]['std'])))
    areas_for_one_sample = []
    for j in range(number_of_time_for_a_sample):
        receptions, input = get_receptions(sensors_json)
        output = modelise_output_from_receptions(receptions)
        areas_for_one_sample.append(compute_area(input, output, sample_length))
    areas[1] = statistics.mean(areas_for_one_sample)
    areas = areas[:2]
    print(areas)"""
    mean = statistics.mean(areas)
    print('(' + str(sample_length) + ', '
          + str(round(min(areas), 3)) + ')')
    print('(' + str(sample_length) + ', '
          + str(round(mean, 3)) + ')')
    print('(' + str(sample_length) + ', '
          + str(round(max(areas), 3)) + ')')
    #print('(' + str(sample_length) + ', ' + str(round(mean, 3)) + ') +- (' + str(round(mean -min(areas),3)) + ', ' + str(round(max(areas)- mean,3)) + ') \n')


def get_infor_for_multiple_sample_length():
    for i in range(10, 20):
        print(i)
        get_mean_mean_evaluation_for_a_sample(i)

if __name__ == "__main__":
    # get_mean_mean_evaluation_for_a_sample(1)
    #print(D_T *math.pow(d_thet, 2) / (8 * T * math.pow(k, 2)))
    # print(1.5 * 8 * T * math.pow(k,2)/(d_thet))
    # plot_graphs_sigma()
    get_infor_for_multiple_sample_length()



