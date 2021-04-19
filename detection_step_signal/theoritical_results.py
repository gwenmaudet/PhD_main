import math
import numpy as np
import statistics
import time
from scipy.stats import norm
import matplotlib.pyplot as plt


sigmas = [0.1, 0.3, 0.4, 0.9, 1, 1.2]

h = 13.5
N = 1
nb_of_Dthets = 100

def ARL_one_by_one(T):
    Dthets = [(0.5 + i*2.5/nb_of_Dthets) for i in range (nb_of_Dthets)]
    mean = []
    for D in Dthets:
        m = 0
        for s in sigmas:
            m += T *  math.ceil(math.pow((h * s/D), 2))
        mean.append(round(m / len(sigmas),3))
    stri = ''
    for i in range(len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ')'
    print(stri)

def ARL_adapted_one_by_one(T):
    Dthets = [(0.5 + i * 2.5 / nb_of_Dthets) for i in range(nb_of_Dthets)]
    mean = []
    for D in Dthets:
        m = 0
        for s in sigmas:
            m += 1 / math.ceil(math.pow((h * s / D), 2))
        mean.append(round(len(sigmas)*T/m, 3))
    stri = ''
    for i in range(len(Dthets)):
        stri += '(' + str(Dthets[i]) + ',' + str(mean[i]) + ')'
    print(stri)


if __name__ == "__main__":
    T = 1
    ARL_one_by_one(T)
    #ARL_adapted_one_by_one(T)