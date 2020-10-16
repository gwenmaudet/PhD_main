# 1st prgrm : simulation in non realistic telecom

#generation of sensors
nb_sensors = 1000
theoritical_temperature = 12
var_max_mean = 1 # mean temperature deviation would be between [theoritical_temp - max_var_mean, theoritical_temp + max_var_mean]
var_max_std = 2
min_prct_reception = 20

# constants for grade rate, and cost function
mean_sensor_constant = 1
std_sensor_constant = 1
prct_repection_constant = 0.5

# confidence_interval_subset_constant = 1
# energie_consumption_subset_constant = 1



max_subset_nb = 20


nb_simulation_per_sensor = 100
sensor_file_name = "sensor_caracteristics_storage.json"



# statics
energy_consumed_per_emission = 1




def time_function(t):
    if t < 1000:
        return 20
    else:
        return 22



###########
"""modeling result frome IoT transmission"""
t_alpha = 0.01