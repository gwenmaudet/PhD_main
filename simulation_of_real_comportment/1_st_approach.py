import random
import statistics
import matplotlib.pyplot as plt
simul_time = 0
event = []


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


elm = 0
nb_of_changes = 0

class sensor:
    def __init__(self, value, period=24 * 3600, error=None, err_args=None, name="sensor", battery=1000):
        global elm
        self.value = value
        self.period = period
        self.error = error
        self.err_args = err_args
        self.battery = battery
        self.name = "{}_{:04}".format(name, elm)
        self.is_ordered = False
        self.position = None
        elm += 1

        self.wake_up = simul_time + random.uniform(0, self.period)
        insert_event(self)

    def sleep(self):
        if self.battery == 0:  # when battery is empty
            return
        #self.wake_up = simul_time + random.uniform(0, self.period)
        self.wake_up = simul_time + self.period
        insert_event(self)

    def draw(self):
        self.battery -= 1

        if self.error:
            return self.value + self.error(*self.err_args)
        return self.value

    def set_period(self, period):
        p=random.random()
        if p < 0.9:
            self.period = period


########### give the desired period ##############
new_period = 3600


if __name__ == "__main__":
    """
    for i in range(3):
        s = sensor(12, name="class A")
    
    for i in range(30):
        s = sensor(12, name="class B", error=random.gauss, err_args=(0, 0.5))
    """
    nb_of_sensors = 96
    #nb_of_sensors = 3
    for i in range(nb_of_sensors):
        s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2))

    # for e in event:
    #     print (e.name, e.wake_up)

    dt = []
    value = []
    ordered = False

    last_ordering = []

    i = 0

    t_0 = 0

    while len(event) != 0:
        evt = event.pop(0)
        assert (evt.wake_up >= simul_time)

        delta_t = evt.wake_up - simul_time
        dt.append(delta_t)

        simul_time = evt.wake_up
        sensor_value = evt.draw()
        value.append(sensor_value)
        # print (nice_time(simul_time), delta_t, evt.name,  evt.battery, sensor_value)


        ######fst approach : give the period in order that in the next period all the sensor would start at the desired time, then give the same period to all the sensors#########
        if ordered is False:
            if i == 0:
                t_0 = simul_time + evt.period## if the new period is lower than the the fst one, then the begginning of scheduling will startafter the last order is given
            if i < nb_of_sensors:
                evt.set_period(t_0 - simul_time + i * new_period / nb_of_sensors) # the newt emission will be after t_0 plus the ith scheduling : get a good schduling
                evt.position = i
                i += 1
            else:
                evt.set_period(new_period)
                i += 1
                if i == 2 * nb_of_sensors:
                    ordered = True
        else:
            if evt.is_ordered is False:
                if round((simul_time - t_0 - evt.position * new_period / nb_of_sensors) % new_period, 5) == 0:
                    if evt.period != new_period:
                        evt.set_period(new_period)
                        #print("prout")
                    else:
                        evt.is_ordered = True
                else:
                    evt.set_period(new_period - (simul_time - t_0) % new_period + evt.position * new_period / nb_of_sensors)

        ########## 2nd approach more robust to loss in the giving of orders -- give to alle sensors a period, then try to find where would start the scheduling in order to minimize the "deplacement" of the sensor periods ##
        """"if ordered is False:
            if i == 0:
                t_0 = simul_time + evt.period## if the new period is lower than the the fst one, then the begginning of scheduling will startafter the last order is given
            if i < nb_of_sensors:
                evt.set_period(t_0 - simul_time + i * new_period / nb_of_sensors) # the newt emission will be after t_0 plus the ith scheduling : get a good schduling
                evt.position = i
                i += 1
            else:
                evt.set_period(new_period)
                i += 1
                if i == 2 * nb_of_sensors:
                    ordered = True
        else:
            if evt.is_ordered is False:
                if round((simul_time - t_0 - evt.position * new_period / nb_of_sensors) % new_period, 5) == 0:
                    if evt.period != new_period:
                        evt.set_period(new_period)
                        #print("prout")
                    else:
                        evt.is_ordered = True
                else:
                    evt.set_period(new_period - (simul_time - t_0) % new_period + evt.position * new_period / nb_of_sensors)
"""
        #print(evt.period)
        #print(evt.is_ordered)
        evt.sleep()
    plt.plot(dt, label="inter-arrival over time")
    plt.title("inter arrival over time")
    plt.xlabel("iteration of reception")
    plt.ylabel("time difference between the last 2 reception")
    plt.legend()
    plt.show()
    print("duration    :", nice_time(simul_time))
    print("interarrival:", statistics.mean(dt[int(len(dt)/4):int(3*len(dt)/4)]), statistics.pvariance(dt[int(len(dt)/2):int(3*len(dt)/4)]))
    print("value       :", statistics.mean(value), statistics.pvariance(value))