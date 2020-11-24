import conf
import sensor_class
import sensor_caracteristic_generation


import json
import random


def create_sensors_and_input_from_all_sensors_for_constant_input():
    sensor_caracteristic_generation.create_sensors_caracteristic_storage(conf.nb_sensors)
    with open(conf.sensor_file_name) as json_file:
        sensors_json = json.load(json_file)

    sensors = sensor_class.sensors()

    for sensor_json in sensors_json:
        new_sensor = sensor_class.sensor(std=sensor_json['std'], prct_reception=sensor_json['prct_reception'],
                                         id=sensor_json['id'], emission_periode=sensor_json['emssion_period'],first_emssion=sensor_json['first_emssion'])
        sensors.add_sensor(new_sensor)


    """beggining of the simulation"""
    for t in range(0, conf.time_of_exp):
        temp = conf.theoritical_temperature
        sensors.get_response_from_gate_at_instant_t(t, temp)
    sensors.write_in_a_json_file_the_sensor_responses()



def simulation_with_constant_input(nb_sensors):

    with open(conf.sensor_with_reception_file_name) as json_file:
        sensors_receptions  = json.load(json_file)
    sensors_receptions = random.sample(sensors_receptions, nb_sensors)
    """creation of the sensors in the related classes"""
    sensors_responses = {}
    sensors = sensor_class.sensors()
    for reception in sensors_receptions:
        new_sensor = sensor_class.sensor(std=reception['std'], receptions=reception['receptions'], id=reception['id'])
        sensors.add_sensor(new_sensor)


    """beggining of the simulation"""
    input = [conf.theoritical_temperature] * conf.time_of_exp
    model = [None] * conf.time_of_exp
    for t in range (0, len(input)):
        temp = input[t]
        value_modelised = sensors.get_response_from_gate_at_instant_t(t, temp)
        model[t] = value_modelised

    to_print = "\\addplot coordinates{"
    for t in range(0, len(input)):
        to_print += ' (' + str(t) + ', ' + str(input[t]) + ') '
    to_print += ' };'
    #print(to_print)

    to_print = "\\addplot+[error bars/.cd,y dir=both,y explicit]coordinates{"
    for t in range(0, 100):
        if model[t] is not None:
            to_print += "(" + str(t) + ',' + str(round(model[t], 3)) + ')+-(0,' + str(round(conf.delta_theta, 3)) + ') '
    to_print += ' };'
    print(to_print)


if __name__ == "__main__":
    create_sensors_and_input_from_all_sensors_for_constant_input()
    # simulation_with_constant_input(100)