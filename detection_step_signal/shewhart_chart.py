import math
import numpy as np
import statistics
import random
import time
import matplotlib.pyplot as plt

h = 5

limit_number_of_taken_values = 200
nb_of_initial_values = 100

nb_of_Dthet = 100
Dthets = [(i * 1 / nb_of_Dthet) for i in range(nb_of_Dthet)]  # thet step for ARL function
sig = 1

# sigs = [(0.5 + i/nb_of_sensors) for i in range(nb_of_sensors)]
# sigs = [2 for i in range(nb_of_sensors)]
sigs = [1, 1.5, 2]
nb_of_sensors = len(sigs)


def mean_detection_time_simultaneously(Dthet, nb_of_iteration):
    nb_of_values = []
    sig_stamp = list(sigs)
    for p in range(nb_of_iteration):
        random.shuffle(sig_stamp)
        X_bar = []
        reception_error = []
        for i in range(nb_of_initial_values):
            sig = sig_stamp[i % nb_of_sensors]
            x = np.random.normal(0, sig)
            n = len(X_bar)
            for j in range(n):
                X_bar[j] = X_bar[j] * (n - j) / (n - j + 1) + x / (n - j + 1)
                reception_error[j] = math.sqrt(math.pow(reception_error[j] * (n - j), 2)
                                               + math.pow(sig, 2)) \
                                     / (n - j + 1)
            X_bar.append(x)
            reception_error.append(sig)
            # print(reception_error)
            # time.sleep(1)
        i = 0
        detected = False
        while detected is False:
            sig = sig_stamp[i % nb_of_sensors]
            x = np.random.normal(Dthet, sig)
            n = len(X_bar)
            if n >= limit_number_of_taken_values:
                X_bar = X_bar[1:]
                reception_error = reception_error[1:]
                n -= 1
            for j in range(n):
                X_bar[j] = X_bar[j] * (n - j) / (n - j + 1) + x / (n - j + 1)
                # print((reception_error[j] * (n-j))**2)
                reception_error[j] = math.sqrt(((reception_error[j] * (n - j))
                                                * (reception_error[j] * (n - j)))
                                               + math.pow(sig, 2)) \
                                     / (n - j + 1)
            X_bar.append(x)
            reception_error.append(sig)
            i += 1
            for j in range(n + 1):
                if (abs(X_bar[j]) > h * reception_error[j]):
                    detected = True
                    # print(X_bar)
                    # print(j)
        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)


def mean_detection_time_one_by_one_and_adapted_one_by_one(Dthet, nb_of_iteration):
    means = []
    stds = []
    for sig in sigs:
        a, b = time_before_detection_step_signal(sig, Dthet, nb_of_iteration)
        means.append(a)
        stds.append(b / math.sqrt(nb_of_iteration))
    q = 0
    for sig in sigs:
        q += math.pow(1 / sig, 2)
    mean_adapted_one_by_one = 0
    std_adapted_one_by_one = 0
    i = 0
    for sig in sigs:
        mean_adapted_one_by_one += math.pow(1 / (q * math.pow(sig, 2)), 2) * means[i]
        std_adapted_one_by_one += stds[i] ** 2 * (1 / (q * math.pow(sig, 2))) ** 2
        i += 1
    mean_adapted_one_by_one *= len(sigs)
    std_adapted_one_by_one = math.sqrt(std_adapted_one_by_one)

    std_one_by_one = 0
    mean_one_by_one = 0
    i = 0
    for sig in sigs:
        std_one_by_one += stds[i] ** 2
        mean_one_by_one += means[i] / math.pow(len(sigs), 2)
        i += 1
    std_one_by_one = math.sqrt(std_one_by_one) / nb_of_sensors
    mean_one_by_one *= len(sigs)
    q = 0
    for m in means:
        q += 1/m
    opti = 0
    for m in means:
        opti += math.pow(1 / (q * m), 2) * m
    opti *= len(sigs)
    return mean_one_by_one, std_one_by_one, mean_adapted_one_by_one, std_adapted_one_by_one, means, opti


def necessary_nb_of_value_GSC(sig, Dthet, h):
    return math.pow(h * sig / Dthet, 2)


def average_nb_of_necessary_values_before_detection(sig, Dthet, nb_of_iteration):
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
def change_at_100(Dthet, nb_of_iteration):
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


def time_before_detection_step_signal(sig, Dthet, nb_of_iteration, h=h):
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
                X_bar[j] = X_bar[j] * (n - j) / (n - j + 1) + x / (n - j + 1)
            X_bar.append(x)
            i += 1
            for j in range(n + 1):
                if (abs(X_bar[j]) > h * sig / math.sqrt(n + 1 - j)):
                    detected = True
                    # print(X_bar)
                    # print(j)
        nb_of_values.append(i)

        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)


def plot_theoritical_ARL():
    nb_of_Dthet = 100
    Dthets = [(0.5 + (i * 2.5 / nb_of_Dthet)) for i in range(1, nb_of_Dthet)]
    mean = []
    for Dthet in Dthets:
        mean.append(necessary_nb_of_value_GSC(sig, Dthet))
    stri = ''
    for i in range(len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ')'
    print(stri)


def plot_ARL():
    sig = 1
    std = []
    mean = []
    expected = []
    h = 10
    nb_of_iteration = 1000
    Dthet = 0.8
    pas = 0.1
    Dthets = []
    while Dthet < 2:
        Dthets.append(Dthet)
        a, b = time_before_detection_step_signal(sig, Dthet, int(nb_of_iteration), h)
        mean.append(a)
        std.append(2.567 * b / math.sqrt(nb_of_iteration))
        expected.append(necessary_nb_of_value_GSC(sig, Dthet, h))
        # print("ok")
        Dthet += pas
        pas *= 1.1
        nb_of_iteration *= 0.9
        stri = ''
        stri += '(' + str(Dthets[-1]) + ',' + str((mean[-1] - expected[-1]) * 100 / mean[-1]) + ') +- (0,)'
        print(stri)
    stri = ''
    for i in range(len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str((mean[i] - expected[i]) * 100 / mean[i]) + ')'
    print(stri)
    stri = ''
    for i in range(len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ')'
    print(stri)
    stri = ''
    for i in range(len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(expected[i]) + ')'
    print(stri)


def time_before_detection_linear_signal(sig, slope, nb_of_iteration, h=h):
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
            i += 1
            x = np.random.normal(slope * i, sig)
            n = len(X_bar)
            if n >= limit_number_of_taken_values:
                X_bar = X_bar[1:]
                n -= 1
            for j in range(n):
                X_bar[j] = X_bar[j] * (n - j) / (n - j + 1) + x / (n - j + 1)
            X_bar.append(x)

            for j in range(n + 1):
                if (abs(X_bar[j]) > h * sig / math.sqrt(n + 1 - j)):
                    detected = True
                    # print(X_bar)
                    # print(j)
        nb_of_values.append(i)

        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)


def plot_LGAARL():
    std = []
    mean = []
    nb_of_iteration = 80000
    Dthet = 0.0
    pas = 0.0005
    Dthets = []
    while Dthet < 0.4:
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


def main_1(Dthet):
    # Dthet = 0.5
    nb_of_iteration = 10000
    f, g = mean_detection_time_simultaneously(Dthet, nb_of_iteration)
    a, b, c, d, mean,e = mean_detection_time_one_by_one_and_adapted_one_by_one(Dthet,
                                                                          int(nb_of_iteration / math.sqrt(len(sigs))))
    """print('simultaneously')
    print(f)
    print(2.567 * g / math.sqrt(nb_of_iteration))

    print("one by one")
    print(a)
    print(2.567 * b)
    print("adapted one by one")
    print(c)
    print(2.567 * d)
    print(e)
    print(sigs)"""
    return f, 2.567 * g / math.sqrt(nb_of_iteration), a, 2.567 * b, c, 2.567 * d, e


def main_2():
    Dthets = [0.5 + i * 2 / 10 for i in range(0, 10)]
    mean_simul = []
    std_simul = []
    mean_one_one = []
    std_one_one = []
    mean_adapted = []
    std_adapted = []
    mean_opti = []
    for Dthet in Dthets:
        a, b, c, d, e, f, g= main_1(Dthet)
        mean_simul.append(a)
        std_simul.append(b)
        mean_one_one.append(c)
        std_one_one.append(d)
        mean_adapted.append(e)
        std_adapted.append(f)
        mean_opti.append(g)

    moyenne = 0
    for i in range(len(Dthets)):
        moyenne += abs((mean_adapted[i] - mean_opti[i])/mean_opti[i])
    #print(moyenne / len(Dthets))

    plt.plot(Dthets, mean_simul, label='S0 round robin')
    plt.plot(Dthets, mean_one_one, label='S1 un par un un')
    plt.plot(Dthets, mean_adapted, label='S2 un par un période modifiée')
    plt.plot(Dthets, mean_opti, label="S Opt optimum global pour les stratégies un par un")

    lower_boundary = []
    upper_boundary = []
    for i in range(len(Dthets)):
        lower_boundary.append(mean_simul[i] - std_simul[i])
        upper_boundary.append(mean_simul[i] + std_simul[i])
    plt.fill_between(Dthets, lower_boundary, upper_boundary, color='#D3D3D3')
    lower_boundary = []
    upper_boundary = []
    for i in range(len(Dthets)):
        lower_boundary.append(mean_one_one[i] - std_one_one[i])
        upper_boundary.append(mean_one_one[i] + std_one_one[i])
    plt.fill_between(Dthets, lower_boundary, upper_boundary, color='#D3D3D3')

    lower_boundary = []
    upper_boundary = []
    for i in range(len(Dthets)):
        lower_boundary.append(mean_adapted[i] - std_adapted[i])
        upper_boundary.append(mean_adapted[i] + std_adapted[i])
    plt.fill_between(Dthets, lower_boundary, upper_boundary, color='#D3D3D3', label='99% confiance intervalle')
    plt.legend()
    plt.xlabel("amplitude du changement à detecter")
    plt.ylabel("temps moyen avant de lever une alerte de detection de changement")
    plt.title("comparaisons de stratégies d'émission pour des problèmes de detection en utilisant la méthode GLR")
    plt.show()



if __name__ == "__main__":
    # quantify_false_positives(sigs)

    # for sig in sigs:
    #    a, b = time_before_detection_step_signal(sig, 3, 10000, h=10)
    #    print("########")
    #    print(sig)
    #    print(a)

    # plot_LGAARL()
    #main_2()
    plot_ARL()