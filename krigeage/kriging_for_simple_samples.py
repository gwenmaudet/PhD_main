import random
from math import *
import numpy as np
import matplotlib.pyplot as plt

#informations for covariance computation
theta = 1
variance_cov = 5


#sensor informations
nb_of_information_sent = 10
sensors_infos = [x * 0.1 for x in range(1, 16)]


#experience
t_of_exp = [1, 20 ]
def function_to_follow(t):
    return 0.75 + 10 *sin(2 * pi * t /10)

"""def function_to_follow(t):
    if 0<=t%2 <=1:
        return 1
    else:
        return 0"""
    #return log(pow(t / 2, 5) + 5 + 8 * t) +  8 * pow(5 * t, 1/2) * sin(t / 10 + 5)
# 2.3 * pow(t, 0.5) +
nb_of_points = 1000
points_for_estimation = [t_of_exp[0] + (i * (t_of_exp[1] - t_of_exp[0])/nb_of_points) for i in range (nb_of_points)]





def simulate_reception(sensors_infos):
    receptions = []
    for sigma in sensors_infos:
        for i in range(nb_of_information_sent):
            t = random.random()
            while t < 0.1:
                t = t * 10
            t *= t_of_exp[1]
            y = np.random.normal(function_to_follow(t), sigma)
            receptions.append({'var': sigma, 't': t, 'y': y})

    return receptions


def cov(t1, t2, theta, variance_cov):
    return variance_cov * exp(- pow(t1-t2, 2)/(2 * pow(theta, 2)))

"""def cov(t1, t2, theta, variance_cov):
    return t1 * t2
"""

def define_K_matrix(receptions,theta, variance_cov):
    n = len(receptions)
    K = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            t1 = receptions[i]['t']
            t2 = receptions[j]['t']
            # K.itemset((i, j), cov(t1, t2, theta, variance_cov))
            K[i][j] = cov(t1, t2, theta, variance_cov)
        K[i][i] += receptions[i]['var']
    return K

def define_k_matrix(receptions, t , theta, variance_cov):
    n = len(receptions)
    k = np.zeros((n, 1))
    for i in range(n):
        t1 = receptions[i]['t']
        # k.itemset(i, cov(t1, t, theta, variance_cov))
        k[i] = cov(t1, t, theta, variance_cov)
    return k

def modelise_with_simple_kriging(k, inv_K, y):
    m = np.dot(np.dot(np.transpose(k), inv_K), y)[0][0]
    v = (variance_cov) - np.dot(np.dot(np.transpose(k), inv_K), k)[0][0]
    return round(m,2), round(v,2)
def modelise_with_ordinary_kriging(k, inv_K, y, mu, un):
    m = np.dot(np.transpose(k), inv_K)[0]

    m = np.dot(m, (y - mu * un)) + mu
    return round(m[0], 2), 0


def modelise():
    x = []
    rep = []
    recept = []
    receptions = simulate_reception([0.05])
    x_1 =[]
    rep_1 = []
    for rec in receptions:
        recept.append(rec)
        x.append(rec['t'])
        x_1.append(rec['t'])
        rep_1.append(rec['y'])
        rep.append(rec['y'])

    receptions = simulate_reception([0.5])
    rep_2 = []
    x_2 = []
    for rec in receptions:
        recept.append(rec)
        x.append(rec['t'])
        x_2.append(rec['t'])
        rep_2.append(rec['y'])
        rep.append(rec['y'])


    receptions = simulate_reception([1])
    rep_3 = []
    x_3 = []
    for rec in receptions:
        recept.append(rec)
        x.append(rec['t'])
        x_3.append(rec['t'])
        rep_3.append(rec['y'])
        rep.append(rec['y'])

    receptions = simulate_reception([1.5])
    rep_4 = []
    x_4 = []
    for rec in receptions:
        recept.append(rec)
        x.append(rec['t'])
        x_4.append(rec['t'])
        rep_4.append(rec['y'])
        rep.append(rec['y'])

    n = len(recept)
    K = define_K_matrix(recept, theta, variance_cov)
    inv_K = np.linalg.inv(K)
    y = np.zeros((n, 1))
    for i in range(n):
        y[i] = recept[i]['y']
    model = []
    var_model = []
    real_value = []
    un = np.ones(n)
    mu = np.dot(np.transpose(un), np.dot(inv_K,un))
    mu = np.dot(mu, np.dot(np.transpose(un), inv_K))
    mu = np.dot(mu, y)[0]

    for t in points_for_estimation:
        k = define_k_matrix(recept, t, theta, variance_cov)
        m, v = modelise_with_simple_kriging(k, inv_K, y)
        # m, v = modelise_with_ordinary_kriging(k, inv_K, y, mu, un)
        model.append(m)
        var_model.append(v)
        real_value.append(function_to_follow(t))
    # print(real_value)
    low_bound = []
    high_bound = []
    for (item1, item2) in zip(model, var_model):
        low_bound.append(item1 - 1.96 * item2)
        high_bound.append((item1 + 1.96 * item2))
    real_value = []
    for t in points_for_estimation:
        real_value.append(function_to_follow(t))
    #plt.plot(points_for_estimation, real_value, '--', label='real physical quantity variations')

    plt.plot(x_1, rep_1, 'ro',color='red', label='receptions from sensor 1')
    plt.plot(x_2, rep_2,'ro', color='yellow', label='receptions from sensor 2')
    plt.plot(x_3, rep_3,'ro', color='green', label='receptions from sensor 3')
    plt.plot(x_4, rep_4,'ro', color='blue', label='receptions from sensor 4')
    #plt.plot(points_for_estimation, model, label='estimation curve' )
    #plt.ylim(-10, 10)
    #plt.plot(points_for_estimation, low_bound, 'r-', alpha=0.5)
    #plt.plot(points_for_estimation, high_bound, 'r-', alpha=0.5)
    #plt.fill_between(points_for_estimation, low_bound, high_bound, color='b', alpha=.1,label='95% confidence interval')

    #plt.legend()
    plt.title("kriging solution")
    plt.xlabel("Time t")
    plt.ylabel('physical quantity R(t)')
    plt.show()

if __name__ == "__main__":
    modelise()