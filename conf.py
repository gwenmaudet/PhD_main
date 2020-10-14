# 1st prgrm : simulation in non realistic telecom


# confidence_interval_subset_constant = 1
# energie_consumption_subset_constant = 1



max_subset_nb = 30



sensor_file_name = "sensor_caracteristics_storage.json"



# statics
energy_consumed_per_emission = 1


time_of_experiment = 200
nb_simulation_per_experiment = 200



################################################
"""modelisation of the sensor """
var__mean_dif = 1
var_max_std = 2
min_prct_reception = 20

nb_sensors = 1000


# temporal function in minute, we suppose the function aplly from the beggining to the end of the experiment
def temporal_fct_to_folow(t):
    return 10 * t


#####################################################
"""informaton about evaluation of sensors"""

sensor_evaluation = 'Dynamic_time_warping'

#Dynamic_time_warping
dist = 'euclidean'
wrap = 1




