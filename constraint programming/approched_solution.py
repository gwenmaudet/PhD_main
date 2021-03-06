import math
from random import shuffle
import random
import matplotlib.pyplot as plt

# informations about the precision desired
# d_c = 1
d_t = 10
k = 2.576

# sensor data
nb_sensors = 20
sigmin_and_max = (0.5, 1.5)
defition_domain_for_period_emission = range(10, 20)
N = 30

# informations forsimulated annealing
nb_of_iterations = 1000
lambda_constant = 0.999
initial_temp = 500
proba_for_changing_schedulings_rather_than_periods = 0.6


def sensor_creation():
    sensor_list = []
    for i in range(nb_sensors):
        sigma = sigmin_and_max[0] + (sigmin_and_max[1] - sigmin_and_max[0]) * i / (nb_sensors - 1)
        sensor_list.append(sigma)
    return sensor_list


def build_solution_from_sensor_list_and_period(sig, period, d_c):
    fst_emissions = []
    i = 1
    for info in zip(sig, period):
        if not fst_emissions:
            fst_emissions.append(1)
        else:
            t = fst_emissions[-1]
            condition = True
            while condition:
                condition = is_the_condition_realised(t, fst_emissions[:i], period[:i], sig[:i], d_c)
                if condition is True:
                    t += 1
            fst_emissions.append(t)
        i += 1
    t_max = fst_emissions[-1]
    condition = True
    while condition:
        condition = is_the_condition_realised(t_max, fst_emissions, period, sig, d_c)
        if condition is True:
            t_max += 1
    return fst_emissions, t_max


def get_the_max_time(f, p, sig, d_c):
    t = 0
    while True:
        if is_the_condition_realised(t, f, p, sig, d_c) is False:
            return t
        else:
            t += 1

def is_the_condition_realised(t, f, p, sig, d_c):
    sigma_pow = 0
    nb_of_sigmas = 0
    for t_prim in range(t , t + d_t):
        for info in zip(f, p, sig):
            if t_prim >= info[0] and (t_prim - info[0]) % info[1] == 0 and (t_prim - info[0]) / info[1] < N:
                sigma_pow += math.pow(info[2], 2)
                nb_of_sigmas += 1
    if nb_of_sigmas == 0:
        return False
    sigma = math.sqrt(sigma_pow) / nb_of_sigmas
    if 2 * k * sigma > d_c:
        return False
    return True


def neighbour(old_sigmas, old_periods):
    sigmas = list(old_sigmas)
    periods = list(old_periods)
    if random.random() < proba_for_changing_schedulings_rather_than_periods:  # do a permutation of 2 sensor schedules
        i = random.randint(0, nb_sensors - 1)
        j = i
        while i == j:
            j = random.randint(0, nb_sensors - 1)
        sigma = sigmas[i]
        sigmas[i] = sigmas[j]
        sigmas[j] = sigma
    else:  # change the period of a random sensor
        i = random.randint(0, nb_sensors - 1)
        period = periods[i]
        while period == periods[i]:
            period = random.choice(defition_domain_for_period_emission)
        periods[i] = period
    return sigmas, periods


def simulated_annealing(d_c):
    sigmas = sensor_creation()

    energy_evolution = []
    # initialisation
    shuffle(sigmas)
    periods = []
    for i in range(nb_sensors):
        periods.append(random.choice(defition_domain_for_period_emission))
    fst_emissions, energy = build_solution_from_sensor_list_and_period(sigmas, periods, d_c)
    maximum = (energy, sigmas, periods, fst_emissions)
    temperature = initial_temp
    iterations = 0
    while iterations < nb_of_iterations:
        new_sigmas, new_periods = neighbour(sigmas, periods)
        fst_emissions, new_energy = build_solution_from_sensor_list_and_period(new_sigmas, new_periods, d_c)
        if new_energy > energy or random.random() < math.exp(- abs(new_energy - energy) / temperature):
            energy = new_energy
            sigmas = new_sigmas
            periods = new_periods
            if new_energy > maximum[0]:
                maximum = (new_energy, new_sigmas, new_periods, fst_emissions)
        iterations += 1
        temperature *= lambda_constant
        energy_evolution.append(energy)
    """plt.plot(energy_evolution)
    plt.xlabel("iterations")
    plt.ylabel("t_max of the solution")
    plt.suptitle("evolution with evolution on the period and scheduling of sensors")
    # plt.savefig('figs/evolution_with_evolution_on_the_period_and_scheduling_of_sensors.png')"""
    #print(maximum)
    return maximum[0]
    # plt.show()

def pareto_function():
    # informations about the precision desired
    d_C = [0.1 * i for i in range(1, 20)]

    nb_of_time_to_find_maximum = 10
    energies = []
    for d_c in d_C:
        energy = []
        for i in range(nb_of_time_to_find_maximum):
            energy.append(simulated_annealing(d_c))
        energies.append(max(energy))
        #print(max(energy))
    to_print = ""
    for i, en in zip(d_C,energies):
        to_print += '(' + str(round(i,2)) + ',' + str(en) + ')'
    print(to_print)
if __name__ == "__main__":
    pareto_function()
