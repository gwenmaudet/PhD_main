import pymongo
import extraction_of_information


import generic_tools

client = pymongo.MongoClient("mongodb://gwen:thesard_errant@wall.plido.net") # defaults to port 27017
db = client.green_wall
raw_data = db.raw





def get_all_measures():
    mongo_object = raw_data.find()
    all_data = []
    for element in mongo_object:
        all_data.append(element)
    all_data.reverse()
    return all_data



def get_last_measure():
    all_measures = get_all_measures()
    the_most_recent = all_measures[0]
    for measure in all_measures:
         if generic_tools.is_more_recent_than(measure, the_most_recent) is True:
             the_most_recent = measure
    return the_most_recent


def get_all_data_from_one_day(day,month,year):
    all_data = get_all_measures()
    d_day_data = []
    for measure in all_data:
        if measure['date'][0:10] == generic_tools.int_in_date_type(year) + "-" + generic_tools.int_in_date_type(month) + "-" + generic_tools.int_in_date_type(day):
            d_day_data.append(measure)
    return d_day_data
