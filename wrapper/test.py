from analysis import parse_util_time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

font1 = {'family': 'serif', 'color': 'black', 'size': 4}


def create_object_template(router_list):
    dict1 = {}
    for router in router_list:
        dict1[router] = {}
    return dict1


def get_color(val):
    val1, val2, *other = val
    try:
        val1 = int(val[0])
        val2 = int(val[1])
    except ValueError:
        val1 = parse_util_time(val[0])
        val2 = parse_util_time(val[1])
    if (val1 == 0 and val2 == 0):
        # print(val1, val2)
        return 'black'
    if (val1 == val2):
        return 'green'
    percent = ((val2 - val1)/val1)*100
    if (percent == 0 or percent < 0):
        return 'green'
    elif (0 < percent <= 10):
        return 'yellow'
    else:
        return 'red'


def plot_and_save(data):
    pp = PdfPages("subplot.pdf")
    # plt.figure(figsize=(3, 3))
    # plt.figure()
    for router in data:
        plt.figure(figsize=(3, 3))
        plt.figure()
        axes = []
        i = 1
        for metric in data[router]:
            plt.rc('xtick', labelsize=5)
            plt.rc('ytick', labelsize=5)
            plt.xticks(fontsize=4)
            plt.yticks(fontsize=4)
            plt.title(f'{router} {metric} comparison', fontdict=font1)
            # plt.subplot(3, 3, i)
            color = get_color(data[router][metric])
            try:
                plt.subplot(3, 3, i)
                ax = plt.bar(['Baseline', 'Compare'], [
                    float(data[router][metric][0]), float(data[router][metric][1])], width=0.45, color=['blue', color])
                axes.append(ax)
            except ValueError:
                plt.subplot(3, 3, i)
                ax = plt.bar(['Baseline', 'Compare'], [
                    parse_util_time(data[router][metric][0])*1000, parse_util_time(data[router][metric][1])*1000], width=0.45, color=['blue', color])
                axes.append(ax)
            # print(metric)
            # print(data[router][metric])
            i = i + 1
        plt.subplots_adjust(left=0.2,
                            bottom=0.2,
                            right=0.9,
                            top=0.9,
                            wspace=0.5,
                            hspace=0.6)
        plt.savefig(pp, format='pdf')
        for x in range(0, len(axes)):
            plt.delaxes(axes[x])
        # plt.show()
    pp.close()


def plot_graph(baseline_dir, compare_dir, filename='sumamry.pdf'):
    baseline_df = pd.read_csv(baseline_dir)
    compare_df = pd.read_csv(compare_dir)
    # save_dir = "/Users/kabil/Desktop/Files/Playground/python-file-write/wrapper/resources/graphs/"
    baseline_metrics = baseline_df['Metric'].unique()
    compare_metrics = compare_df['Metric'].unique()
    unique_metrics = set(baseline_metrics).union(compare_metrics)
    baseline_routers = baseline_df['Node'].unique()
    data = create_object_template(baseline_routers)
    for metric in unique_metrics:
        baseline_data = baseline_df[baseline_df['Metric'] == metric]
        compare_data = compare_df[compare_df['Metric'] == metric]
        # values from the data frame
        baseline_values = baseline_data['Value'].tolist()
        compare_values = compare_data['Value'].tolist()
        for i in range(0, len(baseline_routers)):
            data[baseline_routers[i]][metric] = [
                baseline_values[i], compare_values[i]]
    plot_and_save(data)


plot_graph(baseline_dir="/Users/kabil/Desktop/Files/Playground/python-file-write/wrapper/resources/baseline.csv",
           compare_dir="/Users/kabil/Desktop/Files/Playground/python-file-write/wrapper/resources/compare.csv")
