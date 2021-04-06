import math
import numpy as np
import statistics
import time


nb_of_iteration = 1000

h = 4.5

nb_of_Dthet = 100
Dthets = [i * 1 / nb_of_Dthet for i in range(nb_of_Dthet)] #thet step for ARL function

def time_before_detection(sig,Dthet):
    nb_of_values = []
    for p in range(nb_of_iteration):
        i = 1
        x = np.random.normal(0, sig) - Dthet
        X = [x]
        detected = False
        if math.pow(x, 2) > 2 *h * math.pow(sig, 2):
           detected = True

        while detected is False:
            x = np.random.normal(0, sig) - Dthet
            X.append(x)
            n = len(X)
            for j in range(n):
                g = math.pow(sum(X[j:n]), 2)/(n-j)
                if g > 2 * h * math.pow(sig, 2):
                    detected = True
            i += 1
        nb_of_values.append(i)


        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)


def plot_ARL():
    time_of_detection = []
    for Dthet in Dthets:
        time_of_detection.append(time_before_detection(1, Dthet))
        print("ok")
    stri = ''
    for i in range (nb_of_Dthet):
        stri += '(' + str(Dthets[i]) + ',' + str(time_of_detection[i]) + ') '
    print(stri)


if __name__ == "__main__":
    #print(time_before_detection(1, 0))
    plot_ARL()