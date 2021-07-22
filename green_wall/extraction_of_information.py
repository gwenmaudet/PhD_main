from pykrige.uk import UniversalKriging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import statistics

import get_values_from_DB
import generic_tools
import conf
from conf import coordinates


############## plot a heat map of the last output of the sensors ##########

def plot_the_last_measures():
    data = np.zeros((len(coordinates), 3))
    index = 0
    last_measure = get_values_from_DB.get_last_measure()
    for sensor_key in coordinates:
        data[index][0] = coordinates[sensor_key][0]
        data[index][1] = coordinates[sensor_key][1]
        data[index][2] = last_measure["measure"][sensor_key]
        index += 1
    gridx = np.arange(conf.x_min - conf.x_border, conf.x_max + conf.x_border, conf.x_foot)
    gridy = np.arange(conf.y_min - conf.y_border, conf.y_max + conf.y_border, conf.y_foot)
    input_values = np.zeros((len(gridx), len(gridy)))
    for i in range(len(gridx) - 1):
        for j in range(len(gridy) - 1):
            for sensor_key in coordinates:
                if gridx[i] <= coordinates[sensor_key][0] < gridx[i + 1]:
                    if gridy[j] <= coordinates[sensor_key][1] < gridy[j + 1]:
                        input_values[i][j] = last_measure["measure"][sensor_key]
                        name = 'sensor number ' + str(sensor_key)
                        plt.scatter(i, j, label=name)
    print(data)
    UK = UniversalKriging(
        data[:, 0],
        data[:, 1],
        data[:, 2],
        variogram_model="gaussian",

    )

    z, ss = UK.execute("grid", gridx, gridy)
    print(z)
    # print(input_values)

    plt.imshow(z, cmap='gray', norm=matplotlib.colors.Normalize(vmin=0, vmax=conf.max_voltage),
               origin='lower')
    string = "heat map (white = Really dry -  black = really wet), made at time" + last_measure['date'][0:19]
    plt.title(string)
    plt.legend()
    plt.show()




################# Return a graph of the average daily humidity of the past 'number_of_days' days ##########

def plot_average_humidity_of_last_days(number_of_days):
    last_measure = get_values_from_DB.get_last_measure()
    day, month, year = generic_tools.get_date(last_measure['date'])
    average_measure_of_humidity = []
    for i in range(number_of_days): # add values from the most recent to the oldest
        measures_of_the_day = get_values_from_DB.get_all_data_from_one_day(day, month, year)
        mean_measures = []
        for measures in measures_of_the_day:
            mean_measures.append(statistics.mean(measures['measure']))
        average_measure_of_humidity.append(statistics.mean(mean_measures))
        day, month, year = generic_tools.the_day_before(day, month, year)
    humidity_percentage = []
    for mean_mesure_of_the_day in mean_measures:
        humidity_percentage.append(generic_tools.convert_voltage_in_humidity_percentage(mean_mesure_of_the_day))
    abscissa = [i for i in range(number_of_days)]
    humidity_percentage.reverse() # reverse in order to have a chronological plot
    plt.plot(abscissa, humidity_percentage)
    plt.title()
    plt.show()

def plot_humidity_of_the_day(day, month, year):
    measures_of_the_day = get_values_from_DB.get_all_data_from_one_day(day, month, year)
    measures_of_the_day.reverse()
    measures_of_the_day = generic_tools.process_insert_sorting(measures_of_the_day)
    humidity_of_the_day = []
    h_0 = []
    h_1 = []
    h_2 = []
    h_3 = []

    time = []
    for measure in measures_of_the_day:
        humidity_of_the_day.append(generic_tools.convert_voltage_in_humidity_percentage(statistics.mean(measure['measure'])))
        h_0.append(generic_tools.convert_voltage_in_humidity_percentage(measure['measure'][0]))
        h_1.append(generic_tools.convert_voltage_in_humidity_percentage(measure['measure'][1]))
        h_2.append(generic_tools.convert_voltage_in_humidity_percentage(measure['measure'][2]))
        h_3.append(generic_tools.convert_voltage_in_humidity_percentage(measure['measure'][3]))
        time.append(generic_tools.convert_time_in_hours(measure['date']))
    #plt.scatter(time,humidity_of_the_day)
    plt.plot(time,h_0,label='receptions from sensor 1')
    plt.plot(time, h_1, label='receptions from sensor 2')
    plt.plot(time, h_2, label='receptions from sensor 3')
    plt.plot(time, h_3, label='receptions from sensor 4')
    plt.legend()
    plt.xlabel("time in hours")
    plt.ylabel("humidity percentage")
    plt.title("average humidity of the green wall during the day "
              + generic_tools.int_in_date_type(day) + '-' + generic_tools.int_in_date_type(month)
              + '-' +generic_tools.int_in_date_type(year) )
    plt.xlim(0, 24)
    plt.ylim(0, 100)
    plt.show()




if __name__ == "__main__":
    #plot_the_last_measures()
    plot_humidity_of_the_day(14, 6, 2021)
