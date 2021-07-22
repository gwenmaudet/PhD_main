from green_wall import conf


def int_in_date_type(int):
    if type(int) is str:
        return int
    if int < 10:
        return "0" + str(int)
    else:
        return str(int)

def convert_time_in_hours(mongo_str):
    return int(mongo_str[11:13]) + int(mongo_str[14:16]) / 60 + int(mongo_str[17:19]) / 3600

def the_day_before(day, month, year):
    if int(day) == 1:
        if int(month) == 1:
            return 31, 12, int(year) - 1
        else:
            if int(month-1) in conf.month_in_31:
                return 31, int(month) - 1, year
            else:
                return 30, int(month) - 1, year
    else:
        return int(day)-1, month, year

def the_day_after(day,month,year):
    if (int(day) == 31 and month in conf.month_in_31) or (int(day) == 30 and month not in conf.month_in_31):
        if month == 12:
            return 1,1, year+1
        else:
            return 1, month+1, year
    else:
        return day+1, month, year

def get_date(str_in_mongo):
    return str_in_mongo[8:10], str_in_mongo[5:7], str_in_mongo[0:4]


def convert_voltage_in_humidity_percentage(V):
    return (1 - V / conf.max_voltage) * 100


#### Is the measure1 more recent than the measure2 ?
##  True if the measure 1 is more recent ie is after measure 2
def is_more_recent_than(measure_1, measure_2):
    t1 = measure_1["date"]
    t2 = measure_2["date"]
    if int(t1[0:4]) <= int(t2[0:4]):  # year
        if int(t1[0:4]) != int(t2[0:4]):
            return False
        else:
            if int(t1[5:7]) <= int(t2[5:7]):  # month
                if int(t1[5:7]) != int(t2[5:7]):
                    return False
                else:
                    if int(t1[8:10]) <= int(t2[8:10]):  # day
                        if int(t1[8:10]) != int(t2[8:10]):
                            return False
                        else:
                            if int(t1[11:13]) <= int(t2[11:13]):  # hour
                                if int(t1[11:13]) != int(t2[11:13]):
                                    return False
                                else:
                                    if int(t1[14:16]) <= int(t2[14:16]):  # min
                                        if int(t1[14:16]) != int(t2[14:16]):
                                            return False
                                        else:
                                            if int(t1[17:19]) <= int(t2[17:19]):  # sec
                                                if int(t1[17:19]) != int(t2[17:19]):
                                                    return False
                                                else:
                                                    # print("the objects " + str(measure_1["_id"])+ " and "+ str(measure_2["_id"])+ " have same date registration")
                                                    return False
    return True


def process_insert_sorting(list_of_measures):
    for i in range(len(list_of_measures)):
        j = i
        is_finely_placed = False
        while is_finely_placed is False:
            if j != 0:
                if is_more_recent_than(list_of_measures[j], list_of_measures[j - 1]):
                    is_finely_placed = True
                else:
                    list_of_measures[j - 1], list_of_measures[j] = list_of_measures[j], list_of_measures[j - 1]
            else:
                is_finely_placed = True
            j -= 1
    return list_of_measures


def are_they_well_sorted(list_of_measures):
    for i in range(1, len(list_of_measures)):
        if is_more_recent_than(list_of_measures[i - 1], list_of_measures[i]):
            return False
    return True



