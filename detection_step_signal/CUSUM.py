import math
import numpy as np
import statistics

nb_of_iteration = 1000


nb_of_initial_values = 100

h = 27

nb_of_Dthet = 200
Dthets = [i * 2 /nb_of_Dthet for i in range(nb_of_Dthet)]

def add_new_value_and_raise(S, min_S,max_S, h,X_i):
    new_S = S[-1] + X_i
    S.append(new_S)
    if new_S>max_S:
        max_S = new_S
    if new_S<min_S:
        min_S = new_S
    if max_S - min_S>h:
        boolean = True
    else:
        boolean = False
    return S, min_S, max_S, boolean

def time_before_detection_step_signal(sig, Dthet, nb_of_iteration):
    nb_of_values = []
    for p in range(nb_of_iteration):
        S = [np.random.normal(0, sig)]
        min_S = S[0]
        max_S = S[0]
        for i in range (1, nb_of_initial_values):
            X_i = np.random.normal(0, sig)
            S, min_S, max_S, detected = add_new_value_and_raise(S, min_S, max_S, h, X_i)
        i = 0
        detected = False
        while detected is False:
            X_i = np.random.normal(Dthet, sig)
            i += 1
            S, min_S, max_S, detected = add_new_value_and_raise(S, min_S,max_S, h,X_i)
        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)

def plot_ARL():
    std = []
    mean = []
    sig = 1
    nb_of_iteration = 80000
    Dthet = 0
    pas = 0.01
    Dthets = []
    while Dthet < 0.45:
        Dthets.append(Dthet)
        a, b = time_before_detection_step_signal(sig, Dthet, int(nb_of_iteration))
        mean.append(a)
        std.append(2.567 * b / math.sqrt(nb_of_iteration))
        # print("ok")
        Dthet += pas
        pas *= 1.2
        nb_of_iteration *= 0.9
        stri = '(' + str(Dthets[-1]) + ',' + str(mean[-1]) + ') +- (0,' + str(std[-1]) + ')'
        print(stri)
    stri = ''
    for i in range(len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ') +- (0,' + str(std[i]) + ')'
    print(stri)


def time_before_detection_linear_signal(sig, slope, nb_of_iteration):
    nb_of_values = []
    for p in range(nb_of_iteration):
        S = [np.random.normal(0, sig)]
        min_S = S[0]
        max_S = S[0]
        for i in range (1, nb_of_initial_values):
            X_i = np.random.normal(0, sig)
            S, min_S, max_S, detected = add_new_value_and_raise(S, min_S, max_S, h, X_i)
        i = 0
        detected = False
        while detected is False:
            i += 1
            X_i = np.random.normal(slope *i, sig)
            S, min_S, max_S, detected = add_new_value_and_raise(S, min_S, max_S, h, X_i)
        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)


def plot_LGAARL():
    std = []
    mean = []
    nb_of_iteration = 80000
    Dthet = 0.0
    pas = 0.0005
    Dthets = []
    while Dthet < 1:
        Dthets.append(Dthet)
        a, b = time_before_detection_linear_signal(1, Dthet, int(nb_of_iteration))
        mean.append(a)
        std.append(2.567 * b / math.sqrt(nb_of_iteration))
        # print("ok")
        Dthet += pas
        pas *= 1.1
        nb_of_iteration *= 0.9
        stri = '(' + str(Dthets[-1]) + ',' + str(mean[-1]) + ') +- (0,' + str(std[-1]) + ')'
        print(stri)
    stri = ''
    for i in range(len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ') +- (0,' + str(std[i]) + ')'
    print(stri)



if __name__ == "__main__":
    #a, b = time_before_detection(1, 0, 100000)
    #print(a)
    #print(2.567 * b / math.sqrt(nb_of_iteration))
    plot_ARL()
    #plot_LGAARL()
