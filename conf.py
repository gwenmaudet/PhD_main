# 1st prgrm : simulation in non realistic telecom

#generation of sensors
nb_sensors = 2000


def theoritical_temperature(t):
    if t % 200 < 100:
        return 15
    else:
        return 10

var_max_mean = 0 # mean temperature deviation would be between [theoritical_temp - max_var_mean, theoritical_temp + max_var_mean]
var_max_std = 2
min_prct_reception = 0.2
sensor_emission_period = 50

time_of_exp = 500


#FILE NAMES
sensor_file_name = "json_files\sensor_caracteristics_storage.json"
sensor_with_reception_file_name = "json_files\sensor_with_reception.json"



"""real_time_temperature_modelisation"""

quantille_gauss = 2.576 #representing quantille of gaussian for 99%
t_test_percentage = 0.995
delta_theta = 0.5 # the degre precision for the value measured [theta +- delta_theta]


"""experiment"""
sensor_sample = [1000, 500, 250, 100]
nb_of_iteration = 10

consuption_for_one_sensor = 1

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
