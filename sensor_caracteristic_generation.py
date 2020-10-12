import os
import conf
import random
import json


def create_sensors_caracteristic_storage():
    if os.path.isfile(conf.sensor_file_name):
        os.remove(conf.sensor_file_name)
        print("FILE REMOVED !")
    json_file = []
    for i in range (conf.nb_sensors):
        mean = random.uniform(conf.theoritical_temperature - conf.var_max_mean, conf.theoritical_temperature + conf.var_max_mean)
        std = random.uniform(0, conf.var_max_std)
        json_file.append({'id': i,'mean': mean, 'std': std})
    with open(conf.sensor_file_name, 'w+') as outfile:
        json.dump(json_file, outfile)
    print('NEW FILE OVERWRITED !')


if __name__ == "__main__":
    create_sensors_caracteristic_storage()