from pykrige import OrdinaryKriging
import math
import numpy as np
import matplotlib.pyplot as plt
# doc :
# https://geostat-framework.readthedocs.io/projects/pykrige/en/stable/generated/pykrige.ok.OrdinaryKriging.html
plt.style.use("ggplot")

Metric = 0.1 # (sig * T)^2
sigs = [i * 0.1 for i in range (1, 15)]


def fonction_to_follow(t):
    return math.sin(t) + 0.75


def get_T_from_metric_and_sigma(M, sig):
    return math.sqrt(M)/sig


min = 1
max = 30
inputs = np.linspace(min, max, 1000)

def do_krigin_for_one_sigma(sig):
    T = get_T_from_metric_and_sigma(Metric, sig)
    x = np.arange(min, max, T)
    y = np.copy(x)
    for i in range(len(x)):
        y[i] = np.random.normal(fonction_to_follow(x[i]), sig)
    uk = OrdinaryKriging(x, np.zeros(x.shape), y, variogram_model="gaussian", variogram_parameters={'nugget': sig, 'psill': 0.1, 'range' : 3})
    y_pred, y_std = uk.execute("grid", inputs, np.array([0.0]))
    y_pred = np.squeeze(y_pred)
    y_std = np.squeeze(y_std)

    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.scatter(x, y, s=40, label="Input data")

    ax.plot(inputs, y_pred, label="Predicted values")
    ax.fill_between(
        inputs,
        y_pred - 3 * y_std,
        y_pred + 3 * y_std,
        alpha=0.3,
        label="Confidence interval",
    )
    ax.legend(loc=9)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plt.show()
    return y_pred, y_std


def do_kriging_for_set_of_sigmas(sigs):
    Y = []
    for sig in sigs:
        y_pred, y_std = do_krigin_for_one_sigma(sig)
        Y.append()


if __name__ == "__main__":
    #do_krigin_for_one_sigma(0.3)
    y = np.ones((10,10))
    for i in range (10):
        for j in range(10):
            if abs(i-j) > 2:
                y[i][j] = 0
    print(y)
    y_inv = np.linalg.inv(y)
    print(y_inv)