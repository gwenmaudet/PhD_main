from akajoule_project.tool_box import *
from sklearn.decomposition import PCA
import numpy as np
import json
import time
import matplotlib.pyplot as plt

# file_time_extension = ['semaine', 'mois', 'an']
file_time_extension = ['an']

a = 1
general_gaz_counter = ["GENERAL PEINTURE"]
gaz_subcounters = [["AEROTHERMES", "RETOUCHES", "GDFA100", "GDFA300", "GDFA400", "ETUVE 80°C PRINCIPALE",
                    "ETUVE 180°C RALLONGE PRINCIPALE", "ETUVE 80°C RALLONGE", "ETUVE 180°C RALLONGE"]]

general_gaz_counter = ["GENERAL PEINTURE", "GENERAL CATAPHORESE"]

gaz_subcounters = [["AEROTHERMES", "RETOUCHES", "GDFA100", "GDFA300", "GDFA400", "ETUVE 80°C PRINCIPALE",
                    "ETUVE 180°C RALLONGE PRINCIPALE", "ETUVE 80°C RALLONGE", "ETUVE 180°C RALLONGE"],
                   ["CHAUDIERE CATAPHORESE", "ETUVE 1", "ETUVE 2"]]


def clean_sub_counters_files():
    for file_extension_name in file_time_extension:

        subcounters_data = {}
        i = 0
        for subcounter_list in gaz_subcounters:
            subcounters_data[general_gaz_counter[i]] = {}
            for subcounter_name in subcounter_list:
                subcounters_data[general_gaz_counter[i]][
                    subcounter_name] = extract_subcounter_informations_from_csv_file(
                    r'cvs_files/sous_compteur_gaz_sur_1_' + file_extension_name + '.csv', subcounter_name)
                subcounters_data[general_gaz_counter[i]][subcounter_name] = process_insert_sorting(
                    subcounters_data[general_gaz_counter[i]][subcounter_name])
            i += 1
        counters_data = {}
        for counter_name in general_gaz_counter:
            counters_data[counter_name] = extract_counter_informations_from_csv_file(
                r'cvs_files/compteurs_generaux_sur_1_' + file_extension_name + '.csv', counter_name)
            counters_data[counter_name] = process_insert_sorting(counters_data[counter_name])

        counters_cleaned_data = {}
        subcounters_cleaned_data = {}
        for counter_key in general_gaz_counter:
            counters_cleaned_data[counter_key] = []
            subcounters_cleaned_data[counter_key] = {}
            for subcounter_key in subcounters_data[counter_key]:
                subcounters_cleaned_data[counter_key][subcounter_key] = []
        i = 1
        stamp = counters_data[general_gaz_counter[a]][0]['value']
        while i < len(counters_data[counter_key]):
            is_ok = True
            counter_indexes = []
            subcounters_indexes = []
            end_date = counters_data[general_gaz_counter[a]][i]["date"]
            if stamp != counters_data[general_gaz_counter[a]][i]['value']:
                begin_date = get_date_of_last_different_value(counters_data[general_gaz_counter[a]][:i + 1])
                if begin_date is not None:
                    for counter_key in general_gaz_counter:
                        end_index = get_index_of_item_for_precise_time(counters_data[counter_key], end_date)
                        begin_index = get_index_of_item_for_precise_time(counters_data[counter_key], begin_date)

                        if end_index is None and begin_index is None:
                            is_ok = False
                        else:
                            counter_indexes.append([begin_index, end_index])
                            if counters_data[counter_key][end_index]['value'] == \
                                    counters_data[counter_key][begin_index]['value']:
                                is_ok = False
                            for subcounter_key in subcounters_data[counter_key]:
                                end_index = get_index_of_item_for_precise_time(
                                    subcounters_data[counter_key][subcounter_key], end_date)
                                begin_index = get_index_of_item_for_precise_time(
                                    subcounters_data[counter_key][subcounter_key], begin_date)
                                if end_index is None and begin_index is None:
                                    is_ok = False
                                else:
                                    subcounters_indexes.append([begin_index, end_index])
                                    """if subcounters_data[counter_key][subcounter_key][end_index]['value'] == subcounters_data[counter_key][subcounter_key][end_index-1]['value']:
                                        is_ok = False"""
                    if is_ok is True:
                        i_counter = 0
                        i_subcounter = 0
                        for counter_key in general_gaz_counter:
                            consumption = counters_data[counter_key][counter_indexes[i_counter][1]]['value'] - \
                                          counters_data[counter_key][counter_indexes[i_counter][0]]['value']
                            counters_cleaned_data[counter_key].append(consumption)
                            for subcounter_key in subcounters_data[counter_key]:
                                subconsumption = \
                                subcounters_data[counter_key][subcounter_key][subcounters_indexes[i_subcounter][1]][
                                    'value'] - \
                                subcounters_data[counter_key][subcounter_key][subcounters_indexes[i_subcounter][0]][
                                    "value"]
                                subcounters_cleaned_data[counter_key][subcounter_key].append(subconsumption)
                                i_subcounter += 1
                            i_counter += 1
            stamp = counters_data[general_gaz_counter[a]][i]['value']
            i += 1
        subcounter_to_plot = {}
        for counter_key in general_gaz_counter:
            """print("#############################################")
            print(counter_key)
            print(len(counters_cleaned_data[counter_key]))
            print(counters_cleaned_data[counter_key])"""
            input = [i for i in range(len(counters_cleaned_data[counter_key]))]
            subcounter_to_plot[counter_key] = [0] * len(counters_cleaned_data[counter_key])
            for subcounter_key in subcounters_data[counter_key]:
                for i in range(len(subcounters_cleaned_data[counter_key][subcounter_key])):
                    subcounter_to_plot[counter_key][i] += subcounters_cleaned_data[counter_key][subcounter_key][i]
        i = 0
        p = len(counters_cleaned_data[counter_key])
        """for counter_key in general_gaz_counter:
            print("#####################")
            print(len(counters_cleaned_data[counter_key]))
            for subcounter_key in subcounters_data[counter_key]:
                print(len(subcounters_cleaned_data[counter_key][subcounter_key]))"""
        while i < len(counters_cleaned_data[counter_key]):
            to_delete = False
            for counter_key in general_gaz_counter:
                if subcounter_to_plot[counter_key][i] > counters_cleaned_data[counter_key][i]:
                    to_delete = True
            if to_delete:
                """print("#############################################")
                print(i)
                print(counter_key)
                print(len(counters_cleaned_data[counter_key]))
                print(counters_cleaned_data[counter_key])"""
                for counter_key in general_gaz_counter:
                    val = counters_cleaned_data[counter_key].pop(i)
                    val1 = subcounter_to_plot[counter_key].pop(i)
                    if i != len(counters_cleaned_data[counter_key]):
                        counters_cleaned_data[counter_key][i] += val
                        subcounter_to_plot[counter_key][i] += val1
                    for subcounter_key in subcounters_data[counter_key]:
                        val = subcounters_cleaned_data[counter_key][subcounter_key].pop(i)
                        if i != len(subcounters_cleaned_data[counter_key][subcounter_key]):
                            subcounters_cleaned_data[counter_key][subcounter_key][i] += val
            else:
                i += 1
            p = len(counters_cleaned_data[counter_key])
            """
                        print(subcounter_key)
                        print(len(subcounters_cleaned_data[counter_key][subcounter_key]))
                        print(subcounters_cleaned_data[counter_key][subcounter_key])"""
        input = [i for i in range(0, len(counters_cleaned_data[counter_key]))]


        for counter_key in general_gaz_counter:
            for subcounter_key in subcounters_data[counter_key]:
                time.sleep(1)
                plt.scatter(counters_cleaned_data[counter_key], subcounters_cleaned_data[counter_key][subcounter_key], label='counter')
                plt.legend()
                plt.show()
        """
        for counter_key in general_gaz_counter:
            
            plt.plot(input,counters_cleaned_data[counter_key], label='counter')
            plt.plot(input, subcounter_to_plot[counter_key], label='subcounter')
            plt.legend()
            plt.show()"""

        with open('new_files_in_json/compteurs_generaux_sur_1_' + file_extension_name + '.txt', 'w+') as outfile:
            json.dump(counters_cleaned_data, outfile, indent=4)

        with open('new_files_in_json/sous_compteur_gaz_sur_1_' + file_extension_name + '.txt', 'w+') as outfile:
            json.dump(subcounters_cleaned_data, outfile, indent=4)


if __name__ == "__main__":
    clean_sub_counters_files()
