import pandas as pd
import matplotlib.pyplot as plt

from tool_box import *

counter = [22222352, 22222348]  # [armoire cataphorese, armoire compresseurs]






def plot_measures_of_one_day_of_one_counter(year, month, day, counter):
    data = extract_counter_informations_from_csv_file(r'cvs_files/sous_compteur_electrique_data.csv')
    measures_of_the_day = []
    for inf in data: # fill a list with the value of the day, and the value sensing the counter 'counter'
        if inf['date'][0:10] == int_in_date_type(year) \
                + "-" + int_in_date_type(month) \
                + "-" + int_in_date_type(day) \
                and inf['counter_type'] == str(counter):
            measures_of_the_day.append(inf)
    measures_of_the_day = process_insert_sorting(measures_of_the_day)

    cons_stamp = measures_of_the_day[0]['value']

    ##handling of the border effect
    j = 0
    has_changed = False
    while has_changed is False:
        j += 1
        if measures_of_the_day[j]['value'] != cons_stamp:
            has_changed = True
    cons_stamp = measures_of_the_day[j]['value']
    time_stamp = convert_time_in_hours(measures_of_the_day[j]['date'])

    # begginning of the calculation of the point for visualisation
    time = []
    consumption = []
    for i in range(j, len(measures_of_the_day)):
        if measures_of_the_day[i][
            'value'] != cons_stamp:  # if the measure at time i is the same as i-1, then it means that there were a loss of packet
            time_in_hour = convert_time_in_hours(measures_of_the_day[i]['date'])
            time.append(time_in_hour)
            electrical_charge = (measures_of_the_day[i]['value'] - cons_stamp) / (time_in_hour - time_stamp)
            consumption.append(electrical_charge)
            # need to do a time stamp to compare the consumption before 2 temporal data in order to compute the consumptions
            time_stamp = time_in_hour
            cons_stamp = measures_of_the_day[i]['value']
    plt.plot(time, consumption, label='consumption of counter ' + str(counter))
    plt.title(
        'eletrical consumption of day ' + int_in_date_type(day) + '-' + int_in_date_type(
            month)
        + '-' + int_in_date_type(year) + ' for counter ' + str(counter))
    plt.xlim(0, 24)
    plt.ylim(0, 400)
    plt.show()


if __name__ == "__main__":
    plot_measures_of_one_day_of_one_counter(2021, 5, 13, counter[1])
