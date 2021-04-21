import math
import numpy as np
import statistics
import time

nb_of_iteration = 1000
nb_of_initial_values = 100
limit_number_of_taken_values = 200

h = 5.5
sig = 1
nb_of_Dthet = 100
Dthets = [i * 1 / nb_of_Dthet for i in range(nb_of_Dthet)]  # thet step for ARL function
nb_of_sensors = 20
sigs = [(0.5 + i*2/nb_of_sensors) for i in range(nb_of_sensors)]
#sigs = [2 for i in range(nb_of_sensors)]



def mean_detection_time_one_by_one(Dthet, nb_of_iteration):
    means = []
    std = []
    for sig in sigs:
        a,b = time_before_detection(sig,Dthet, nb_of_iteration)
        means.append(a)
        std.append(b)
    std_result = 0
    for s in std:
        std_result += s**2
    std_result = math.sqrt(std_result) /nb_of_sensors
    return statistics.mean(means), std_result

def mean_detection_time_adapted_one_by_one(Dthet, nb_of_iteration):
    means = []
    stds = []
    for sig in sigs:
        a, b = time_before_detection(sig, Dthet, nb_of_iteration)
        means.append(a)
        stds.append(b)

    q = 0
    for sig in sigs:
        q += math.pow(1/sig, 2)
    mean = 0
    #std = 0
    i = 0
    for sig in sigs:
        #print(1/(q * math.pow(sig,2)) * means[i])
        mean += math.pow(1/(q * math.pow(sig, 2)), 2) * means[i]
        #std += math.sqrt(1/(q * sig)) * stds[i]
        i += 1
    std_result = 0
    mean *= len(sigs)
    i = 0
    for s in stds:
        std_result += s ** 2 * 1/(q * math.pow(sigs[i], 2))
        i += 1

    return mean, std_result


def time_before_detection(sig, Dthet, nb_of_iteration, h=h):
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
        a, b = time_before_detection(sig, Dthet, int(nb_of_iteration))
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


if __name__ == "__main__":
    #a, b = time_before_detection(1, 0, 100)
    #print(a)
    #print(2.567 * b / math.sqrt(nb_of_iteration))
    #plot_ARL()
    for sig in sigs:
        a, b = time_before_detection(sig, 3, 10000, h=20)
        print("########")
        print(sig)
        print(a)

    #Dthet = 0.5
    #nb_of_iteration = 1000
    #a, b = mean_detection_time_one_by_one(Dthet, nb_of_iteration)
    #print(a)
    #print(2.567 * b / math.sqrt(nb_of_iteration))

    #a, b = mean_detection_time_adapted_one_by_one(Dthet, nb_of_iteration)
    #print(a)
    #print(2.567 * b / math.sqrt(nb_of_iteration))
