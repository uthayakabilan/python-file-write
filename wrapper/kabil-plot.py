import pandas as pd
import matplotlib.pyplot as plt


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


def plot_graph(baseline_dir, compare_dir, save_dir):
    baseline_df = pd.read_csv(baseline_dir)
    compare_df = pd.read_csv(compare_dir)
    # save_dir = "/Users/kabil/Desktop/Files/Playground/python-file-write/wrapper/resources/graphs/"
    baseline_metrics = baseline_df['Metric'].unique()
    compare_metrics = compare_df['Metric'].unique()
    unique_metrics = set(baseline_metrics).union(compare_metrics)

    for metric in unique_metrics:
        baseline_data = baseline_df[baseline_df['Metric'] == metric]
        compare_data = compare_df[compare_df['Metric'] == metric]
        baseline_values = baseline_data['Value'].tolist()
        baseline_router = baseline_data['Node'].tolist()
        compare_values = compare_data['Value'].tolist()
        compare_router = compare_data['Node'].tolist()
        for i in range(0, len(baseline_router or compare_router)):
            try:
                plt.bar(['Baseline', 'Compare'], [
                    float(baseline_values[i]), float(compare_values[i])])
            except ValueError:
                plt.bar(['Baseline', 'Compare'], [
                    parse_util_time(baseline_values[i]), parse_util_time(compare_values[i])])
            plt.title(
                f'{baseline_router[i]} {metric} Comparison')
            plt.savefig(f'./{baseline_router[i]} {metric} Comparison.png')
            plt.show()
            plt.close()


base_dir = '/Users/kabil/Desktop/Files/Playground/python-file-write/wrapper/resources/baseline.csv'
comp_dir = '/Users/kabil/Desktop/Files/Playground/python-file-write/wrapper/resources/compare.csv'
plot_graph(base_dir, comp_dir, '/usr')
