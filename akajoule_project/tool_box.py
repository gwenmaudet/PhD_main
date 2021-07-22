import pandas as pd


general_gaz_counter = ["GENERAL PEINTURE", "GENERAL CATAPHORESE"]
general_eletric_counter = ["ARMOIRE COMPRESSEURS", "ARMOIRE CATAPHORESE"]


gaz_subcounters = [["AEROTHERMES", "RETOUCHES", "GDFA100", "GDFA300", "GDFA400", "ETUVE 80°C PRINCIPALE",
                 "ETUVE 180°C RALLONGE PRINCIPALE", "ETUVE 80°C RALLONGE", "ETUVE 180°C RALLONGE"],
                ["CHAUDIERE CATAPHORESE", "ETUVE 1", "ETUVE 2"],
                ["SOUS LE PORCHE"]]


def get_date_of_last_different_value(truncated_counter): #only the par of the values that are before the indicated date
    i = len(truncated_counter)
    value = truncated_counter[i-1]["value"]
    while i > 0:
        i -= 1
        if truncated_counter[i]["value"] < value:
            return truncated_counter[i]["date"]
    return None


def get_index_of_item_for_precise_time(counter, date):
    i = 0
    for elt in counter:
        if elt['date'] == date:
            return i
        i += 1
    return None

def convert_time_in_hours(mongo_str):
    return int(mongo_str[11:13]) + int(mongo_str[14:16]) / 60 + int(mongo_str[17:19]) / 3600


def int_in_date_type(int):
    if type(int) is str:
        return int
    if int < 10:
        return "0" + str(int)
    else:
        return str(int)


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
                                                    return False
    return True


### Extract from the csv file the information of date, type of counter, and the the value in KWh
def extract_counter_informations_from_csv_file(file_name, counter_name=None):
    df = pd.read_csv(file_name)
    df = df.to_numpy()
    output_consumption = []
    for data in df:
        stamp = data[0].split(';')
        if stamp[12] in general_gaz_counter or stamp[12] in general_eletric_counter:
            if counter_name is None or stamp[12] == counter_name:
                important_information_dic = {}
                important_information_dic['date'] = stamp[7]  # year, month, day, hour, minute
                important_information_dic['counter_type'] = stamp[12]
                important_information_dic['value'] = int(stamp[9])
                output_consumption.append(important_information_dic)
    return output_consumption


def extract_subcounter_informations_from_csv_file(file_name, subcounter_name=None):
    df = pd.read_csv(file_name)
    df = df.to_numpy()
    output_consumption = []
    for data in df:
        stamp = data[0].split(';')
        if subcounter_name is None or stamp[12] == subcounter_name:
            if stamp[12] in gaz_subcounters[0]:
                important_information_dic = {}
                important_information_dic['date'] = stamp[7]  # year, month, day, hour, minute
                important_information_dic["counter_type"] = general_gaz_counter[0]
                important_information_dic['subcounter_type'] = stamp[12]
                important_information_dic['value'] = int(stamp[9])
                output_consumption.append(important_information_dic)
            elif stamp[12] in gaz_subcounters[1]:
                important_information_dic = {}
                important_information_dic['date'] = stamp[7]  # year, month, day, hour, minute
                important_information_dic["counter_type"] = general_gaz_counter[1]
                important_information_dic['subcounter_type'] = stamp[12]
                important_information_dic['value'] = int(stamp[9])
                output_consumption.append(important_information_dic)
            elif stamp[12] in gaz_subcounters[2]:
                important_information_dic = {}
                important_information_dic['date'] = stamp[7]  # year, month, day, hour, minute
                important_information_dic["counter_type"] = 0
                important_information_dic['subcounter_type'] = stamp[12]
                important_information_dic['value'] = int(stamp[9])
                output_consumption.append(important_information_dic)
            else:
                a = 0
                print(data[0])
    return output_consumption