from constraint import *
import math
#informations about the precision desired
d_c = 1
d_t = 20
k = 2.576


# sensor information
sensors = {'1': 0.5,
           '2': 0.5,
           '3': 0.8,
           '4': 0.8,
           '5': 0.8,
           '6': 0.8,
           }
n = len(sensors)

# number of emission max for a sensor
N = 30

# definition domain of the period of emissions
D = [1, 2, 5, 10, 15, 20, 25, 30]

problem = Problem()

"""
def resolve_constraint_problem():
    period_names = ['period_' + id for id in sensors]
    fst_emission_names = ['fst_emission_' + id for id in sensors]
    #problem.addVariables(period_names, D)
    #problem.addVariables(fst_emission_names, range(100 * D[-1] * n))
    for period_name in period_names:
        problem.addVariable(period_name, D)
    for fst_emission_name in fst_emission_names:
        problem.addVariable(fst_emission_name, range(100 * D[-1] * n))
    problem.addConstraint(main_function, [period_names + fst_emission_names])
    sol = problem.getSolution()
    print(sol)


def maximum_time(period_names, fst_emission_names):
    maxi = 0
    for id in period_names:
        if maxi < period_names[id] + N * fst_emission_names[id]:
            maxi = period_names[id] + N * fst_emission_names[id]
    return maxi


def main_function(informations):
    period_names = informations[:len(informations) / 2]
    fst_emission_names = informations[len(informations) / 2:]
    t_max = maximum_time(period_names, fst_emission_names)
    return True

"""

sensors = [0.5, 0.8, 0.8, 0.8]
def resolve_constraint_problem():
    problem.addVariables(['period_1', 'period_2'], D)
    problem.addVariables(['fst_emission_1', 'fst_emission_2'],
                         range(1, N * D[-1] * 2))
    problem.addConstraint(main_function, ['period_1', 'period_2',
                                          'fst_emission_1', 'fst_emission_2'])
    solutions = problem.getSolutions()
    maxi_sol, maximax = get_maximized_solution(solutions)
    print("optimized solution")
    print(maxi_sol)
    print("with total monitoring time of ")
    print(maximax)

def get_maximized_solution(solutions):
    maximax = 0
    maxi_sol = []
    for sol in solutions:
        tots = [sol[i] for i in sol]
        p = tots[:len(tots)//2]
        f = tots[len(tots)//2:]
        maxi = maximum_time(p, f)
        if maxi > maximax:
            maximax = maxi
            maxi_sol = sol
    return maxi_sol, maximax

def maximum_time(p, f):
    maxi = 0
    i = 0
    while i < len(p):
        if maxi < f[i] + p[i] * N:
            maxi = f[i] + p[i] * N
        i += 1
    return maxi


def main_function(p1, p2, f1, f2 ):
    p = [p1, p2]
    f = [f1, f2]
    t_max = maximum_time(p, f)
    for t in range(0, t_max - d_t):
        i = 0
        powered_sigma = 0
        nb_sigm = 0
        for inf in zip(f, p):
            if inf[0] <= t + d_t:
                for t_prim in range(t, t + d_t):
                    if t_prim - inf[0] > 0 and (t_prim - inf[0]) % inf[1] == 0 and (t_prim - inf[0]) / inf[1] < N:
                        powered_sigma += math.pow(sensors[i], 2)
                        nb_sigm += 1
            i += 1
        if nb_sigm == 0:
            return False
        sigma = math.sqrt(powered_sigma) / nb_sigm
        if (2 * k *sigma > d_c):
            return False


    return True




if __name__ == "__main__":
    resolve_constraint_problem()

