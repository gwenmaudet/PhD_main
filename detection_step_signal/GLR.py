import math
import numpy as np
import statistics
import random
import time
import matplotlib.pyplot as plt

h = 40

limit_number_of_taken_values = 200
nb_of_initial_values = 100

nb_of_Dthet = 100
Dthets = [(i * 1 / nb_of_Dthet) for i in range(nb_of_Dthet)]  # thet step for ARL function

# sigs = [(0.5 + i/nb_of_sensors) for i in range(nb_of_sensors)]
# sigs = [2 for i in range(nb_of_sensors)]
sigs = [0.1, 0.5, 1.5]
nb_of_sensors = len(sigs)


def time_before_detection_step_signal(sigs, Dthet, nb_of_iteration, probas=[1] * len(sigs), h=h):
    n= len(sigs)
    nb_of_values = []
    for p in range(nb_of_iteration):
        #random.shuffle(sigs)
        X_bar = []  # somme y_i -mu_0 / sigma i
        nb_of_initial_values =random.randint(200, 200 + n )
        for i in range(nb_of_initial_values):
            sig = sigs[i % n]
            p = random.random()
            if p<probas[i % n]:
                x = np.random.normal(0, sig)
                m = len(X_bar)
                for j in range(m):
                    X_bar[j] = X_bar[j] + x / sig
                X_bar.append(x)
                # print(reception_error)
                # time.sleep(1)
        detected = False
        i = nb_of_initial_values
        while detected is False:
            sig = sigs[i % n]
            p = random.random()
            if p < probas[i % n]:
                x = np.random.normal(Dthet, sig)
                """m = len(X_bar)
                if m >= limit_number_of_taken_values:
                    X_bar = X_bar[1:]
                    m -= 1"""
                for j in range(m):
                    X_bar[j] = X_bar[j] + x / sig
                    # print((reception_error[j] * (n-j))**2)
                X_bar.append(x)
                for j in range(m + 1):
                    if (abs(X_bar[j]) / math.sqrt(m - j + 1) > h):
                        detected = True
                        # print(X_bar)
                        # print(j)
            i += 1
        nb_of_values.append(i - nb_of_initial_values)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values), nb_of_values

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
"""


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
        a, b = time_before_detection_step_signal([sig], Dthet, int(nb_of_iteration), h)
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
"""
def main_1(Dthet):
    means = []
    stds = []
    # Dthet = 1
    nb_of_iteration = 10000
    #h = 10
    sigs = [1, 1.5, 2]
    nb_of_sensors = len(sigs)
    for sig in sigs:
        mean, std,z = time_before_detection_step_signal([sig], Dthet, int(nb_of_iteration / math.sqrt(len(sigs))))
        means.append(mean)
        stds.append(std / math.sqrt(nb_of_iteration / math.sqrt(len(sigs))))
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
        q += 1 / m
    opti = 0
    for m in means:
        opti += math.pow(1 / (q * m), 2) * m
    opti *= len(sigs)

    mean, std, z = time_before_detection_step_signal(sigs, Dthet, nb_of_iteration)
    """
    print("one by one")
    print(mean_one_by_one)
    print(2.567 * std_one_by_one)
    print("adapted one by one")
    print(mean_adapted_one_by_one)
    print(2.567 * std_adapted_one_by_one)


    print("simultaneously")
    print(mean)
    print(2.567 * std / math.sqrt(nb_of_iteration))
    """
    return mean, 2.567 * std / math.sqrt(
        nb_of_iteration), mean_one_by_one, 2.567 * std_one_by_one, mean_adapted_one_by_one, 2.567 * std_adapted_one_by_one, opti


def main_2():
    Dthets = [1 + i * 2 / 10 for i in range(0, 10)]
    mean_simul = []
    std_simul = []
    mean_one_one = []
    std_one_one = []
    mean_adapted = []
    std_adapted = []
    mean_opti = []
    for Dthet in Dthets:
        a, b, c, d, e, f, g = main_1(Dthet)
        mean_simul.append(a)
        std_simul.append(b)
        mean_one_one.append(c)
        std_one_one.append(d)
        mean_adapted.append(e)
        std_adapted.append(f)
        mean_opti.append(g)
    moyenne = 0
    for i in range(len(Dthets)):
        moyenne += abs((mean_adapted[i] - mean_opti[i]) / mean_opti[i])
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


def main_3():
    Dthet = 1
    sigs = [0.1, 0.5, 1.5]
    nb_of_iteration = 1000

    ##### fst approach, nested one
    sigmas = [sigs[0],sigs[1]]
    for i in range (5):
        sigmas.append(sigs[2])
    sigmas.append(sigs[1])
    for i in range (5):
        sigmas.append(sigs[2])
    sigmas.append(sigs[1])
    for i in range(5):
        sigmas.append(sigs[2])
    sigmas.append(sigs[1])
    for i in range(5):
        sigmas.append(sigs[2])
    mean = time_before_detection_step_signal(sigmas, Dthet, nb_of_iteration, h=h)
    print(mean)

    sigs_lengths = 500

    means = []
    stds = []
    for i in range(int(nb_of_iteration/100)):
        sigmas = []
        for j in range(sigs_lengths):
            p = random.random()
            if p < 0.04:
                sigmas.append(sigs[0])
            elif p < 0.2:
                sigmas.append(sigs[1])
            else:
                sigmas.append(sigs[2])
        mean = time_before_detection_step_signal(sigmas, Dthet, 100, h=h)
        means.append(mean[0])
        stds.append(mean[1])
    print(statistics.mean(means))
    print(statistics.mean(stds))


def comparison_of_different_scheduling(nb_of_first,nb_of_second,sigma_first, sigma_second, first_proba, second_proba, nb_of_cases):
    infos = []
    for i in range(nb_of_first):
        infos.append([sigma_first,first_proba])
    for i in range(nb_of_second):
        infos.append([sigma_second, second_proba])

    nb_of_iteration = 1000
    h = 40
    Dthet = 0.5
    means = []
    stds = []
    for i in range(nb_of_cases):
        random.shuffle(infos)
        sigmas = []
        probas = []
        for elt in infos:
            sigmas.append(elt[0])
            probas.append(elt[1])
        mean, std, z = time_before_detection_step_signal(sigmas, Dthet, nb_of_iteration,probas, h)
        means.append(mean)
        stds.append(std/math.sqrt(nb_of_iteration))
    means = sorted(means)
    n = len(means)
    to_print = ""
    tot = 0
    for elt in means:
        tot += 1/n
        to_print += "(" + str(elt) +"," + str(tot) + ') '
    print(to_print)

def comparison_of_two_opposite_schedulings(nb_of_first,nb_of_second,sigma_first, sigma_second, first_proba, second_proba):

    nb_of_iteration = 50000
    h = 40
    Dthet = 1

    #### construction of the strategy where in the first time it is always the fisrt cat, then after the second cat..
    infos = []
    for i in range(nb_of_first):
        infos.append([sigma_first, first_proba])
    for i in range(nb_of_second):
        infos.append([sigma_second, second_proba])
    sigmas = []
    probas = []
    for elt in infos:
        sigmas.append(elt[0])
        probas.append(elt[1])
    mean, std, nb_of_value_before_detection = time_before_detection_step_signal(sigmas, Dthet, nb_of_iteration, probas, h)
    print(mean)
    nb_of_value_before_detection = sorted(nb_of_value_before_detection)
    values = []
    nb_of_items = []
    values.append(nb_of_value_before_detection.pop(0))
    nb_of_items.append(1)
    for elt in nb_of_value_before_detection:
        if elt ==values[-1]:
            nb_of_items[-1] += 1
        else:
            values.append(elt)
            nb_of_items.append(1)

    n = len(nb_of_value_before_detection)
    to_print = ""
    tot = 0
    for elt in zip(values, nb_of_items):
        tot += elt[1] / n
        to_print += "(" + str(elt[0]) + "," + str(tot) + ') '
    print(to_print)



    pgcd = math.gcd(nb_of_first, nb_of_second)
    infos = []
    for i in range(int(nb_of_first/pgcd)):
        infos.append([sigma_first,first_proba])
    for i in range(int(nb_of_second/pgcd)):
        infos.append([sigma_second, second_proba])
    sigmas = []
    probas = []
    for elt in infos:
        sigmas.append(elt[0])
        probas.append(elt[1])
    mean, std, nb_of_value_before_detection = time_before_detection_step_signal(sigmas, Dthet, nb_of_iteration, probas,
                                                                           h)
    print(mean)
    nb_of_value_before_detection = sorted(nb_of_value_before_detection)
    values = []
    nb_of_items = []
    values.append(nb_of_value_before_detection.pop(0))
    nb_of_items.append(1)
    for elt in nb_of_value_before_detection:
        if elt == values[-1]:
            nb_of_items[-1] += 1
        else:
            values.append(elt)
            nb_of_items.append(1)

    n = len(nb_of_value_before_detection)
    to_print = ""
    tot = 0
    for elt in zip(values, nb_of_items):
        tot += elt[1] / n
        to_print += "(" + str(elt[0]) + "," + str(tot) + ') '
    print(to_print)




def plot_CDF_of_one_random_solution(nb_of_first,nb_of_second,sigma_first, sigma_second, first_proba, second_proba):
    Dthet = 0.5
    nb_of_iteration = 10000
    h = 40
    infos = []
    for i in range(nb_of_first):
        infos.append([sigma_first, first_proba])
    for i in range(nb_of_second):
        infos.append([sigma_second, second_proba])
    random.shuffle(infos)
    sigmas = []
    probas = []
    for elt in infos:
        sigmas.append(elt[0])
        probas.append(elt[1])
    mean, std, nb_of_value_before_detection = time_before_detection_step_signal(sigmas, Dthet, nb_of_iteration, probas, h)
    print(mean)
    nb_of_value_before_detection = sorted(nb_of_value_before_detection)
    values = []
    nb_of_items = []
    values.append(nb_of_value_before_detection.pop(0))
    nb_of_items.append(1)
    for elt in nb_of_value_before_detection:
        if elt == values[-1]:
            nb_of_items[-1] += 1
        else:
            values.append(elt)
            nb_of_items.append(1)

    n = len(nb_of_value_before_detection)
    to_print = ""
    tot = 0
    for elt in zip(values, nb_of_items):
        tot += elt[1] / n
        to_print += "(" + str(elt[0]) + "," + str(tot) + ') '
    print(to_print)

def test():


    values = []
    for i in range(100000):
        values.append(np.random.normal(0,0.1)/0.1)
    values = sorted(values)
    plt.plot(values)
    plt.show()
    values = []
    for i in range(100000):
        values.append(np.random.normal(0, 1))
    values = sorted(values)
    plt.plot(values)
    plt.show()

def function_of_the_performance_according_to_the_error_noise():
    Dthet = 1
    nb_of_iteration = 10000
    h = 40
    sigs = [i/10 + 0.1 for i in range(20)]
    perfs = []
    for sig in sigs:
        mean, std, values = time_before_detection_step_signal([sig], Dthet, nb_of_iteration, probas=[1] * len(sigs), h=h)
        perfs.append(mean)
    plt.plot(sigs,perfs)
    plt.show()

if __name__ == "__main__":
    # quantify_false_positives(sigs)

    # for sig in sigs:
    #    a, b = time_before_detection_step_signal(sig, 3, 10000, h=10)
    #    print("########")
    #    print(sig)
    #    print(a)

    # plot_LGAARL()
    #main_3()
    """nb_of_first = 50
    nb_of_second = 50
    sigma_first = 0.1
    sigma_second = 0.1
    first_proba = 1
    second_proba = 1

    nb_of_cases = 2

    comparison_of_different_scheduling(nb_of_first, nb_of_second, sigma_first, sigma_second, first_proba, second_proba, nb_of_cases)
    """
    function_of_the_performance_according_to_the_error_noise()
    #comparison_of_two_opposite_schedulings(nb_of_first, nb_of_second, sigma_first, sigma_second, first_proba, second_proba)
    #plot_CDF_of_one_random_solution(nb_of_first, nb_of_second, sigma_first, sigma_second, first_proba, second_proba)
