import os
import csv


def filterFileExtension(dir_path, ext):
    file_list = os.listdir(dir_path)
    filtered_list = []
    for file in file_list:
        if "." in file:
            split_file = file.split(".")
            if split_file[-1] == ext:
                filtered_list.append(file)
    return filtered_list


# '0:05:14.380000'
def parseUTILTime(time):
    replacedString = time.replace(":", ".")
    replacedString = replacedString.split(".")
    totalTime = 0
    if len(replacedString) == 4:
        # hours to millisecond
        totalTime = totalTime + int(replacedString[0]) * 3600000
        totalTime = (
            totalTime + int(replacedString[1]) * 60000
        )  # minutes to milliseconds
        # seconds to milliseconds
        totalTime = totalTime + int(replacedString[2]) * 1000
        totalTime = totalTime + int(replacedString[3])
    elif len(replacedString) == 3:
        totalTime = (
            totalTime + int(replacedString[0]) * 60000
        )  # minutes to milliseconds
        # seconds to milliseconds
        totalTime = totalTime + int(replacedString[1]) * 1000
        totalTime = totalTime + int(replacedString[2])
    return totalTime


def getLowestValue(file_dir):
    csv_files = filterFileExtension(file_dir, "csv")
    lowest_memory_file = []
    if len(csv_files) == 1:
        return os.path.join(file_dir, csv_files[0])
    elif len(csv_files) == 0:
        return "no file found"
    else:
        for filename in csv_files:
            data = []
            with open(os.path.join(file_dir, filename), "r") as file:
                csvFile = csv.reader(file)
                memory_usage = 0
                cpu_util = 0
                for line in csvFile:
                    if "Memory_Usage" in line[1]:
                        memory_usage = memory_usage + float(line[2])
                    if "cpu_UTIL" in line[1]:
                        time = parseUTILTime(line[2])
                        cpu_util = cpu_util + time
                # print(file.name, __name__, memory_usage, cpu_util)
                data.append(file.name)
                data.append(memory_usage)
                data.append(cpu_util)
            lowest_memory_file.append(data)
        lowest_memory_file.sort(key=lambda x: (x[1], x[2]))
    return lowest_memory_file[0][0]


# path = os.path.join(os.getcwd(), "wrapper")
# file_path = os.path.join(
#     "/Users/kabil/Desktop/Files/Playground/python-file-write/cx-health-monitor/",
#     "Multicast",
#     "Baseline",
#     "XX_10_12_0001AJ",
# )

# getLowestValue(file_path)
