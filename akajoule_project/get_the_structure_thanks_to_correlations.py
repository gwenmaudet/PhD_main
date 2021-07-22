import json
from scipy import stats
import numpy as np


file_extension_name = 'an'


general_gaz_counter = ["GENERAL PEINTURE", "GENERAL CATAPHORESE"]

gaz_subcounters = [["AEROTHERMES", "RETOUCHES", "GDFA100", "GDFA300", "GDFA400", "ETUVE 80°C PRINCIPALE",
                    "ETUVE 180°C RALLONGE PRINCIPALE", "ETUVE 80°C RALLONGE", "ETUVE 180°C RALLONGE"],
                   ["CHAUDIERE CATAPHORESE", "ETUVE 1", "ETUVE 2"]]


def main(counter_index):

    with open('new_files_in_json/sous_compteur_gaz_sur_1_' + file_extension_name + '.txt', 'r+') as json_file:
        subcounters_values = json.load(json_file)
    with open('new_files_in_json/compteurs_generaux_sur_1_' + file_extension_name + '.txt', 'r+') as json_file:
        counters_values = json.load(json_file)


    pearson_correl_coef = {}
    spearman_correl_coef = {}
    x = np.array(counters_values[general_gaz_counter[counter_index]])
    for counter_key in general_gaz_counter:
        for subcounter_key in subcounters_values[counter_key]:
            y = np.array(subcounters_values[counter_key][subcounter_key])
            pearson_correl_coef[subcounter_key],a = stats.pearsonr(x, y)
            spearman_correl_coef[subcounter_key],a = stats.spearmanr(x, y)
    pearson_correl_coef = {k: v for k, v in sorted(pearson_correl_coef.items(), key=lambda item: item[1])}
    spearman_correl_coef = {k: v for k, v in sorted(spearman_correl_coef.items(), key=lambda item: item[1])}

    print(pearson_correl_coef)
    print(spearman_correl_coef)
    return spearman_correl_coef


def main_1():
    results = [main(0),main(1)]
    for sub_counter_index in results[0]:
        print("##############")
        print(sub_counter_index)
        if results[0][sub_counter_index] > results[1][sub_counter_index]:
            print(general_gaz_counter[0])
        else:
            print(general_gaz_counter[1])




if __name__ == "__main__":
    main_1()
