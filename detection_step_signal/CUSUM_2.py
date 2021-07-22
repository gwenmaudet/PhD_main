import math
import numpy as np
import statistics
import random
import matplotlib.pyplot as plt

nb_of_iteration = 1000
nb_of_initial_values = 100

mu_1 = 1
h = 10

nb_of_Dthet = 200
Dthets = [i * 2 / nb_of_Dthet for i in range(nb_of_Dthet)]

sig_sensors = [1, 1.5, 2]

def time_before_detection_step_signal(sigs, Dthet, nb_of_iteration, h):
    n = len(sigs)
    nb_of_values = []
    for p in range(nb_of_iteration):
        g_k_minus = 0
        g_k_plus = 0
        random.shuffle(sigs)
        for i in range(1, nb_of_initial_values):
            sig = sigs[i % n]
            X_i = np.random.normal(0, sig)
            g_k_minus = max(0, g_k_minus - (X_i + mu_1 / 2) * mu_1 / sig)
            g_k_plus = max(0, g_k_plus + (X_i - mu_1 / 2) * mu_1 / sig)
        i = nb_of_initial_values
        detected = False
        while detected is False:
            sig = sigs[i % n]
            X_i = np.random.normal(Dthet, sig)
            i += 1
            g_k_minus = max(0, g_k_minus - (X_i + mu_1 / 2) * mu_1 / sig**2)
            g_k_plus = max(0, g_k_plus + (X_i - mu_1 / 2) * mu_1 / sig**2)
            if g_k_plus > h or g_k_minus > h:
                detected = True
        nb_of_values.append(i - nb_of_initial_values)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)


def plot_CUSUM_principle():
    sigs = [0.7]
    Dthet = 1.5
    n = 1
    h = 15
    nb_of_initial_values = 20
    g_k_minus = 0
    g_k_plus = 0
    random.shuffle(sigs)
    abscissa = []
    constant = []
    X = []
    g = []
    for i in range(1, nb_of_initial_values):
        sig = sigs[i % n]
        X_i = np.random.normal(0, sig)
        g_k_minus = max(0, g_k_minus - (X_i + mu_1 / 2) * mu_1 / sig)
        g_k_plus = max(0, g_k_plus + (X_i - mu_1 / 2) * mu_1 / sig)
        X.append(X_i)
        g.append(g_k_plus)
        abscissa.append(i)
        constant.append(mu_1 / 2)
    i = nb_of_initial_values
    detected = False
    while detected is False:
        sig = sigs[i % n]
        X_i = np.random.normal(Dthet, sig)
        i += 1
        g_k_minus = max(0, g_k_minus - (X_i + mu_1 / 2) * mu_1 / sig)
        g_k_plus = max(0, g_k_plus + (X_i - mu_1 / 2) * mu_1 / sig)
        if g_k_plus > h or g_k_minus > h:
            detected = True
        g.append(g_k_plus)
        X.append(X_i)
        abscissa.append(i)
        constant.append(mu_1 / 2)
    plt.plot(abscissa, X, label="receptions")
    plt.plot(abscissa, g, label="decision function")
    plt.plot(abscissa, constant, '--', label="")
    plt.axvline(x=nb_of_initial_values, label="change time", color='black')
    plt.legend()
    plt.xlabel("time")
    plt.title("Representation de la fonction de décision de la méthode CUSUM")

    plt.show()

def main_1(Dthet):
    means = []
    stds = []
    #Dthet = 1
    nb_of_iteration = 10000
    h = 10
    sigs = [1, 1.5, 2]
    nb_of_sensors = len(sigs)
    for sig in sigs:
        mean, std = time_before_detection_step_signal([sig], Dthet, int(nb_of_iteration/math.sqrt(len(sigs))), h)
        means.append(mean)
        stds.append(std/math.sqrt(nb_of_iteration/math.sqrt(len(sigs))))
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



    mean, std = time_before_detection_step_signal(sigs, Dthet, nb_of_iteration, h)
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
    return mean, 2.567 * std / math.sqrt(nb_of_iteration), mean_one_by_one, 2.567 * std_one_by_one, mean_adapted_one_by_one, 2.567 * std_adapted_one_by_one, opti

def main_2():
    Dthets = [1 + i*2/10 for i in range(0, 10)]
    mean_simul = []
    std_simul = []
    mean_one_one =[]
    std_one_one = []
    mean_adapted = []
    std_adapted = []
    mean_opti = []
    for Dthet in Dthets:
        a,b,c,d,e,f, h = main_1(Dthet)
        mean_simul.append(a)
        std_simul.append(b)
        mean_one_one.append(c)
        std_one_one.append(d)
        mean_adapted.append(e)
        std_adapted.append(f)
        mean_opti.append(h)
    moyenne = 0
    for i in range(len(Dthets)):
        moyenne += abs((mean_adapted[i] - mean_opti[i])/mean_opti[i])
    #print(moyenne / len(Dthets))
    plt.plot(Dthets, mean_simul, label = 'S0 round robin')
    plt.plot(Dthets, mean_one_one, label= 'S1 un par un un')
    plt.plot(Dthets, mean_adapted, label='S2 un par un période modifiée')
    plt.plot(Dthets, mean_opti, label='S Opt Optimum global pour les stragégies un par un')

    lower_boundary = []
    upper_boundary = []
    for i in range (len(Dthets)):
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
    plt.title("comparaisons de stratégies d'émission pour des problèmes de detection en utilisant la méthode CUSUM")
    plt.show()
if __name__ == "__main__":
    # a, b = time_before_detection(1, 0, 100000)
    # print(a)
    # print(2.567 * b / math.sqrt(nb_of_iteration))
    # plot_ARL()
    # plot_LGAARL()
    #plot_CUSUM_principle()
    main_2()
