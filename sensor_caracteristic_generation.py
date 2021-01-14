import os
import conf
import random
import json


def create_sensors_caracteristic_storage(nb_sensors):
    if os.path.isfile(conf.sensor_file_name):
        os.remove(conf.sensor_file_name)
        #print("SENSOR FILE REMOVED !")
    json_file = []
    for i in range (nb_sensors):
        std = random.uniform(0, conf.var_max_std)
        prct_reception = random.uniform(conf.min_prct_reception, 1)
        json_file.append({'id': i,'std': std, 'prct_reception': prct_reception, 'emssion_period': conf.sensor_emission_period, 'first_emssion': i % conf.sensor_emission_period})
    with open(conf.sensor_file_name, 'w+') as outfile:
        json.dump(json_file, outfile, indent=4)
    #print('NEW SENSOR FILE OVERWRITED !')


def create_sensors_caracteristic_storage_for_sigma_constant_distribution(nb_sensors,sigmin,sigmax, emission_period=conf.sensor_emission_period):
    if os.path.isfile(conf.sensor_file_name):
        os.remove(conf.sensor_file_name)
        #print("SENSOR FILE REMOVED !")
    json_file = []
    for i in range(nb_sensors):
        std = sigmin + i * (sigmax - sigmin) / (nb_sensors)
        prct_reception = 1
        json_file.append({'id': i, 'std': std, 'prct_reception': prct_reception, 'emssion_period': emission_period, 'first_emssion': i % conf.sensor_emission_period})
    with open(conf.sensor_file_name, 'w+') as outfile:
        json.dump(json_file, outfile, indent=4)
    #print('NEW SENSOR FILE OVERWRITED !')



if __name__ == "__main__":
    create_sensors_caracteristic_storage()