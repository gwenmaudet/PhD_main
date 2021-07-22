import json
from scipy import stats
import numpy as np


file_extension_name = 'mois'


general_gaz_counter = ["GENERAL PEINTURE", "GENERAL CATAPHORESE"]

gaz_subcounters = [["AEROTHERMES", "RETOUCHES", "GDFA100", "GDFA300", "GDFA400", "ETUVE 80°C PRINCIPALE",
                    "ETUVE 180°C RALLONGE PRINCIPALE", "ETUVE 80°C RALLONGE", "ETUVE 180°C RALLONGE"],
                   ["CHAUDIERE CATAPHORESE", "ETUVE 1", "ETUVE 2"]]


def get_the_most_discriminant_index_using_minimum_number_of_ejected_values(counters_dics, subcounters_dics):
    best_candidate = [0,0]
    for i in range(len(counters_dics[general_gaz_counter[0]])):
        sub_elt = []
        sum_subs = 0
        counter_elt = []
        for counter_index in general_gaz_counter:
            counter_elt.append(counters_dics[counter_index][i])
            for subcounter_index in subcounters_dics[counter_index]:
                sub_elt.append(subcounters_dics[counter_index][subcounter_index])
                sum_subs += subcounters_dics[counter_index][subcounter_index]
        sub_elt = sorted(sub_elt) #necessarly in the worst case only the bigger element are being excluded
        counter_that_give_the_decision = sorted(counter_elt)[0] #the constraint is applied on the smallest counter_elt
        sub_is_less_than_counter_elt = False
        discrimant = 0
        while sub_is_less_than_counter_elt is False:
            if sum_subs < counter_that_give_the_decision:
                sub_is_less_than_counter_elt = True
            else:
                discrimant += 1
                elt = sub_elt.pop(-1)
                sum_subs -= elt #remoove the elt from the solution in order to know what will be the minimum
        if discrimant > best_candidate[1]:
            best_candidate = [i, discrimant]



def get_the_most_discriminant_index_using_maximum_number_of_rejected_values(counters_dics, subcounters_dics):
    best_candidate = [0, 0]
    for i in range(len(counters_dics[general_gaz_counter[0]])):
        sub_elt = []
        sum_subs = 0
        counter_elt = []
        for counter_index in general_gaz_counter:
            counter_elt.append(counters_dics[counter_index][i])
            for subcounter_index in subcounters_dics[counter_index]:
                sub_elt.append(subcounters_dics[counter_index][subcounter_index])
                sum_subs += subcounters_dics[counter_index][subcounter_index]
        sub_elt = sorted(sub_elt)  # necessarly in the best case only the smaller element are being excluded, in order to fasten the number
        counter_that_give_the_decision = sorted(counter_elt)[0]  # the constraint is applied on the smallest counter_elt
        sub_is_less_than_counter_elt = False
        discrimant = 0
        while sub_is_less_than_counter_elt is False:
            if sum_subs < counter_that_give_the_decision:
                sub_is_less_than_counter_elt = True
            else:
                discrimant += 1
                elt = sub_elt.pop()
                sum_subs -= elt  # remoove the elt from the solution in order to know what will be the minimum
        if discrimant > best_candidate[1]:
            best_candidate = [i, discrimant]


def main():

    with open('new_files_in_json/sous_compteur_gaz_sur_1_' + file_extension_name + '.txt', 'r+') as json_file:
        subcounters_dics = json.load(json_file)
    with open('new_files_in_json/compteurs_generaux_sur_1_' + file_extension_name + '.txt', 'r+') as json_file:
        counters_dics = json.load(json_file)







if __name__ == "__main__":
    main(0)
