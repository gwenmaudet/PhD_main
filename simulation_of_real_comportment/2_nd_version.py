import random
import statistics
import matplotlib.pyplot as plt
import numpy as np
from math import log, ceil

import conf

event = []
elm = 0
M = 1


"""
TOOLBOX
"""

def insert_event(elm):
    global event

    for i in range(len(event)):
        if event[i].wake_up > elm.wake_up:
            event.insert(i, elm)
            return

    # last element
    event.append(elm)

def update_end_of_devices(new_death):
    global end_of_devices
    index_to_delete = None
    for i in range(len(end_of_devices)):
        if end_of_devices[i][0] == new_death[0]:
            if end_of_devices[i][1] == new_death[1]:
                return
            else:
                index_to_delete = i
    if index_to_delete is not None:
        del end_of_devices[index_to_delete]

    for i in range (len(end_of_devices)):
        if end_of_devices[i][1]> new_death[1]:
            end_of_devices.insert(i, new_death)
            return
    end_of_devices.append(new_death)

def is_in_end_of_devices(name):
    global end_of_devices
    for elt in end_of_devices:
        if elt[0] == name:
            return True
    return False

"""
sensor class for initialisation of sensors, and management of their comportment
"""
class sensor:
    def __init__(self, period=conf.p_0, error=None, err_args=None, name="sensor",
                 battery=conf.C, fst_wake_up=0, time_out_of_scope=None):
        global elm
        self.period = period
        self.battery = battery
        self.name = "{}_{:04}".format(name, elm)
        elm += 1
        self.expected_next_emission = None
        self.need_one_changing_of_period = False
        self.time_out_of_scope = time_out_of_scope
        self.is_out_of_scope = False
        self.wake_up = fst_wake_up + random.uniform(0, self.period)
        self.fst_emission = self.wake_up
        insert_event(self)

    def sleep(self, simul_time):
        if self.time_out_of_scope is not None and simul_time + self.period > self.time_out_of_scope:
            self.is_out_of_scope = True
        if self.battery < conf.c_e:  # when battery is empty
            return False
        # self.wake_up = simul_time + random.uniform(0, self.period)
        self.wake_up = simul_time + self.period
        insert_event(self)
        return True

    def draw(self):
        if self.is_out_of_scope is False:
            self.battery -= conf.c_e
            return 0 #self.value
        #else:
        #    return None  ##meaning that the sensor has been taken out of the environment

    def set_period(self, period):
        p = random.random()
        if p < 1:
            self.period = period
            self.battery -= conf.c_r


"""
View of a sensor from the gateway
"""
class sensor_view:
    def __init__(self, sensor):
        self.name = sensor.name
        self.period = sensor.period
        self.battery = sensor.battery
        self.expected_next_emission = sensor.expected_next_emission


"""
information system knowledge
"""
class information_system:
    def __init__(self):
        self.sensor_view_list = {}

    def update(self, sensor):
        self.sensor_view_list[sensor.name] = [sensor_view(sensor)]

    def remove(self,sensor):
        if sensor.name in self.sensor_view_list:
            del self.sensor_view_list[sensor.name]

    def is_in(self,sensor):
        if sensor.name in self.sensor_view_list:
            return True
        else:
            return False

    def length(self):
        return len(self.sensor_view_list)




"""
Initialisation of the sensors
"""
def initialisation_of_sensors(fixed_arrival=False):
    ##initialisation of the sensors : case where there are sensors that are tken off, and other that arrive afteward
    names = []
    stopping_times = {}
    begginning_times = {}
    # print("sensor startin from the begginning finishing early")
    global event
    if fixed_arrival is False:
        for i in range(conf.n):
            begginning = random.uniform(0, (conf.C - conf.c_r) // conf.c_e * conf.tau)
            s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2), fst_wake_up=begginning)
            names.append(s.name)
    else:
        t_i = 0
        for i in range(conf.n):
            begginning = random.uniform(t_i + conf.tau * (i + 2),
                                        t_i + conf.tau * (i + 2))
            # s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2))
            s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2), fst_wake_up=begginning)
            t_i = s.fst_emission

            # print(s.name)
            # print(end)
            names.append(s.name)
            # stopping_times[s.name] = end
            begginning_times[s.name] = s.fst_emission
    return names, event



"""
General monitoring of sensor emission, taking initial sensor emissions, and an algorithm of emission management
"""
def monitoring_of_sensor_emissions(management_function, event_stamp, sensor_names):
    global event
    #global sensor_view_list
    event = event_stamp
    simul_time = 0
    dt = []
    emission_time_per_sensor = {}
    changed_period = {}
    initial_time = 0
    for name in sensor_names:
        emission_time_per_sensor[name] = []
        changed_period[name] = []


    management_function(None, 0)
    while len(event) != 0:
        evt = event.pop(0)
        assert (evt.wake_up >= simul_time)
        delta_t = evt.wake_up - simul_time
        if initial_time == 0:
            initial_time = simul_time
        sensor_value = evt.draw()
        simul_time = evt.wake_up
        view = sensor_view(evt)
        new_period = management_function(view, simul_time) ######## use of the management function
        if sensor_value is not None:  # le message recu n'indique pas que le capteur est passé en dehors de l'environnement
            dt.append(delta_t)
            emission_time_per_sensor[evt.name].append(simul_time)
            if new_period is not None and evt.battery >= conf.c_r:
                evt.set_period(new_period)
                changed_period[evt.name].append(simul_time)
            evt.expected_next_emission = simul_time + evt.period
            #bool = evt.sleep(simul_time)
            #if bool is False:
            #    sensor_view_list.remove(evt)
        #else:
        #    sensor_view_list.remove(evt)

    return simul_time, dt, emission_time_per_sensor, changed_period, initial_time



"""
Function that takes a number of active sensor M, and propose a solution that cycle all avor the time M sensor one after the other
"""
t_0 = 0
end_of_devices = []
def cycling_over_M(evt, simul_time):
    global M
    global t_0
    global end_of_devices
    global sensor_view_list
    new_period = None
    if evt is None:
        sensor_view_list = information_system()
        t_0 = 0
        end_of_devices = []
    else:
        if sensor_view_list.is_in(evt) is False: # first emission of the sensor
            sensor_view_list.update(evt)
            if sensor_view_list.length() <= M: # it will directly be included in the cycle
                if sensor_view_list.length() == 1:
                    t_0 = simul_time
                    new_period = conf.tau
                else:
                    new_period = conf.tau - (
                            simul_time - t_0) % conf.tau + (
                                         sensor_view_list.length() - 1) * conf.tau
            else:#it would switch of just after the death of the next sensor, with a period of tau
                beggining_of_this_sensor = end_of_devices.pop(0)
                new_period = beggining_of_this_sensor[1] - simul_time
                time_for_changing_of_the_sensor = beggining_of_this_sensor[1] + (
                                (evt.battery - 2 * conf.c_r) // conf.c_e + 1) * conf.tau * M
        else:
            sensor_view_list.update(evt)
            if evt.period != min(sensor_view_list.length(), M) * conf.tau:
                new_period = min(sensor_view_list.length(), M) * conf.tau
                if evt.battery < conf.c_e + conf.c_r:
                    sensor_view_list.remove(evt)
            else:
                if evt.battery < conf.c_e:
                    sensor_view_list.remove(evt)

        #updating of end_of_device
        #sensor that have changed their period to M\tau or that didn't chang their period but will do at next emission : one change of period
        sensor_death = None
        if new_period == M * conf.tau :
            sensor_death = simul_time + ((evt.battery - conf.c_r)//conf.c_e +1) * conf.tau * M
        elif new_period is None and evt.period != M * conf.tau :
            sensor_death = simul_time + evt.period +((evt.battery - conf.c_r - conf.c_e)//conf.c_e +1) * conf.tau * M
        #sensor have changed it period but would need to change a second time to be really scheduled : 2 change of period
        elif new_period is not None and new_period != M * conf.tau :
            sensor_death = simul_time + new_period + ((evt.battery - 2 * conf.c_r - conf.c_e) // conf.c_e + 1) * conf.tau * M
        #if sensor_death is None : pas de changement de periode et deja la période finale : M * \tau
        if sensor_death is not None:
            update_end_of_devices([evt.name, sensor_death])
    return new_period



def plot_inter_arrival(dt, monitoring_time, emission_time_per_sensor, changed_period, t_0):
    plt.scatter([i for i in range(len(dt))], dt, label="inter-arrival over time")
    plt.title("inter arrival over time")
    plt.xlabel("iteration of reception")
    plt.ylabel("time difference between the last 2 reception")
    plt.legend()
    plt.show()
    print("interarrival:", statistics.mean(dt[int(len(dt) / 5):int(len(dt) * 3 / 5)]),
          statistics.pvariance(dt[int(len(dt) / 5):int(len(dt) * 3 / 5)]))
    print(monitoring_time)
    i = 0
    maxi = 0
    not_yet = True
    for sensor_name in emission_time_per_sensor:
        plt.scatter(emission_time_per_sensor[sensor_name], [i for j in range(len(emission_time_per_sensor[sensor_name]))], edgecolor='none')
        if not_yet is True:
            plt.scatter(changed_period[sensor_name], [i for j in range(len(changed_period[sensor_name]))], color='none',
                        edgecolor='black', linewidth=3, label="change of period instruction")
            not_yet = False
        else:
            plt.scatter(changed_period[sensor_name], [i for j in range(len(changed_period[sensor_name]))], color='none',
                        edgecolor='black', linewidth=3)
        i += 1
        if maxi < max(emission_time_per_sensor[sensor_name]):
            maxi = max(emission_time_per_sensor[sensor_name])
    time = t_0
    plt.axvline(x=time, linestyle='--', label="footstep", linewidth=0.5)
    while time < maxi:
        time += conf.tau
        plt.axvline(x=time, linestyle='--', linewidth=0.5)
    plt.title("representation of the sensor emission over time")
    plt.xlabel("time line")
    plt.ylabel("index of the sensor")
    plt.legend(loc='lower center')
    plt.show()





if __name__ == "__main__":
    M= 2
    sensor_names, event_stamp = initialisation_of_sensors()
    simul_time, dt, emission_time_per_sensor, changed_period, initial_time = monitoring_of_sensor_emissions(cycling_over_M, event_stamp, sensor_names)
    plot_inter_arrival(dt, simul_time - initial_time, emission_time_per_sensor, changed_period, initial_time)