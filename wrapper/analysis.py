#!/usr/bin/env python
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def filter_file_extension(dir_path, ext):
    file_list = os.listdir(dir_path)
    filtered_list = []
    for file in file_list:
        if "." in file:
            split_file = file.split(".")
            if split_file[-1] == ext:
                filtered_list.append(file)
    return filtered_list


# '0:05:14.380000'
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


font1 = {'family': 'serif', 'color': 'black', 'size': 4}


def create_object_template(router_list):
    dict1 = {}
    for router in router_list:
        dict1[router] = {}
    return dict1


def get_color(val):
    try:
        val1 = float(val[0])
        val2 = float(val[1])
    except ValueError:
        val1 = parse_util_time(val[0])
        val2 = parse_util_time(val[1])
    print(val1, val2)
    if (val1 == val2):
        return 'green'
    if (val1 == 0 and val2 == 0):
        return 'green'
    percent = (val2 - val1)/val1 * 100
    if (percent < 0):
        return 'green'
    elif (0 <= percent <= 10):
        return 'yellow'
    else:
        return 'red'


def plot_and_save(data, filename):
    pp = PdfPages(filename)
    # plt.figure()
    for router in data:
        # plt.figure(figsize=(3, 3))
        axes = []
        bar_texts = []
        i = 1
        for metric in data[router]:
            plt.rc('xtick', labelsize=5)
            plt.rc('ytick', labelsize=5)
            plt.xticks(fontsize=4)
            plt.yticks(fontsize=4)
            # plt.title(f'{router} {metric} comparison', fontdict=font1)
            # plt.title("{} {} comparison".format(
            #     router, metric), fontdict=font1)
            color = get_color(data[router][metric])
            try:
                plt.subplot(3, 3, i)
                ax = plt.bar(['Baseline', 'Testrun'], [
                    float(data[router][metric][0]), float(data[router][metric][1])], width=0.45, color=['blue', color])
                axes.append(ax)
                plt.title("{} {} comparison".format(
                    router, metric), fontdict=font1)
                print(metric, float(data[router][metric][0]), float(
                    data[router][metric][1]), i)
                text1 = plt.text(0, float(data[router][metric][0])//2, float(
                    data[router][metric][0]), ha='center', fontsize=4, color="black", fontweight="bold")
                text2 = plt.text(1, float(data[router][metric][1])//2, float(
                    data[router][metric][1]), ha='center', fontsize=4, color="black", fontweight="bold")
                bar_texts.append([text1, text2])
            except ValueError:
                plt.subplot(3, 3, i)
                ax = plt.bar(['Baseline', 'Testrun'], [
                    parse_util_time(data[router][metric][0])/1000, parse_util_time(data[router][metric][1])/1000], width=0.45, color=['blue', color])
                axes.append(ax)
                plt.title("{} {} comparison".format(
                    router, metric), fontdict=font1)
                print(metric, parse_util_time(
                    data[router][metric][0])/1000, parse_util_time(data[router][metric][1])/1000, i)
                text1 = plt.text(0, (parse_util_time(data[router][metric][0])/1000)//2, (parse_util_time(
                    data[router][metric][0])/1000), ha='center', fontsize=4, color="black", fontweight="bold")
                text2 = plt.text(1, (parse_util_time(data[router][metric][1])/1000)//2, (parse_util_time(
                    data[router][metric][1])/1000), ha='center', fontsize=4, color="black", fontweight="bold")
                bar_texts.append([text1, text2])
            i = i + 1
            # plt.show()
        plt.subplots_adjust(left=0.2,
                            bottom=0.2,
                            right=0.9,
                            top=0.9,
                            wspace=0.5,
                            hspace=0.6)
        plt.savefig(pp, format='pdf')
        for x in range(0, len(axes)):
            plt.delaxes(axes[x])
            text1 = bar_texts[x][0]
            text2 = bar_texts[x][1]
            text1.set_visible(False)
            text2.set_visible(False)
    pp.close()


def plot_graph(baseline_dir, compare_dir, filename='sumamry.pdf'):
    baseline_df = pd.read_csv(baseline_dir)
    compare_df = pd.read_csv(compare_dir)
    baseline_metrics = baseline_df['Metric'].unique()
    compare_metrics = compare_df['Metric'].unique()
    unique_metrics = set(baseline_metrics).union(compare_metrics)
    baseline_routers = baseline_df['Node'].unique()
    data = create_object_template(baseline_routers)
    for metric in unique_metrics:
        baseline_data = baseline_df[baseline_df['Metric'] == metric]
        compare_data = compare_df[compare_df['Metric'] == metric]
        baseline_values = baseline_data['Value'].tolist()
        compare_values = compare_data['Value'].tolist()
        for i in range(0, len(baseline_routers)):
            data[baseline_routers[i]][metric] = [
                baseline_values[i], compare_values[i]]
    plot_and_save(data, filename)
