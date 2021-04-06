import math
import numpy as np
import statistics


k_alpha = 12

nb_of_iteration = 1000

nb_of_Dthet = 100
Dthets = [(i * 1 / nb_of_Dthet) for i in range(nb_of_Dthet)] #thet step for ARL function
sig = 1

def necessary_nb_of_value_GSC(sig,Dthet):
    return math.ceil(math.pow(k_alpha * sig/Dthet, 2))



def average_nb_of_necessary_values_before_detection(sig, Dthet):
    nb_of_values = []
    for p in range(nb_of_iteration):
        i = 1
        X_bar = [np.random.normal(0, sig)]
        mean = statistics.mean(X_bar)
        while (mean + (k_alpha * sig/math.sqrt(i))>Dthet):
            X_bar.append(np.random.normal(0, sig))
            mean = statistics.mean(X_bar)
            i += 1
        nb_of_values.append(i)
    return statistics.mean(nb_of_values)


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
        if (mean + (k_alpha * sig) < Dthet) or (mean - (k_alpha * sig) > Dthet):
            detected = True
        while (i < N) and detected is False:
            x = np.random.normal(0, sig)
            n = len(X_bar)
            for j in range(n):
                X_bar[j] = X_bar[j] * (n - j) / (n - j + 1) + x / (n - j + 1)
            X_bar.append(x)
            i += 1
            for j in range(n + 1):
                if (X_bar[j] + (k_alpha * sig / math.sqrt(n + 1 - j)) < Dthet) or (
                        X_bar[j] - (k_alpha * sig / math.sqrt(n + 1 - j)) > Dthet):
                    detected = True
        if i != N:
            prop_of_detected[i] += 1
        else:
            not_detected += 1
    print(not_detected)








def time_before_detection(sig,Dthet, nb_of_iteration):
    nb_of_values = []
    for p in range(nb_of_iteration):
        i = 1
        X = [np.random.normal(0, sig)]
        X_bar = [X[0]]
        mean = X[0]
        detected = False
        if (mean + (k_alpha * sig) < Dthet) or (mean - (k_alpha * sig ) > Dthet):
           detected = True

        while detected is False:
            x = np.random.normal(0, sig)
            X.append(x)
            n = len(X_bar)
            for j in range(n):
                X_bar[j] = X_bar[j] * (n-j) / (n-j+1) + x / (n-j+1)
            X_bar.append(x)
            i += 1
            for j in range(n+1):
                if (X_bar[j] + (k_alpha * sig / math.sqrt(n+1 - j)) < Dthet) or (X_bar[j] - (k_alpha * sig / math.sqrt(n+1 - j)) > Dthet):
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
    nb_of_iteration = 10000
    Dthet = 0.5
    pas = 0.1
    Dthets = []
    while Dthet < 3:
        Dthets.append(Dthet)
        a, b = time_before_detection(sig, Dthet, int(nb_of_iteration))
        mean.append(a)
        std.append(2.567 * b / math.sqrt(nb_of_iteration))
        print("ok")
        Dthet += pas
        #pas *= 1.1
        nb_of_iteration *=0.99
    stri = ''
    for i in range (len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ') +- (0,' + str(std[i]) + ')'
    print(stri)

if __name__ == "__main__":
    #print(time_before_detection(1, 0.5, 100))
    #plot_ARL()
    plot_theoritical_ARL()
    #change_at_100(0.4)