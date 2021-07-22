import numpy as np
import math
import statistics


nb_of_initial_values = 10
limit_number_of_taken_values = 200


h = 3


def time_before_detection_step_signal(sig, Dthet, nb_of_iteration, h=h):
    nb_of_values = []
    for p in range(nb_of_iteration):
        X_bar = []
        X_GLR = []
        for i in range(nb_of_initial_values):
            x = np.random.normal(0, sig)
            n = len(X_bar)

            #Shewhart chart
            print("kaboum")
            for j in range(n):
                X_bar[j] = (X_bar[j] * math.sqrt(n - j) + x ) / math.sqrt(n-j+1)
            X_bar.append(x)
            print("boum")

            #GLR
            for j in range(n):
                X_GLR[j] = math.pow(math.sqrt(X_GLR[j] * (n - j)) + x, 2) / (n - j + 1)
            X_GLR.append(math.pow(x, 2))
            print(x)
        kk = []
        for el in X_bar:
            kk.append(math.pow(el, 2))
        print(kk)
        print(X_GLR)
        i = 0
        detected = False
        while detected is False:
            x = np.random.normal(Dthet, sig)
            n = len(X_bar)
            if n >= limit_number_of_taken_values:
                X_bar = X_bar[1:]
                X_GLR = X_GLR[1:]
                n -= 1
            for j in range(n):
                X_bar[j] = X_bar[j] * math.sqrt(n-j) / math.sqrt(n-j+1) + x / math.sqrt(n-j+1)
                X_GLR[j] = math.pow(math.sqrt(X_GLR[j] * (n - j)) + x, 2) / (n - j + 1)
            X_GLR.append(math.pow(x, 2))
            X_bar.append(x)
            i += 1
            j = 0
            while (j<=n and detected is False):
                if (abs(X_bar[j]) > h * sig):
                    detected = True
                if (X_GLR[j]) > math.sqrt(h) * math.pow(sig, 2):
                    detected = True
                if detected is True:
                    print("ok")
                    print(j)
                    print("GLR")

                    print(X_GLR[j] / (math.sqrt(h) * math.pow(sig, 2)))
                    print(X_GLR)
                    print("X_BAR")
                    print(abs(X_bar[j]) / (h * sig))
                    print(X_bar)
                j +=1
        nb_of_values.append(i)


        nb_of_values.append(i)
    return statistics.mean(nb_of_values), statistics.stdev(nb_of_values)

if __name__ == "__main__":
    time_before_detection_step_signal(1, 1, 2)