import math
import numpy as np
import statistics
k_alpha = 3.090 #representing quantille of gaussian for 99%

nb_of_iteration = 1000

nb_of_values_of_r = 500

h = 14.5

nb_of_Dthet = 200
Dthets = [i * 2 /nb_of_Dthet for i in range(nb_of_Dthet)]

def add_new_value_and_raise(Dthet,S, min_S,max_S, h,X_i):
    new_S = S[-1] + X_i - Dthet
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


def time_before_detection(sig, Dthet):
    nb_of_values = []
    for p in range(nb_of_iteration):
        i = 1
        S = [np.random.normal(0, sig)]
        min_S = S[0]
        max_S = S[0]
        detected = False
        while detected is False:
            X_i = np.random.normal(0, sig)
            i += 1
            S, min_S, max_S, detected = add_new_value_and_raise(Dthet,S, min_S,max_S, h,X_i)
        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)

def plot_ARL():
    time_of_detection = []
    for Dthet in Dthets:
        time_of_detection.append(time_before_detection(1, Dthet))
    stri = ''
    for i in range (nb_of_Dthet):
        stri += '(' + str(Dthets[i]) + ',' + str(time_of_detection[i]) + ') '
    print(stri)

if __name__ == "__main__":
    #print(time_before_detection(1, 0))
    plot_ARL()
