import math
import numpy as np
import statistics
import time
import random
from constraint import *

import cplex



nb_of_iteration = 1000
nb_of_initial_values = 100
limit_number_of_taken_values = 200

h = 5.5
sig = 1
nb_of_Dthet = 100
Dthets = [i * 1 / nb_of_Dthet for i in range(nb_of_Dthet)]  # thet step for ARL function
nb_of_sensors = 10
sigs = [(0.5 + 1 * i/nb_of_sensors) for i in range(nb_of_sensors)]
# sigs = [2 for i in range(nb_of_sensors)]



def mean_detection_time_simultaneously(Dthet, nb_of_iteration):
    nb_of_values = []
    sig_stamp = list(sigs)
    for p in range(nb_of_iteration):
        random.shuffle(sig_stamp)
        g_k = []
        for i in range(nb_of_initial_values):
            sig = sig_stamp[i % nb_of_sensors]
            x = np.random.normal(0, sig)
            #x = 1
            n = len(g_k)
            for j in range(n):
                g_k[j] = math.pow(math.sqrt(g_k[j] * (n-j)) + x / sig, 2) / (n - j + 1)
            g_k.append(math.pow(x/ sig, 2) )
            #print(g_k)
            #time.sleep(1)
        i = 0
        detected = False

        while detected is False:
            sig = sig_stamp[i % nb_of_sensors]
            x = np.random.normal(Dthet, sig)
            n = len(g_k)
            if n >= limit_number_of_taken_values:
                g_k = g_k[1:]
                n -= 1
            for j in range(n):
                g_k[j] = math.pow(math.sqrt(g_k[j] * (n - j)) + x / sig, 2) / (n - j + 1)
            g_k.append(math.pow(x / sig, 2))
            i += 1
            for j in range(n + 1):
                if (abs(g_k[j])> 2 * h) :
                    detected = True
        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)



def mean_detection_time_one_by_one_and_adapted_one_by_one(Dthet, nb_of_iteration):
    means = []
    stds = []
    for sig in sigs:
        a, b = time_before_detection_step_signal(sig, Dthet, nb_of_iteration)
        means.append(a)
        stds.append(b)
    q = 0
    for sig in sigs:
        q += math.pow(1/sig, 2)
    mean_adapted_one_by_one = 0
    std_adapted_one_by_one = 0
    i = 0
    for sig in sigs:
        mean_adapted_one_by_one += math.pow(1/(q * math.pow(sig, 2)), 2) * means[i]
        std_adapted_one_by_one += stds[i] ** 2 * 1 / (q * math.pow(sig, 2))
        i += 1
    mean_adapted_one_by_one *= len(sigs)
    std_adapted_one_by_one = math.sqrt(std_adapted_one_by_one)

    std_one_by_one = 0
    mean_one_by_one = 0
    i = 0
    for sig in sigs:
        std_one_by_one += stds[i] ** 2
        mean_one_by_one += means[i]/ math.pow(len(sigs), 2)
        i += 1
    std_one_by_one = math.sqrt(std_one_by_one / nb_of_sensors)
    mean_one_by_one *= len(sigs)
    return mean_one_by_one, std_one_by_one, mean_adapted_one_by_one, std_adapted_one_by_one, means


def time_before_detection_step_signal(sig, Dthet, nb_of_iteration, h=h):
    nb_of_values = []
    for p in range(nb_of_iteration):
        X_bar = []
        for i in range(nb_of_initial_values):
            x = np.random.normal(0, sig)
            n = len(X_bar)
            for j in range(n):
                X_bar[j] = math.pow(math.sqrt(X_bar[j] * (n - j)) + x, 2) / (n - j + 1)
            X_bar.append(math.pow(x, 2))
        i = 0
        detected = False

        while detected is False:
            x = np.random.normal(Dthet, sig)
            n = len(X_bar)
            if n >= limit_number_of_taken_values:
                X_bar = X_bar[1:]
                n -= 1
            for j in range(n):
                X_bar[j] = math.pow(math.sqrt(X_bar[j] * (n - j)) + x, 2) / (n - j + 1)
            X_bar.append(math.pow(x, 2))
            for j in range(n + 1):
                if (X_bar[j]) > 2 * h * math.pow(sig, 2):
                    detected = True
            i += 1
        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)


def plot_ARL():
    std = []
    mean = []
    nb_of_iteration = 100000
    Dthet = 00
    pas = 0.01
    Dthets = []
    while Dthet < 1:
        Dthets.append(Dthet)
        a, b = time_before_detection_step_signal(sig, Dthet, int(nb_of_iteration))
        mean.append(a)
        std.append(2.567 * b / math.sqrt(nb_of_iteration))
        # print("ok")
        Dthet += pas
        pas *= 1.2
        nb_of_iteration *= 0.9
        stri = ''
        stri += '(' + str(Dthets[-1]) + ',' + str(mean[-1]) + ') +- (0,' + str(std[-1]) + ')'
        print(stri)
    stri = ''
    for i in range(len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ') +- (0,' + str(std[i]) + ')'
    print(stri)


def time_before_detection_linear_signal(sig, slop, nb_of_iteration, h=h):
    nb_of_values = []
    for p in range(nb_of_iteration):
        X_bar = []
        for i in range(nb_of_initial_values):
            x = np.random.normal(0, sig)
            n = len(X_bar)
            for j in range(n):
                X_bar[j] = math.pow(math.sqrt(X_bar[j] * (n - j)) + x, 2) / (n - j + 1)
            X_bar.append(math.pow(x, 2))
        i = 0
        detected = False

        while detected is False:
            i += 1
            x = np.random.normal(slop * i, sig)
            n = len(X_bar)
            if n >= limit_number_of_taken_values:
                X_bar = X_bar[1:]
                n -= 1
            for j in range(n):
                X_bar[j] = math.pow(math.sqrt(X_bar[j] * (n - j)) + x, 2) / (n - j + 1)
            X_bar.append(math.pow(x, 2))
            for j in range(n + 1):
                if (X_bar[j]) > 2 * h * math.pow(sig, 2):
                    detected = True

        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)


def plot_LGAARL():
    std = []
    mean = []
    nb_of_iteration = 80000
    Dthet = 00
    pas = 0.005
    Dthets = []
    while Dthet < 0.2:
        Dthets.append(Dthet)
        a, b = time_before_detection_linear_signal(sig, Dthet, int(nb_of_iteration))
        mean.append(a)
        std.append(2.567 * b / math.sqrt(nb_of_iteration))
        # print("ok")
        Dthet += pas
        pas *= 1.2
        nb_of_iteration *= 0.9
        stri = ''
        stri += '(' + str(Dthets[-1]) + ',' + str(mean[-1]) + ') +- (0,' + str(std[-1]) + ')'
        print(stri)
    stri = ''
    for i in range(len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ') +- (0,' + str(std[i]) + ')'
    print(stri)

nb_for_D = 1000
D = [i/nb_for_D for i in range(nb_for_D)]


def main1():
    Dthet = 0
    nb_of_iteration = 1000
    a, b = mean_detection_time_simultaneously(Dthet, len(sigs) * nb_of_iteration)
    print("simultaneously")
    print(a)
    print(2.567 * b / math.sqrt(nb_of_iteration))

    a, b, c, d, e = mean_detection_time_one_by_one_and_adapted_one_by_one(Dthet, nb_of_iteration)
    print("one by one")
    print(a)
    print(2.567 * b / math.sqrt(nb_of_iteration))
    print("adapted one by one")
    print(c)
    print(2.567 * d / math.sqrt(nb_of_iteration))
    print(e)
    print(sigs)



def get_sigma_squared_and_periods(sigs2):
    Ts = []
    A = 0
    for sig in sigs2:
        A += 1/sig
    sum = 0
    Tsum = 0
    for sig in sigs2:
        T = 1/(A * sig)
        Ts.append(T)
        sum += sig * math.pow(T, 2)
        Tsum += T
    print(Ts)
    print(Tsum)
    print(sum)

if __name__ == "__main__":
    #nb_of_iteration = 50000
    #a, b = time_before_detection_step_signal(1, 0.95, nb_of_iteration)
    #print(a)
    #print(2.567 * b / math.sqrt(nb_of_iteration))
    #plot_ARL()
    # plot_LGAARL()
    #constraint_programming_to_find_the_good_periods([2.3, 2.5, 3.3])
    #main1()
    #sigs2 = [0.1,0.3,0.4,0.45, 0.8, 1, 1.5, 2, 5, 5.2]
    #sigs2 = [0.2, 0.2, 0.5, 0.5, 1, 1.5, 1.6, 1.8, 3, 3.4]
    #get_sigma_squared_and_periods(sigs2)
    main1()