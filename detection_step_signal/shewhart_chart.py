import math
import numpy as np
import statistics
import random
import time
h = 3.34

nb_of_iteration = 1000

limit_number_of_taken_values = 200
nb_of_initial_values = 100

nb_of_Dthet = 100
Dthets = [(i * 1 / nb_of_Dthet) for i in range(nb_of_Dthet)] #thet step for ARL function
sig = 1
nb_of_sensors = 20
sigs = [(0.5 + i*2/nb_of_sensors) for i in range(nb_of_sensors)]
#sigs = [2 for i in range(nb_of_sensors)]

def quantify_false_positives(sigs):
    nb_of_hs = 20
    hs = [1 +i*1.5/nb_of_hs for i in range (nb_of_hs)]
    nb_of_iteration = 10000
    mses = []
    for h in hs:
        temp = []
        for sig in sigs:
            a, b = time_before_detection(sig, 0, nb_of_iteration, h)
            temp.append(a)
        print(temp)
        mses.append(statistics.stdev(temp))
    stri = ''
    for i in range(len(hs)):
        stri += '(' + str(hs[i]) + ',' + str(mses[i]) + ')'
    print(stri)




def mean_detection_time_simultaneously(Dthet, nb_of_iteration):
    nb_of_values = []
    for p in range(nb_of_iteration):
        random.shuffle(sigs)
        X_bar = []
        reception_error = []
        for i in range(nb_of_initial_values):
            sig = sigs[i % nb_of_sensors]
            x = np.random.normal(0, sig)
            n = len(X_bar)
            for j in range(n):
                X_bar[j] = X_bar[j] * (n - j) / (n - j + 1) + x / (n - j + 1)
                reception_error[j] = math.sqrt(math.pow(reception_error[j] * (n - j), 2)
                                               + math.pow(sig,2)) \
                                     / (n - j + 1)
            X_bar.append(x)
            reception_error.append(sig)
            #print(reception_error)
            #time.sleep(1)
        i = 0
        detected = False
        while detected is False:
            sig = sigs[i % nb_of_sensors]
            x = np.random.normal(Dthet, sig)
            n = len(X_bar)
            if n >= limit_number_of_taken_values:
                X_bar = X_bar[1:]
                reception_error = reception_error[1:]
                n -= 1
            for j in range(n):
                X_bar[j] = X_bar[j] * (n - j) / (n - j + 1) + x / (n - j + 1)
                #print((reception_error[j] * (n-j))**2)
                reception_error[j] = math.sqrt(((reception_error[j] * (n-j))
                                                * (reception_error[j] * (n-j)))
                                               + math.pow(sig,2))\
                                     / (n - j + 1)
            X_bar.append(x)
            reception_error.append(sig)
            i += 1
            for j in range(n + 1):
                if (abs(X_bar[j])>h * reception_error[j]) :
                    detected = True
                    # print(X_bar)
                    # print(j)
        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)

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
        mean += 1/(q * math.pow(sig, 2)) * means[i]
        #std += math.sqrt(1/(q * sig)) * stds[i]
        i += 1
    std_result = 0
    i = 0
    for s in stds:
        std_result += s ** 2 * 1/(q * math.pow(sigs[i], 2))
        i += 1

    return mean, std_result


def necessary_nb_of_value_GSC(sig,Dthet):
    return math.ceil(math.pow(h * sig / Dthet, 2))



def average_nb_of_necessary_values_before_detection(sig, Dthet):
    nb_of_values = []
    for p in range(nb_of_iteration):
        i = 1
        X_bar = [np.random.normal(0, sig)]
        mean = statistics.mean(X_bar)
        while (mean + (h * sig / math.sqrt(i)) > Dthet):
            X_bar.append(np.random.normal(0, sig))
            mean = statistics.mean(X_bar)
            i += 1
        nb_of_values.append(i)
    return statistics.mean(nb_of_values)



## approximate the necessary threshold
def change_at_100(Dthet):
    N = 120
    prop_of_detected = [0 for i in range(N)]
    i_s = [i for i in range(N)]
    not_detected = 0
    for p in range(nb_of_iteration):
        i = 1
        x = np.random.normal(0, sig)
        X_bar = [x]
        mean = x
        detected = False
        if (mean + (h * sig) < Dthet) or (mean - (h * sig) > Dthet):
            detected = True
        while (i < N) and detected is False:
            x = np.random.normal(0, sig)
            n = len(X_bar)
            for j in range(n):
                X_bar[j] = X_bar[j] * (n - j) / (n - j + 1) + x / (n - j + 1)
            X_bar.append(x)
            i += 1
            for j in range(n + 1):
                if (X_bar[j] + (h * sig / math.sqrt(n + 1 - j)) < Dthet) or (
                        X_bar[j] - (h * sig / math.sqrt(n + 1 - j)) > Dthet):
                    detected = True
        if i != N:
            prop_of_detected[i] += 1
        else:
            not_detected += 1
    print(not_detected)








def time_before_detection(sig,Dthet, nb_of_iteration, h=h):
    nb_of_values = []
    for p in range(nb_of_iteration):
        X_bar = []
        for i in range(nb_of_initial_values):
            x = np.random.normal(0, sig)
            n = len(X_bar)
            for j in range(n):
                X_bar[j] = X_bar[j] * (n - j) / (n - j + 1) + x / (n - j + 1)
            X_bar.append(x)
        i = 0
        detected = False
        while detected is False:
            x = np.random.normal(Dthet, sig)
            n = len(X_bar)
            if n >= limit_number_of_taken_values:
                X_bar = X_bar[1:]
                n -= 1
            for j in range(n):
                X_bar[j] = X_bar[j] * (n-j) / (n-j+1) + x / (n-j+1)
            X_bar.append(x)
            i += 1
            for j in range(n+1):
                if (abs(X_bar[j]) > h * sig / math.sqrt(n + 1 - j)):
                    detected = True
                    #print(X_bar)
                    #print(j)
        nb_of_values.append(i)


        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)
def plot_theoritical_ARL():
    nb_of_Dthet = 100
    Dthets = [(0.5  + (i * 2.5 / nb_of_Dthet)) for i in range(1, nb_of_Dthet)]
    mean = []
    for Dthet in Dthets:
        mean.append(necessary_nb_of_value_GSC(sig, Dthet))
    stri = ''
    for i in range(len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ')'
    print(stri)

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
        #print("ok")
        Dthet += pas
        pas *= 1.2
        nb_of_iteration *=0.9
        stri = ''
        stri += '(' + str(Dthets[-1]) + ',' + str(mean[-1]) + ') +- (0,' + str(std[-1]) + ')'
        print(stri)
    stri = ''
    for i in range (len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ') +- (0,' + str(std[i]) + ')'
    print(stri)

if __name__ == "__main__":
    #a, b = time_before_detection(1, 0, 1000, h=2.45)
    #print(a)
    #print(2.567 * b / math.sqrt(nb_of_iteration))
    #plot_ARL()
    #plot_theoritical_ARL()
    #change_at_100(0.4)
    #Dthet = 0.5
    #nb_of_iteration = 1000
    #a, b = mean_detection_time_simultaneously(Dthet, nb_of_iteration)
    #print(a)
    #print(2.567 * b / math.sqrt(nb_of_iteration))

    #a, b = mean_detection_time_one_by_one(Dthet, nb_of_iteration)
    #print(a)
    #print(2.567 * b / math.sqrt(nb_of_iteration))

    #a, b = mean_detection_time_adapted_one_by_one(Dthet, nb_of_iteration)
    #print(a)
    #print(2.567 * b / math.sqrt(nb_of_iteration))

    quantify_false_positives(sigs)