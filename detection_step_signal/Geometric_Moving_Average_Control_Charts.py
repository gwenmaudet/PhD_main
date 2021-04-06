import math
import numpy as np
import statistics
import time
from scipy.stats import norm
import matplotlib.pyplot as plt
k_alpha = 3.090 #representing quantille of gaussian for 99%

nb_of_iteration = 1000

nb_of_values_of_r = 1000

h = 3

nb_of_Dthet = 10
Dthets = [i *1 /nb_of_Dthet for i in range(nb_of_Dthet)] #thet step for ARL function


def change_at_100(Dthet, r):
    N = 120
    prop_of_detected= [0 for i in range (N)]
    i_s = [i for i in range (N)]
    not_detected = 0
    for p in range(nb_of_iteration):
        g_i = [0 for i in range (len(r))]
        i = 0
        detected = False
        while (i<N) and detected is False:
            if i<(N/2):
                x_i = np.random.normal(0, 1)
            else:
                x_i = np.random.normal(Dthet, 1)
            g_i, detected, rr = update_function_and_find_if_detected_treshold_moving(g_i, r, 1, 0, x_i)
            i += 1
        if i != N:
            prop_of_detected[i] += 1
        else :
            not_detected += 1
    print(not_detected)
    #plt.plot(i_s, prop_of_detected)
    #plt.show()



def find_relationchip_r_parameter_having_same_average_false_positive(sig, N, Dthet):
    g_is = [[] for i in range(1, nb_of_values_of_r)]
    for p in range(nb_of_iteration):
        rs = [i /(5* nb_of_values_of_r) for i in range(1, nb_of_values_of_r)]
        g_i = [Dthet for i in range(1, nb_of_values_of_r)]
        max_gi = g_i
        for i in range(N):
            x_i = np.random.normal(0, sig)
            g_i, detected, rr = update_function_and_find_if_detected_treshold_moving(g_i, rs, sig, 0, x_i)
            for r in range(len(g_i)):
                g = g_i[r]
                if abs(g) > max_gi[r]:
                    max_gi[r] = abs(g)
        for r in range(len(max_gi)):
            g_is[r].append(max_gi[r])
    mean_gis = []
    for elt in g_is:
        mean_gis.append(statistics.mean(elt))

    r_function = []
    for r in rs:
        r_function.append(2.9 * math.sqrt(r / (2 - r)))
    plt.plot(rs, mean_gis)
    plt.plot(rs, r_function, color='green')
    plt.show()


def plot_iterations_for_a_fixed_r_andDthet(r,Dthet, N):
    nb_of_iteration = 10
    iterations = [[[] for i in range(N)] for j in range (len(r))] ## [r_0[N0[it0, it1..],N1[it0, it1..]....], r1[N0[it0, it1..],N1[it0, it1..]....]........]
    N_plot = [i for i in range(N)]
    for p in range(nb_of_iteration):
        g_i = [0 for i in range (len(r))]
        rs = r
        print("####")
        for i in range(N):
            x_i = np.random.normal(Dthet, 1)
            print(g_i[0])
            g_i, boolean, rr = update_function_and_find_if_detected_treshold_moving(g_i, rs, 1, Dthet, x_i)
            print(g_i[0])
            for j in range(len(r)):
                iterations[j][i].append(max(abs(Dthet + g_i[j]), abs(Dthet - g_i[j])) * math.sqrt((2 - r[j]) / r[j]))#

    for j in range(len(r)):
        iterations_plot = [statistics.mean(iterations[j][i]) for i in range(N)]
        plt.plot(N_plot, iterations_plot, label=str(r[j]))
    plt.legend()
    plt.title("")
    plt.xlabel("iteration" + str(Dthet))
    plt.ylabel('sqrt((2 - r) / r) * abs(Dthet - g_i)')
    plt.show()

def find_threshold_for_mean_nmb_of_false_detection(sig, N):
    h = []
    for p in range(nb_of_iteration):
        r = [i / nb_of_values_of_r for i in range(1, nb_of_values_of_r)]
        g_i = [0 for i in range(1, nb_of_values_of_r)]
        max_gi = g_i
        for i in range(N):
            x_i = np.random.normal(0, sig)
            g_i, detected, rr = update_function_and_find_if_detected_treshold_moving(g_i, r, sig, 0, x_i)
            for k in range(len(g_i)):
                g = g_i[k] * math.sqrt((2 - r[k]) / r[k])
                if abs(g) > max_gi[k]:
                    max_gi[k] = abs(g)
        h.append(max(max_gi))
    return statistics.mean(h)


def update_function_and_find_if_detected_treshold_moving(g_i_minus1, r, sig, Dthet, x_i):
    g_i = []
    boolean = False
    rr = 0
    for i in range(len(g_i_minus1)):
        g_i.append(g_i_minus1[i]*(1-r[i]) + r[i] * x_i)
        h_r = h * sig * math.sqrt(r[i]/(2 - r[i]))
        if h_r < max(abs(g_i[i] - Dthet),abs(g_i[i] + Dthet)):
            boolean = True
            rr = r[i]
    return g_i, boolean, rr

def update_function_and_find_if_detected_or_not_fixed_treshold(g_i_minus1,r, sig, Dthet, x_i):
    g_i = []
    boolean = False
    rr = 0
    for i in range(len(g_i_minus1)):
        g_i.append(g_i_minus1[i]*(1-r[i]) + r[i] * x_i)
        h_r = h * sig * math.sqrt(r[i]/(2-r[i]))
        if h_r < max(abs(g_i[i] - Dthet), abs(g_i[i] + Dthet)):
            boolean = True
            rr = r[i]
    return g_i, boolean, rr

def time_before_detection(sig, Dthet, nb_of_iteration):
    r = [i/nb_of_values_of_r for i in range(1, nb_of_values_of_r)]
    nb_of_values = []
    rs = []
    for p in range(nb_of_iteration):
        i = 1
        g_i = [0 for i in range(1, nb_of_values_of_r)]
        x_i = np.random.normal(Dthet, sig)
        g_i, detected, rr = update_function_and_find_if_detected_treshold_moving(g_i, r, sig, 0, x_i)
        if detected:
            rs.append(rr)
        while detected is False:
            x_i = np.random.normal(0, sig)
            g_i, detected, rr = update_function_and_find_if_detected_treshold_moving(g_i, r, sig, 0, x_i)
            i += 1
            if detected:
                rs.append(rr)
        time.sleep(1)
        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)

def plot_theoritical_ARL():
    return 0


def plot_ARL():
    std = []
    mean = []
    nb_of_iteration = 1000
    Dthet = 0.3
    pas = 0.1
    Dthets = []
    while Dthet < 1:
        Dthets.append(Dthet)
        a, b = time_before_detection(1, Dthet, int(nb_of_iteration))
        mean.append(a)
        std.append(2.567 * b / math.sqrt(nb_of_iteration))
        #print("ok")
        Dthet += pas
        #pas *= 1.1
        nb_of_iteration *=0.99
        stri = '(' + str(Dthets[-1]) + ',' + str(mean[-1]) + ') +- (0,' + str(std[-1]) + ')'
        print(stri)
    stri = ''
    for i in range (len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ') +- (0,' + str(std[i]) + ')'
    print(stri)

if __name__ == "__main__":
    plot_ARL()
    #a, b = time_before_detection(1, 0.1, 1000)
    #print(a)
    #print(2.567 * b / math.sqrt(nb_of_iteration))
    #print(find_threshold_for_mean_nmb_of_false_detection(1, 120))
    #find_relationchip_r_parameter_having_same_average_false_positive(1, 120, 0.01)
    #plot_iterations_for_a_fixed_r_andDthet([0.001,0.002, 0.003,  0.006, 0.01, 0.015, 0.020, 0.025, 0.03,
    #                                      0.035, 0.04, 0.06, 0.08, 0.1, 0.15], 0.05, 150)
    #r = [i / nb_of_values_of_r for i in range(1, nb_of_values_of_r)]
    #change_at_100(0.4, r)