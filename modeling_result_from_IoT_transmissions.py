import numpy as np
import scipy.stats
import conf



def student_test(alpha, gl):
    return scipy.stats.t.ppf(1-(alpha/2), gl)



"""def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h"""

def student_interval(simulation):
    n = len(simulation + 1) # checking for the simulation plus
    t = student_test(conf.t_alpha, n - 1)
    # TODO : find an interval or another solution for outlier detection
    return ()


def temperature_change_detection(sensor_list, T_fct):
    t = 0
    for sensor in sensor_list:
        sensor.pop('evaluation', None)
        mean, mini, maxi = student_interval(sensor['simulation'])
        sensor['conf_interval'] = (mini, maxi)
    while t < 10000:
        for sensor in sensor_list:
            sensor_object = sensor['sensor']
            if t - sensor_object.emssion_sending_beggining % sensor_object.emission_periode:
                res = sensor_object.one_simulation
                if res is not None:

                    if sensor['conf_interval'][0] < res < sensor['conf_interval'][1]:
                        sensor['simulation'].append(res)
                        mean, mini, maxi = student_interval(sensor['simulation'])
                        sensor['conf_interval'] = (mini, maxi)
                    else:
                        print("ERROR FOUND AT TIME : " + t)
                        return ()
        t += 1