#!/usr/bin/env python
import os
import csv


def filter_file_extension(dir_path, ext):
    file_list = os.listdir(dir_path)
    filtered_list = []
    for file in file_list:
        if "." in file:
            split_file = file.split(".")
            if split_file[-1] == ext:
                filtered_list.append(file)
    return filtered_list


# for cpu utilization
def parse_util_time(time):
    replaced_string = time.replace(":", ".")
    replaced_string = replaced_string.split(".")
    total_time = 0
    if len(replaced_string) == 4:
        # hours to millisecond
        total_time = total_time + int(replaced_string[0]) * 3600000
        total_time = (
            total_time + int(replaced_string[1]) * 60000
        )  # minutes to milliseconds
        # seconds to milliseconds
        total_time = total_time + int(replaced_string[2]) * 1000
        total_time = total_time + int(replaced_string[3])
    elif len(replaced_string) == 3:
        total_time = (
            total_time + int(replaced_string[0]) * 60000
        )  # minutes to milliseconds
        # seconds to milliseconds
        total_time = total_time + int(replaced_string[1]) * 1000
        total_time = total_time + int(replaced_string[2])
    return total_time


def get_lowest_value(file_dir):
    csv_files = filter_file_extension(file_dir, "csv")
    lowest_memory_file = []
    if len(csv_files) == 1:
        return os.path.join(file_dir, csv_files[0])
    elif len(csv_files) == 0:
        return "no file found"
    else:
        for filename in csv_files:
            data = []
            with open(os.path.join(file_dir, filename), "r") as file:
                csv_file = csv.reader(file)
                memory_usage = 0
                cpu_util = 0
                for line in csv_file:
                    if "Memory_Usage" in line[1]:
                        memory_usage = memory_usage + float(line[2])
                    if "cpu_UTIL" in line[1]:
                        time = parse_util_time(line[2])
                        cpu_util = cpu_util + time
                # print(file.name, __name__, memory_usage, cpu_util)
                data.append(file.name)
                data.append(memory_usage)
                data.append(cpu_util)
            lowest_memory_file.append(data)
        lowest_memory_file.sort(key=lambda x: (x[1], x[2]))
    return lowest_memory_file[0][0]
