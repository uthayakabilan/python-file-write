import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV files
baseline_df = pd.read_csv(
    '/Users/kabil/Desktop/Files/Playground/python-file-write/wrapper/resources/baseline.csv')
compare_df = pd.read_csv(
    '/Users/kabil/Desktop/Files/Playground/python-file-write/wrapper/resources/compare.csv')

# Get unique metrics
baseline_metrics = baseline_df['Metric'].unique()
compare_metrics = compare_df['Metric'].unique()
unique_metrics = set(baseline_metrics).union(compare_metrics)

# Iterate over each metric and create a separate graph
for metric in unique_metrics:
    # Filter data for the current metric from baseline and compare datasets
    baseline_data = baseline_df[baseline_df['Metric'] == metric]
    compare_data = compare_df[compare_df['Metric'] == metric]

    # Get the values for the current metric from baseline and compare datasets
    baseline_values = baseline_data['Value'].tolist()
    compare_values = compare_data['Value'].tolist()

    # Create a new figure and plot the bar graph
    plt.figure(figsize=(6, 4))
    plt.bar(['Baseline', 'Compare'], [
            baseline_values[0][0], compare_values[0][0]])
    plt.xlabel('Dataset')
    plt.ylabel('Value')
    plt.title(f'{metric} Comparison')
    plt.show()
    print(baseline_values, compare_values)

x = ["APPLES", "BANANAS"]
y = [400, 350]
plt.bar(x, y)
plt.show()
