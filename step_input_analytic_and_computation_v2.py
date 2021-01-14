import sensor_caracteristic_generation
import conf

import math
import random
import json
import numpy as np
import statistics
# input
D_T = 100
D_thet = 5

# sensors
sigma = 1
sigmin = 0.5
sigmax = 1.5

T = 10

# precision

k = 2.576
d_thet = 1

# iteration for simulation

nb_simulation = 200

m = math.ceil(math.pow(2 * k * sigma / (d_thet), 2))
m_min = math.ceil(math.pow(2 * k * sigmin / (d_thet), 2))
cst = D_T * D_thet * math.sqrt(2 / math.pi) /(4*k)

# samples legnth and others
number_of_samples = 1000
number_of_time_for_a_sample = 200

"""basic functions"""


# time function
def f(t):
    if t < D_T / 2:
        return D_thet
    else:
        return 0


# function for defining the minimum value necessary for getting the output


def A(nb_sensors):
    res = (cst + (1 / nb_sensors) * T * (D_thet * m - math.sqrt(m) * sigma * math.sqrt(2 / math.pi)))
    return res












def modelise_out_for_one_t_v2(receptions, t):
    for t_prim in range(t - m_min, 0, -1):
        sigma = 0
        for t_sec in range(t_prim, t + 1):
            sigma += math.pow(receptions[t_sec][1], 2)
        sigma = math.sqrt(sigma / math.pow(t - t_prim + 1, 2))

        if (2 * k * sigma < d_thet):
            modeled_value = 0
            for t_sec in range(t_prim, t + 1):
                modeled_value += receptions[t_sec][0]
            return round(modeled_value / (t + 1 - t_prim), 3)
    return 0

def modelise_output_from_receptions_v2(receptions):
    output = [0] * math.ceil(len(receptions))
    for t in range(m_min, len(output)):
        output[t] = modelise_out_for_one_t_v2(receptions, t)
    return output

def get_mean_mean_evaluation_for_a_sample_v2(sample_length):
    with open(conf.sensor_file_name) as json_file:
        sensors_json = json.load(json_file)

    areas = [0] * number_of_samples
    for i in range(number_of_samples):
        sensors_json = random.sample(sensors_json, sample_length)

    mean = statistics.mean(areas)
    print('(' + str(sample_length) + ', '
          + str(round( min(areas), 3)) + ')')

    """) +- ('
          + str(round(mean - min(areas), 3)) + ', '
          + str(round(max(areas) - mean, 3)) + ') \n')"""


if __name__ == "__main__":
    