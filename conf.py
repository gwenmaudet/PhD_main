# 1st prgrm : simulation in non realistic telecom

#generation of sensors
nb_sensors = 5
theoritical_temperature = 12
var_max_mean = 0 # mean temperature deviation would be between [theoritical_temp - max_var_mean, theoritical_temp + max_var_mean]
var_max_std = 2
min_prct_reception = 0.2

sensor_emission_period = 2



#FILE NAMES
sensor_file_name = "json_files\sensor_caracteristics_storage.json"
sensor_with_reception_file_name = "json_files\sensor_with_reception.json"



"""real_time_temperature_modelisation"""
time_of_exp = 10
quantille_gauss = 2.326 #representing quantille of gaussian for 99%
quantille_student = [31.82,  6.965, 4.541,  3.747,  3.365, 3.143,  2.998, 2.896,  2.821, 2.764,
                      2.718, 2.681,  2.650, 2.624, 2.602,  2.583,  2.567,  2.552,  2.539,  2.528,
                      2.518, 2.508, 2.500, 2.492, 2.485,  2.479,  2.473, 2.467,  2.462, 2.457]

delta_theta = 0.5 # the degre precision for the value measured [theta +- delta_theta]



###########
"""modeling result frome IoT transmission"""
t_alpha = 0.01



"""
                ----OLD----
"""

# constants for grade rate, and cost function
mean_sensor_constant = 1
std_sensor_constant = 1
prct_repection_constant = 0.5


# confidence_interval_subset_constant = 1
# energie_consumption_subset_constant = 1



max_subset_nb = 20



nb_simulation_per_sensor = 100

# statics
energy_consumed_per_emission = 1

def time_function(t):
    if t < 1000:
        return 20
    else:
        return 22
