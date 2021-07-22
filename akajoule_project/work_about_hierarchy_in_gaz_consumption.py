from green_wall import generic_tools
import pandas as pd
import matplotlib.pyplot as plt


from tool_box import *
general_counter = ["GENERAL PEINTURE", "GENERAL CATAPHORESE"]  # [general peinture, general cataphorese
subsouncters = [["AEROTHERMES", "RETOUCHES", "GDFA100", "GDFA300", "GDFA400", "ETUVE 80°C PRINCIPALE",
                 "ETUVE 180°C RALLONGE PRINCIPALE", "ETUVE 80°C RALLONGE", "ETUVE 180°C RALLONGE"],
                ["CHAUDIERE CATAPHORESE", "ETUVE 1", "ETUVE 2"],
                ["SOUS LE PORCHE"]]  # [general peinture subcounter],[general cataphorese subcounters],[temperature]]

"""
information about the csv file 'sur_1_semaine' : 

from 12 05 2021 to 20 05 2021

information about the cvs 'sur_1_mois':

from 20 04 2021 to 20 05 2021
"""

# file_extension_name = 'semaine'
# file_extension_name = 'an'
file_extension_name = 'mois'


def extract_principal_counter_information_from_csv_file():
    df = pd.read_csv(r'cvs_files/compteurs_generaux_sur_1_' + file_extension_name + '.csv')
    df = df.to_numpy()
    output_consumption = []
    for data in df:
        stamp = data[0].split(';')
        if stamp[12] in general_counter:
            important_information_dic = {}
            important_information_dic['date'] = stamp[7]  # year, month, day, hour, minute
            important_information_dic['counter_type'] = stamp[12]
            important_information_dic['value'] = int(stamp[9])
            output_consumption.append(important_information_dic)

    return output_consumption


def extract_subcounter_informations_from_csv_file():
    df = pd.read_csv(r'cvs_files/sous_compteur_gaz_sur_1_' + file_extension_name + '.csv')
    df = df.to_numpy()
    output_consumption = []
    for data in df:
        stamp = data[0].split(';')
        if stamp[12] in subsouncters[0]:
            important_information_dic = {}
            important_information_dic['date'] = stamp[7]  # year, month, day, hour, minute
            important_information_dic["counter_type"] = general_counter[0]
            important_information_dic['subcounter_type'] = stamp[12]
            important_information_dic['value'] = int(stamp[9])
            output_consumption.append(important_information_dic)
        elif stamp[12] in subsouncters[1]:
            important_information_dic = {}
            important_information_dic['date'] = stamp[7]  # year, month, day, hour, minute
            important_information_dic["counter_type"] = general_counter[1]
            important_information_dic['subcounter_type'] = stamp[12]
            important_information_dic['value'] = int(stamp[9])
            output_consumption.append(important_information_dic)
        elif stamp[12] in subsouncters[2]:
            important_information_dic = {}
            important_information_dic['date'] = stamp[7]  # year, month, day, hour, minute
            important_information_dic["counter_type"] = 0
            important_information_dic['subcounter_type'] = stamp[12]
            important_information_dic['value'] = int(stamp[9])
            output_consumption.append(important_information_dic)
        else:
            a = 0
            print(data[0])
    return output_consumption

def get_measures_of_a_counter_over_few_days(begin_date, end_date, counter, subcounter=None):
    date = begin_date
    measurements = get_measures_of_a_counter_over_a_day(date[0], date[1], date[2], counter, subcounter)
    while list(date) != list(end_date):
        date = generic_tools.the_day_after(date[0], date[1], date[2])
        measurements = measurements + get_measures_of_a_counter_over_a_day(date[0], date[1], date[2], counter, subcounter)
    return measurements

def get_measures_of_a_counter_over_a_day(day, month, year, counter, subcounter=None):
    measurement_of_the_day = []
    if subcounter is None:
        general_counter_data = extract_principal_counter_information_from_csv_file()

        for inf in general_counter_data:  # fill a list with the value of the day, and the value sensing the counter 'counter'

            if inf['date'][0:10] == generic_tools.int_in_date_type(year) \
                    + "-" + generic_tools.int_in_date_type(month) \
                    + "-" + generic_tools.int_in_date_type(day) \
                    and inf['counter_type'] == counter:

                    measurement_of_the_day.append(inf)
                    stamp = inf['value']

        measurement_of_the_day = generic_tools.process_insert_sorting(
            measurement_of_the_day)
    else:
        subcounter_data = extract_subcounter_informations_from_csv_file()
        for inf in subcounter_data:  # fill a list with the value of the day, and the value sensing the counter 'counter'
            if inf['date'][0:10] == generic_tools.int_in_date_type(year) \
                    + "-" + generic_tools.int_in_date_type(month) \
                    + "-" + generic_tools.int_in_date_type(day) \
                    and inf['counter_type'] == counter \
                    and inf["subcounter_type"] == subcounter:
                measurement_of_the_day.append(inf)
        measurement_of_the_day = generic_tools.process_insert_sorting(measurement_of_the_day)
    stamp = 0
    measurement_without_redundancy = []
    for measure in measurement_of_the_day:
        if generic_tools.convert_time_in_hours(measure['date']) < 6 or generic_tools.convert_time_in_hours(
                measure['date']) > 17 or measure['value'] != stamp:
            measurement_without_redundancy.append(measure)
            stamp = measure['value']
    return measurement_of_the_day


def compute_the_gaz_consumption_of_a_counter_over_a_day(day, month, year, counter, subcounter=None):
    measurement_of_the_day = get_measures_of_a_counter_over_a_day(day, month, year, counter, subcounter)
    if len(measurement_of_the_day) == 0:
        print(day, month, year, counter, subcounter)
    return measurement_of_the_day[-1]['value'] - measurement_of_the_day[0]["value"]


def daily_graph_comparasion_subcounter_and_counters(counter_index, begin_date, end_date):
    counter_daily_consumptions = []
    subcounter_sum_daily_consumptions = []
    i = 0
    x_abcsissa = [i]

    date = end_date
    counter_daily_consumptions.append(
        compute_the_gaz_consumption_of_a_counter_over_a_day(date[0], date[1], date[2], general_counter[counter_index]))
    subcounter_consumption_of_the_day = 0
    for subcounter_id in subsouncters[counter_index]:
        subcounter_consumption_of_the_day += compute_the_gaz_consumption_of_a_counter_over_a_day(date[0], date[1],
                                                                                                 date[2],
                                                                                                 general_counter[
                                                                                                     counter_index],
                                                                                                 subcounter_id)
    subcounter_sum_daily_consumptions.append(subcounter_consumption_of_the_day)

    while list(date) != begin_date:
        date = generic_tools.the_day_before(date[0], date[1], date[2])

        counter_daily_consumptions.append(compute_the_gaz_consumption_of_a_counter_over_a_day(date[0], date[1], date[2],
                                                                                              general_counter[
                                                                                                  counter_index]))
        subcounter_consumption_of_the_day = 0
        for subcounter_id in subsouncters[counter_index]:
            subcounter_consumption_of_the_day += compute_the_gaz_consumption_of_a_counter_over_a_day(date[0], date[1],
                                                                                                     date[2],
                                                                                                     general_counter[
                                                                                                         counter_index],
                                                                                                     subcounter_id)
        subcounter_sum_daily_consumptions.append(subcounter_consumption_of_the_day)
        i += 1
        x_abcsissa.append(i)
    counter_daily_consumptions.reverse()
    subcounter_sum_daily_consumptions.reverse()
    plt.plot(x_abcsissa, counter_daily_consumptions, label="consumption of the main counter")
    plt.plot(x_abcsissa, subcounter_sum_daily_consumptions, label="sum of the consumption of the subsounters")
    plt.legend()
    plt.show()


def plot_of_days_comparison_hour_by_hour(counter_index, begin_date, end_date):
    general_consumption_x_index = []
    general_consumption_y_index = []
    measurements_of_the_day = get_measures_of_a_counter_over_few_days(begin_date, end_date, general_counter[counter_index])
    for i in range(1, len(measurements_of_the_day)):
        general_consumption_x_index.append(measurements_of_the_day[i]['date'])
        general_consumption_y_index.append(measurements_of_the_day[i]['value'] - measurements_of_the_day[i - 1]['value'])

    subcounters_consumption_y_index = [0 for i in range(len(general_consumption_x_index))]
    for subcounter_id in subsouncters[counter_index]:
        measurements_of_the_day = get_measures_of_a_counter_over_few_days(begin_date, end_date, general_counter[counter_index],  subcounter_id)
        for i in range(1, len(measurements_of_the_day)):
            subcounters_consumption_y_index[i-1] += measurements_of_the_day[i]['value'] - measurements_of_the_day[i - 1][
                'value']
    plt.plot(general_consumption_x_index, general_consumption_y_index, label="general counter measure of the day")
    plt.plot(general_consumption_x_index, subcounters_consumption_y_index, label="subcounter sum of the day")
    plt.legend()
    #plt.title('day : ' + str(date[0]) + '-' + str(date[1]) + '-' + str(date[2]) + ' for counter ' + general_counter[counter_index])
    plt.show()


def plot_modified_representation_of_data_for_the_day(counter_index, begin_date, end_date):
    general_counter_measures = get_measures_of_a_counter_over_few_days(begin_date, end_date, general_counter[counter_index])
    subcounters_measures = []
    for subcounter_id in subsouncters[counter_index]:
        subcounters_measures.append(get_measures_of_a_counter_over_few_days(begin_date, end_date, general_counter[counter_index], subcounter=subcounter_id))
    i = 1
    print(len(general_counter_measures))
    stamp = general_counter_measures[0]['value']
    modified_plot = []
    original_plot = []
    x_abscissa = []
    while i < len(general_counter_measures):
        x_abscissa.append(general_counter_measures[i]['date'])
        original_plot.append(general_counter_measures[i]['value'] - general_counter_measures[i - 1]['value'] )
        if general_counter_measures[i]['value'] != stamp:
            modified_plot.append(general_counter_measures[i]['value'] - stamp)
            stamp = general_counter_measures[i]['value']
        else:
            has_a_reception = False
            j = i
            while has_a_reception is False and j<len(general_counter_measures)-1:
                j +=1
                if general_counter_measures[j]['value']!= stamp:
                    has_a_reception = True
            subcounter_reception_in_undetermined_time = []
            total_sum = 0
            for k in range(i, j+1):
                sum = 0
                for subcounter_measure in subcounters_measures:
                    sum += subcounter_measure[k]['value'] - subcounter_measure[k-1]['value']
                subcounter_reception_in_undetermined_time.append(sum)
                total_sum += sum
                if k != i:
                    x_abscissa.append(general_counter_measures[k]['date'])
                    original_plot.append(general_counter_measures[k]['value'] - stamp)
            if total_sum == 0:
                for k in range(i, j+1):
                    modified_plot.append(0)
            else:
                proportion = []
                for elt in subcounter_reception_in_undetermined_time:
                    proportion.append(elt / total_sum)
                total_shift = general_counter_measures[j]['value'] - general_counter_measures[i]['value']
                for prop in proportion:
                    modified_plot.append(total_shift * prop)
            stamp = general_counter_measures[j]['value']
            i = j
        i += 1
    subcounter_plot = [0 for i in range (len(subcounters_measures[0]))]
    for elt in subcounters_measures:
        for i in range(1, len(elt)):
            subcounter_plot[i] += elt[i]['value'] - elt[i-1]['value']
    del subcounter_plot[0]
    print(len(subcounter_plot))
    #plt.plot(x_abscissa, original_plot, label= 'original')
    plt.plot(x_abscissa, modified_plot, label = 'modified')
    plt.plot(x_abscissa, subcounter_plot, label='subcounter sum')
    plt.legend()
    plt.show()


def plot_gaz_quantity_consummed(counter_index, begin_date, end_date):
    general_counter_measures = get_measures_of_a_counter_over_few_days(begin_date, end_date,
                                                                       general_counter[counter_index])
    subcounters_measures = []
    for subcounter_id in subsouncters[counter_index]:
        measure = get_measures_of_a_counter_over_few_days(begin_date, end_date, general_counter[counter_index],
                                                          subcounter=subcounter_id)
        subcounters_measures.append(measure)
    general_init = general_counter_measures[0]['value']
    subcounters_init = [measure[0]['value'] for measure in subcounters_measures]
    x_general = [0]
    y_general = [0]
    x_subcounters = [0]
    y_subsounters = [0]

    for i in range(1, len(general_counter_measures)):
        x_general.append(i)
        y_general.append(general_counter_measures[i]['value'] - general_init)
        subcounter_sum = 0
        for init, measure in zip(subcounters_init, subcounters_measures):
            subcounter_sum += measure[i]['value'] - init
        x_subcounters.append(i)
        y_subsounters.append(subcounter_sum)
    plt.plot(x_general, y_general, label="general")
    plt.plot(x_subcounters, y_subsounters, label="subcounters")
    plt.legend()
    plt.show()

def plot_modified_gaz_quantity_consummed(counter_index, begin_date, end_date):
    general_counter_measures = get_measures_of_a_counter_over_few_days(begin_date, end_date, general_counter[counter_index])
    subcounters_measures = []
    for subcounter_id in subsouncters[counter_index]:
        measure = get_measures_of_a_counter_over_few_days(begin_date, end_date, general_counter[counter_index], subcounter=subcounter_id)
        subcounters_measures.append(measure)
    general_init = general_counter_measures[0]['value']
    subcounters_init = [measure[0]['value'] for measure in subcounters_measures]
    x_general = [0]
    y_general = [0]
    x_subcounters = [0]
    y_subsounters = [0]

    for i in range(1, len(general_counter_measures)):
        if (general_counter_measures[i]['value']- general_init) != y_general[-1]:
            x_general.append(i)
            y_general.append(general_counter_measures[i]['value'] - general_init)
        subcounter_sum = 0
        for init, measure in zip(subcounters_init, subcounters_measures):
            subcounter_sum += measure[i]['value'] - init
        if subcounter_sum != y_subsounters[-1]:
            x_subcounters.append(i)
            y_subsounters.append(subcounter_sum)
    plt.plot(x_general,y_general, label="general")
    plt.plot(x_subcounters,y_subsounters, label="subcounters")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot_of_days_comparison_hour_by_hour(1, [4, 5, 2021], [7, 5, 2021])
    daily_graph_comparasion_subcounter_and_counters(1, [4, 5, 2021], [7, 5, 2021])

    plot_gaz_quantity_consummed(1, [4, 5, 2021], [7, 5, 2021])
    plot_modified_gaz_quantity_consummed(1, [4, 5, 2021], [7, 5, 2021])
    plot_modified_representation_of_data_for_the_day(1, [4, 5, 2021], [7, 5, 2021])
