import sys
import os
import re
import operator
import csv
def sort_messages(file):
    error_types = {}
    stats_types={}
    for line in file.readlines():
        error = re.search(r'(ticky: ERROR:)([\w ]*)', line)
        stats = re.search(r'(ERROR|INFO).*\((.*)\)', line)
        if error: 
            if error.group(2) in error_types:
                error_types[error.group(2)] += 1
            else:
                error_types[error.group(2)] = 1
        #seperates by name first. Then increments errors and info stats
        if not stats.group(2) in stats_types:
            stats_types[stats.group(2)] = {"ERROR": 0, "INFO": 0}
        stats_types[stats.group(2)][stats.group(1)] += 1
    return [stats_types, error_types]

def generate_csv(stats_types, error_types):
    #generate error csv file:
    with open(os.path.join(sys.path[0], "error.csv"), "w") as csvf:
        writer = csv.writer(csvf)
        writer.writerow(["Error", "Count"])
        for item in error_types:
            writer.writerow([item[0], item[1]])
    #generate stats csv file 
    with open(os.path.join(sys.path[0], "stats.csv"), "w") as csvf:
        writer = csv.writer(csvf)
        writer.writerow(["Username", "INFO", "ERROR"])
        for item in stats_types:
            writer.writerow([item[0], item[1]["INFO"], item[1]["ERROR"]])

with open(os.path.join(sys.path[0], "syslog.txt"), "r") as file:
    #counts error types, and user stats. then collects them in respective dictionaries
    #returns two dictionaries stored in a list
    stats_error_dict = sort_messages(file)
   
    #sort dictonary values into descending order
    stats_error_dict[0] = sorted(stats_error_dict[0].items(), key=operator.itemgetter(0))
    stats_error_dict[1] = sorted(stats_error_dict[1].items(), key=operator.itemgetter(1), reverse=True)
    
    #generate csv files
    generate_csv(stats_error_dict[0], stats_error_dict[1])
    