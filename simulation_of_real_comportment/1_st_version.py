import random
import statistics
import matplotlib.pyplot as plt
import numpy as np
from math import log, ceil

import conf

event = []
elm = 0

nb_of_changes = 0


def insert_event(elm):
    global event

    for i in range(len(event)):
        if event[i].wake_up > elm.wake_up:
            event.insert(i, elm)
            return

    # last element
    event.append(elm)


def nice_time(t):
    d = t // (24 * 60 * 60)

    x = t % (24 * 60 * 60)
    h = t // 3600
    h %= 24

    x = x % 3600
    m = x // 60

    x = x % 60
    s = x

    assert (t == d * (24 * 60 * 60) + h * 3600 + m * 60 + s)

    return "{:04}-{:02}:{:02}:{:02}.{:03}".format(int(d), int(h), int(m), int(s), int(100 * (s - int(s))))


class sensor:
    def __init__(self, value, period=conf.initial_sensor_period, error=None, err_args=None, name="sensor",
                 battery=conf.battery_capacity, fst_wake_up=0, time_out_of_scope=None):
        global elm
        self.value = value
        self.period = period
        self.error = error
        self.err_args = err_args
        self.battery = battery
        self.name = "{}_{:04}".format(name, elm)
        # objects for simultaneously
        # self.position = None
        self.need_one_changing_of_period = False

        # object for one by one 2
        self.beggining_of_the_monitoring = None
        elm += 1
        self.time_out_of_scope = time_out_of_scope
        self.is_out_of_scope = False
        self.wake_up = fst_wake_up + random.uniform(0, self.period)
        self.fst_emission = self.wake_up
        insert_event(self)

    def sleep(self, simul_time):
        if self.time_out_of_scope is not None and simul_time + self.period > self.time_out_of_scope:
            self.is_out_of_scope = True
        if self.battery < conf.emission_consumption:  # when battery is empty
            return False
        # self.wake_up = simul_time + random.uniform(0, self.period)
        self.wake_up = simul_time + self.period
        insert_event(self)
        return True

    def draw(self):
        if self.is_out_of_scope is False:
            self.battery -= conf.emission_consumption

            if self.error:
                return self.value + self.error(*self.err_args)
            return self.value
        else:
            return None  ##meaning that the sensor has been taken out of the environment

    def set_period(self, period):
        # p = random.random()
        p = 0
        if p < 1:
            self.period = period
            self.battery -= conf.reception_consumption


def initialisation_of_sensors(fixed_arrival=False):
    ##initialisation of the sensors : case where there are sensors that are tken off, and other that arrive afteward
    names = []
    stopping_times = {}
    begginning_times = {}
    # print("sensor startin from the begginning finishing early")
    if fixed_arrival is False:
        for i in range(conf.nb_of_sensors):
            end = random.uniform(conf.initial_sensor_period + 50 * conf.desired_reception_period,
                                 conf.initial_sensor_period + 110 * conf.desired_reception_period)
            s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2))
            # s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2), time_out_of_scope=end)

            # print(s.name)
            # print(end)
            names.append(s.name)
            stopping_times[s.name] = end
            begginning_times[s.name] = s.fst_emission
    else:
        t_i = 0
        for i in range(conf.nb_of_sensors):
            begginning = random.uniform(t_i + conf.desired_reception_period * (i + 2),
                                        t_i + conf.desired_reception_period * (i + 2))
            # s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2))
            s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2), fst_wake_up=begginning)
            t_i = s.fst_emission

            # print(s.name)
            # print(end)
            names.append(s.name)
            # stopping_times[s.name] = end
            begginning_times[s.name] = s.fst_emission
    return names, begginning_times

    # print("snesors starting late ")
    """for i in range(conf.nb_of_sensors // 4):
        begin = random.uniform(0, conf.max_time / 3)
        s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2), fst_wake_up=begin)
        print(s.name)
        print(begin)"""
    """

    print("sensor startin from the begginning finishing early")
    for i in range(nb_of_sensors):
        end = random.uniform(2 * reception_period, max_time / 2)
        s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2))
        #s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2), time_out_of_scope=end)

        print(s.name)
        print(end)"""


########### building of strategies ##############


def sensors_emitting_simultaneously_1():
    simul_time = 0
    sensor_names = initialisation_of_sensors()

    # e in event:
    #     print (e.name, e.wake_up)

    dt = []
    value = []
    i = 0
    sensor_list = []
    t_0 = 0
    while len(event) != 0:
        evt = event.pop(0)
        assert (evt.wake_up >= simul_time)
        delta_t = evt.wake_up - simul_time

        simul_time = evt.wake_up
        sensor_value = evt.draw()
        if sensor_value is not None:  # le message recu n'indique pas que le capteur est passé en dehors de l'environnement
            dt.append(delta_t)
            value.append(sensor_value)
            if evt.name not in sensor_list:
                sensor_list.append(evt.name)
                new_period = conf.desired_reception_period * len(sensor_list)

                """evt.position = i
                i += 1
                if i == 0:
                    t_0 = simul_time + evt.period  ## if the new period is lower than the the fst one, then the begginning of scheduling will startafter the last order is given
                """

                """evt.position = 0
                for ev in event:
                    if simul_time > ev.fst_wake_up:
                        ev.position += 1"""

                evt.position = 0
                i = 0
                i += 1
                for ev in event:
                    if simul_time > ev.fst_emission:
                        ev.position = None

            # else:
            ######fst approach : give the period in order that in the next period all the sensor would start at the desired time, then give the same period to all the sensors#########
            """link to the proposition : if a new sensor arrives, then we fix the time to it, and the next sensor have the next positions"""
            """if evt.position is None:
                evt.position = i
                i += 1"""
            if round((simul_time - t_0 - evt.position * new_period / len(sensor_list)) % new_period, 3) == 0:
                if evt.period != new_period:
                    evt.set_period(new_period)
                    time_when_ordered = simul_time
                    # print("prout")
            else:
                evt.set_period(
                    new_period - (simul_time - t_0) % new_period + evt.position * new_period / len(sensor_list))

            # print(evt.period)
            # print(evt.is_ordered)
            evt.sleep(simul_time)
        else:
            if evt.name in sensor_list:
                sensor_list.remove(evt.name)
                new_period = conf.desired_reception_period * len(sensor_list)
                # initialisation of sensor position
                k = 0
                for ev in event:
                    if ev.fst_emission < simul_time:
                        ev.position = k
                        k += 1
    monitoring_time = 0
    for delta in dt:
        if delta <= conf.desired_reception_period:
            monitoring_time += delta
    return dt, monitoring_time


def sensors_emitting_simultaneously_2():
    simul_time = 0
    sensor_names, begginning_times = initialisation_of_sensors()

    # e in event:
    #     print (e.name, e.wake_up)

    dt = []
    output = {}
    changed_period = {}
    stopping_times = {}
    for name in sensor_names:
        output[name] = []
        changed_period[name] = []
        stopping_times[name] = None
    value = []
    i = 0
    sensor_list = []
    t_0 = 0
    last_scheduled_candidate = []  ### [0] : the time of the last scheduled candidate
    while len(event) != 0:
        evt = event.pop(0)
        assert (evt.wake_up >= simul_time)
        delta_t = evt.wake_up - simul_time

        sensor_value = evt.draw()
        if sensor_value is not None:  # le message recu n'indique pas que le capteur est passé en dehors de l'environnement
            simul_time = evt.wake_up
            dt.append(delta_t)
            value.append(sensor_value)
            output[evt.name].append(simul_time)
            if evt.name not in sensor_list:
                sensor_list.append(evt.name)
                if t_0 == 0:
                    t_0 = simul_time
                    evt.set_period(conf.desired_reception_period)
                    changed_period[evt.name].append(simul_time)
                    evt.expected_next_emission = t_0 + conf.desired_reception_period
                    last_scheduled_candidate = [simul_time]
                else:
                    """evt.set_period((len(sensor_list)) * conf.desired_reception_period + conf.desired_reception_period - ((
                            simul_time - t_0) % conf.desired_reception_period))"""

                    new_period = conf.desired_reception_period - (
                                simul_time - last_scheduled_candidate[0]) % conf.desired_reception_period + (
                                             len(sensor_list) - 1) * conf.desired_reception_period
                    evt.set_period(new_period)
                    changed_period[evt.name].append(simul_time)
                    #            nb of precedent sensor plus this one * the inter arrival + the time between thie emission and the next one
                    evt.need_one_changing_of_period = True
                    evt.expected_next_emission = simul_time + new_period
            else:
                if round(evt.expected_next_emission, 3) == round(simul_time, 3):
                    if (evt.need_one_changing_of_period == True) or (
                            evt.need_one_changing_of_period == False and evt.period != len(
                        sensor_list) * conf.desired_reception_period):
                        evt.set_period(len(sensor_list) * conf.desired_reception_period)
                        changed_period[evt.name].append(simul_time)
                        evt.expected_next_emission = simul_time + len(sensor_list) * conf.desired_reception_period
                        evt.need_one_changing_of_period = False

                    else:
                        evt.expected_next_emission = simul_time + evt.period
                        evt.need_one_changing_of_period = False
                    last_scheduled_candidate = [simul_time]
                else:
                    print("pbbbbbbbb !!! ")
                    print(simul_time)
                    evt.set_period(evt.expected_next_emission)
                    changed_period[evt.name].append(simul_time)

                    evt.expected_next_emission = simul_time + evt.expected_next_emission

                    evt.need_one_changing_of_period = True
            bool = evt.sleep(simul_time)

            if bool is False:
                sensor_list.remove(evt.name)
        else:
            # last_scheduled_candidate = [evt.wake_up]
            sensor_list.remove(evt.name)
            stopping_times[evt.name] = evt.wake_up
        for ev in event:
            if ev.fst_emission < simul_time:
                # TODO : gerer le fait qu'il y ai un ajout de nouveau capteur entre le moment ou le capteur en question devait emettre et simul-time
                if ev.expected_next_emission < simul_time:
                    ev.expected_next_emission += len(sensor_list) * conf.desired_reception_period

    monitoring_time = 0
    for delta in dt:
        if delta <= conf.desired_reception_period:
            monitoring_time += delta
    return dt, monitoring_time, output, changed_period, stopping_times, begginning_times, t_0


def one_by_one_1():
    simul_time = 0
    sensor_names, begginning_times = initialisation_of_sensors()

    # e in event:
    #     print (e.name, e.wake_up)

    dt = []
    output = {}
    changed_period = {}
    stopping_times = {}
    for name in sensor_names:
        output[name] = []
        changed_period[name] = []
        stopping_times[name] = None
    value = []
    i = 0
    sensor_list = []
    t_0 = 0
    last_scheduled_candidate = []  ### [0] : the time of the last scheduled candidate
    last_out_of_battery = 0
    while len(event) != 0:
        evt = event.pop(0)

        assert (evt.wake_up >= simul_time)

        delta_t = evt.wake_up - simul_time
        dt.append(delta_t)
        simul_time = evt.wake_up
        sensor_value = evt.draw()
        value.append(sensor_value)
        output[evt.name].append(simul_time)
        # print (nice_time(simul_time), delta_t, evt.name,  evt.battery, sensor_value)
        ### fixing the period of the sensors
        if evt.name not in sensor_list:
            sensor_list.append(evt.name)
            if evt.period != conf.desired_reception_period:
                if last_out_of_battery == 0:
                    if t_0 == 0:
                        t_0 = simul_time
                    evt.set_period(conf.desired_reception_period)
                    changed_period[evt.name].append(simul_time)
                    last_out_of_battery = simul_time + (
                            (
                                evt.battery) // conf.emission_consumption + 1) * conf.desired_reception_period
                else:
                    if (last_out_of_battery - simul_time) > 0:
                        evt.set_period(last_out_of_battery - simul_time)
                        changed_period[evt.name].append(simul_time)
                        last_out_of_battery = last_out_of_battery + (
                                (
                                        evt.battery - conf.emission_consumption) // conf.emission_consumption) * conf.desired_reception_period
                    else:
                        evt.set_period(conf.desired_reception_period)
                        changed_period[evt.name].append(simul_time)
                        last_out_of_battery = simul_time + (
                                (
                                        evt.battery - conf.emission_consumption) // conf.emission_consumption) * conf.desired_reception_period
        else:
            if evt.period != conf.desired_reception_period:
                evt.set_period(conf.desired_reception_period)
                changed_period[evt.name].append(simul_time)
        evt.sleep(simul_time)
    monitoring_time = 0
    for delta in dt:
        if delta <= conf.desired_reception_period:
            monitoring_time += delta
    return dt, monitoring_time, output, changed_period, stopping_times, begginning_times, t_0


"""Strategy : dichotomie - si un capteur doit se reconnecter a un moment on vas lui faire emettre a une periode (prochain départ)/n 
n étant a fixer. Ensuite quand on re-recoit le message suivant, on divise une fois de plus par n le temps du massage suivant.
exple pour n=2

volonté d'emission:
-________________-
-________-____-__-
de sorte a palier les problemes de reception d'ordres
"""


def one_by_one_2():
    counter = 0

    simul_time = 0

    nb_of_sensors_detected_in_information_systeme = 0
    # nb_of_sensors = 3
    sensor_names = initialisation_of_sensors()
    dt = []
    j = 0
    value = []
    last_emission_of_the_last_sensor = 0
    sensor_list = []
    currently_active = []
    while len(event) != 0:
        evt = event.pop(0)

        assert (evt.wake_up >= simul_time)

        delta_t = evt.wake_up - simul_time
        dt.append(delta_t)
        simul_time = evt.wake_up
        sensor_value = evt.draw()
        if sensor_value is not None:
            value.append(sensor_value)
            # print (nice_time(simul_time), delta_t, evt.name,  evt.battery, sensor_value)
            ### fixing the period of the sensors
            if evt.name not in sensor_list:
                sensor_list.append(evt.name)
                evt.beggining_of_the_monitoring = last_emission_of_the_last_sensor
                evt.position = j
                j += 1
                if evt.position == 0:
                    last_emission_of_the_last_sensor = 0
                    last_emission_of_the_last_sensor += simul_time
                    estimation_of_the_loss_du_to_the_robustness = 0
                    currently_active.append(evt.name)
                    evt.beggining_of_the_monitoring = last_emission_of_the_last_sensor
                else:
                    if last_emission_of_the_last_sensor - simul_time > 0:
                        estimation_of_the_loss_du_to_the_robustness = (
                                                                              conf.emission_consumption + conf.reception_consumption) * ceil(
                            log(
                                conf.maxi_period_for_sequensing / (
                                        last_emission_of_the_last_sensor - simul_time)) / log(
                                (conf.n_sequensing_for_robustness - 1) / conf.n_sequensing_for_robustness))
                last_emission_of_the_last_sensor += (
                                                            (
                                                                    evt.battery - conf.emission_consumption - estimation_of_the_loss_du_to_the_robustness) // conf.emission_consumption) * conf.desired_reception_period  # estimation of the number of emission done during monitoring
            if evt.period != conf.desired_reception_period:
                if (
                        evt.beggining_of_the_monitoring - simul_time) / conf.n_sequensing_for_robustness > conf.maxi_period_for_sequensing:
                    evt.set_period((evt.beggining_of_the_monitoring - simul_time) / conf.n_sequensing_for_robustness)
                else:
                    evt.set_period(conf.desired_reception_period)
                    currently_active.append(evt.name)
            evt.sleep(simul_time)
        else:
            counter += 1
            if evt.name in currently_active:
                sensor_list = []
                j = 0
                currently_active = []
            else:
                k = evt.position
                monitoring_begginning_slisting = [evt.beggining_of_the_monitoring]
                for ev in event:
                    if ev.fst_emission < simul_time:
                        if ev.position > k:
                            monitoring_begginning_slisting.append(ev.beggining_of_the_monitoring)
                monitoring_begginning_slisting = sorted(monitoring_begginning_slisting)
                for ev in event:
                    if ev.fst_emission < simul_time:
                        if ev.position > k:
                            index = monitoring_begginning_slisting.index(ev.beggining_of_the_monitoring)
                            ev.beggining_of_the_monitoring = monitoring_begginning_slisting[index - 1]
                            ev.position -= 1
                last_emission_of_the_last_sensor = monitoring_begginning_slisting[-1]
    monitoring_time = 0
    for delta in dt:
        if delta <= conf.desired_reception_period:
            monitoring_time += delta
    return dt, monitoring_time


def hybrid_version(M):
    simul_time = 0
    sensor_names, begginning_times = initialisation_of_sensors(fixed_arrival=True)

    # e in event:
    #     print (e.name, e.wake_up)

    dt = []
    output = {}
    changed_period = {}
    stopping_times = {}

    for name in sensor_names:
        output[name] = []
        changed_period[name] = []
        stopping_times[name] = None
    value = []
    i = 0
    sensor_list = []
    t_0 = 0
    last_scheduled_candidate = []  ### [0] : the time of the last scheduled candidate
    end_of_devices = []
    beggining = 0
    while len(event) != 0:
        evt = event.pop(0)
        assert (evt.wake_up >= simul_time)
        delta_t = evt.wake_up - simul_time
        if beggining == 0:
            beggining = simul_time
        sensor_value = evt.draw()
        if sensor_value is not None:  # le message recu n'indique pas que le capteur est passé en dehors de l'environnement
            simul_time = evt.wake_up
            dt.append(delta_t)
            value.append(sensor_value)
            output[evt.name].append(simul_time)
            if evt.name not in sensor_list:
                sensor_list.append(evt.name)

                if len(sensor_list) <= M:
                    if len(sensor_list) == 1:
                        t_0 = simul_time
                        new_period = conf.desired_reception_period
                        time_for_changing_of_the_sensor = t_0 + new_period + ((
                                                                                  evt.battery) // conf.emission_consumption - 1) * conf.desired_reception_period
                    else:
                        new_period = conf.desired_reception_period - (
                                simul_time - t_0) % conf.desired_reception_period + (
                                             len(sensor_list) - 1) * conf.desired_reception_period

                        # new_period = (simul_time - t_0)%conf.desired_reception_period + len(sensor_list) * conf.desired_reception_period
                        evt.need_one_changing_of_period = True
                        time_for_changing_of_the_sensor = t_0 + new_period + ((
                                                                                      evt.battery - conf.reception_consumption) // conf.emission_consumption - 1) * conf.desired_reception_period
                    changed_period[evt.name].append(simul_time)
                    evt.set_period(new_period)
                    evt.expected_next_emission = t_0 + new_period
                    # end_of_devices.append((evt.battery - conf.emission_consumption - conf.reception_consumption * (M - len(sensor_list)))// conf.emission_consumption + simul_time)
                    end_of_devices.append(
                        [evt.name, time_for_changing_of_the_sensor])  ##[evt.name, hypothetic_out_of_battery]


                else:
                    """evt.set_period((len(sensor_list)) * conf.desired_reception_period + conf.desired_reception_period - ((
                            simul_time - t_0) % conf.desired_reception_period))"""
                    beggining_of_this_sensor = end_of_devices.pop(0)
                    new_period = beggining_of_this_sensor[1] - simul_time
                    evt.set_period(new_period)
                    changed_period[evt.name].append(simul_time)
                    #            nb of precedent sensor plus this one * the inter arrival + the time between thie emission and the next one
                    evt.need_one_changing_of_period = True
                    evt.expected_next_emission = simul_time + new_period
                    end_of_devices.append([evt.name, evt.expected_next_emission + ((
                                                                                               evt.battery - conf.reception_consumption) // conf.emission_consumption - 1) * conf.desired_reception_period * M])
            else:
                if round(evt.expected_next_emission, 3) == round(simul_time, 3):
                    if (evt.need_one_changing_of_period == True) or (
                            evt.need_one_changing_of_period == False and evt.period != min(len(sensor_list),
                                                                                           M) * conf.desired_reception_period):
                        new_period = min(len(sensor_list), M) * conf.desired_reception_period
                        evt.set_period(new_period)
                        changed_period[evt.name].append(simul_time)
                        evt.expected_next_emission = simul_time + new_period
                        evt.need_one_changing_of_period = False

                    else:
                        evt.expected_next_emission = simul_time + evt.period
                        evt.need_one_changing_of_period = False
                    for i in range(len(end_of_devices)):
                        if end_of_devices[i][0] == evt.name:
                            if len(sensor_list) < M:
                                end_of_devices[i][1] = evt.expected_next_emission + ((
                                                                                             evt.battery - conf.reception_consumption) // conf.emission_consumption - 1) * conf.desired_reception_period * M
                            else:
                                end_of_devices[i][1] = evt.expected_next_emission + ((
                                                                                         evt.battery) // conf.emission_consumption - 1) * conf.desired_reception_period * M
                else:
                    print("pbbbbbbbb !!! ")
                    print(simul_time)
                    print(evt.expected_next_emission)
                    evt.set_period(evt.expected_next_emission)
                    changed_period[evt.name].append(simul_time)

                    evt.expected_next_emission = simul_time + evt.expected_next_emission

                    evt.need_one_changing_of_period = True
            evt.expected_next_emission = simul_time + evt.period
            bool = evt.sleep(simul_time)
            if bool is False:
                sensor_list.remove(evt.name)
                stopping_times[evt.name] = simul_time

        else:
            # last_scheduled_candidate = [evt.wake_up]
            sensor_list.remove(evt.name)
            stopping_times[evt.name] = evt.wake_up
        for ev in event:
            if ev.fst_emission < simul_time:
                # TODO : gerer le fait qu'il y ai un ajout de nouveau capteur entre le moment ou le capteur en question devait emettre et simul-time
                if ev.expected_next_emission < simul_time:
                    ev.expected_next_emission += len(sensor_list) * conf.desired_reception_period

    monitoring_time = 0
    for delta in dt:
        if delta <= conf.desired_reception_period:
            monitoring_time += delta
    monitoring_time = simul_time - beggining
    return dt, monitoring_time, output, changed_period, stopping_times, begginning_times, t_0


def plot_inter_arrival():
    # dt, monitoring_time, output, changed_period, stopping_times,begginning_times, t_0 = one_by_one_1()
    # dt, monitoring_time = one_by_one_2()
    # dt, monitoring_time = sensors_emitting_simultaneously_1()
    # dt, monitoring_time, output, changed_period, stopping_times,begginning_times, t_0 = sensors_emitting_simultaneously_2()
    dt, monitoring_time, output, changed_period, stopping_times, begginning_times, t_0 = hybrid_version(3)
    print(stopping_times)
    print(begginning_times)
    """to_print = ""
    for i in range(len(dt)):
        to_print += "(" + str(i) + "," + str(dt[i]) + ") "
    print(to_print)"""
    plt.scatter([i for i in range(len(dt))], dt, label="inter-arrival over time")
    plt.title("inter arrival over time")
    plt.xlabel("iteration of reception")
    plt.ylabel("time difference between the last 2 reception")
    plt.legend()
    plt.show()
    """to_print=""
    for i in range(5000, 5100):
        to_print += "(" + str(i) + "," + str(dt[i]) + ") "
    print(to_print)"""
    # plt.scatter([i for i in range(5000, 5100)], dt[5000:5100], label="inter-arrival over time")
    # plt.scatter([i for i in range(2200, 2800)], dt[2200: 2800], label="inter-arrival over time")
    plt.title("inter arrival over time")
    plt.xlabel("iteration of reception")
    plt.ylabel("time difference between the last 2 reception")
    plt.legend()
    plt.show()
    # print("duration    :", nice_time(simul_time))
    print("interarrival:", statistics.mean(dt[int(len(dt) / 5):int(len(dt) * 3 / 5)]),
          statistics.pvariance(dt[int(len(dt) / 5):int(len(dt) * 3 / 5)]))
    print(monitoring_time)

    # print("value       :", statistics.mean(value), statistics.pvariance(value))
    i = 0
    maxi = 0
    # plt.scatter(0, 0, marker='X', color='red', edgecolors="red", label = "left out of the monitoring")
    # plt.scatter(0,0, marker='v', color='green', edgecolors="green", label="first emission of the sensor")
    not_yet = True
    for sensor_name in output:
        plt.scatter(output[sensor_name], [i for j in range(len(output[sensor_name]))], edgecolor='none')
        if not_yet is True:
            plt.scatter(changed_period[sensor_name], [i for j in range(len(changed_period[sensor_name]))], color='none',
                        edgecolor='black', linewidth=3, label="change of period instruction")
            not_yet = False
        else:
            plt.scatter(changed_period[sensor_name], [i for j in range(len(changed_period[sensor_name]))], color='none',
                        edgecolor='black', linewidth=3)

        if stopping_times[sensor_name] is not None:
            plt.scatter(stopping_times[sensor_name], i, marker='X', color='red', edgecolors="red")
        # plt.scatter(begginning_times[sensor_name], i, marker = 'v',color='green', edgecolors="green")
        i += 1
        if maxi < max(output[sensor_name]):
            maxi = max(output[sensor_name])
    print(maxi)
    time = t_0
    plt.axvline(x=time, linestyle='--', label="footstep", linewidth=0.5)
    while time < maxi:
        time += conf.desired_reception_period
        plt.axvline(x=time, linestyle='--', linewidth=0.5)

    plt.title("representation of the sensor emission over time")
    plt.xlabel("time line")
    plt.ylabel("index of the sensor")
    plt.legend(loc='lower center')
    plt.show()


def plot_results_from_hybride():
    X = []
    Y = []
    Y_theo = []
    for M in range(1, conf.nb_of_sensors + 1, 3):
        y = []
        X.append(M)
        for i in range(conf.nb_of_iteration):
            dt, monitoring_time, output, changed_period, stopping_times, begginning_times, t_0 = hybrid_version(M)
            y.append(monitoring_time)

        Y.append(statistics.mean(y))
        y_theo = (conf.nb_of_sensors * conf.battery_capacity
                   - (2 * conf.nb_of_sensors - 1 + M*(M - 1)) * conf.reception_consumption
                   - (1 *conf.nb_of_sensors - 1) * conf.emission_consumption) *conf.desired_reception_period/ conf.emission_consumption
        Y_theo.append(y_theo)
    plt.plot(X, Y, label="real monitoring time")
    plt.plot(X, Y_theo, label = "function f")
    plt.xlabel("Size of the active sensor set")
    plt.ylabel("Monitoring time")
    plt.title("Representation of the monitoring time relatively to the sensor set considered")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    """means = []

    for i in range(1000):
        dt, pct_before_being_scheduled =main_1()
        means.append(pct_before_being_scheduled)
    print(statistics.mean(means))"""
    plot_inter_arrival()
    #plot_results_from_hybride()
    # sensors_emitting_simultaneously()
