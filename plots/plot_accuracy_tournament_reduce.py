import os
import re
import matplotlib.pyplot as plt
import numpy as np


save_dir = "/data/home/qvd/Assignments/a2-the-squad/plots/"

# Function to extract misprediction rate for conditional branches
def extract_accuracy_rate(file_content):
    match = re.search(r'Branch Prediction Accuracy:\s*([0-9.]+)%\s*MPKI:\s*([0-9.]+)\s*Average ROB Occupancy at Mispredict:\s*([0-9.]+)', file_content)
    if match:
        accuracy = float(match.group(1))
        return accuracy
    return 0

# Directory where all result files are stored
results_dir = "/data/home/qvd/Assignments/a2-the-squad/results_10M/"

# Benchmark list
benchmarks_list = [
    "600.perlbench_s-210B",
    "602.gcc_s-734B",
    "625.x264_s-18B",
    "641.leela_s-800B",
    "648.exchange2_s-1699B"
]

# Benchmark table
benchmarks_table = [
    "4096",
    "65536",
    "1048576",
    "16777216",
]

# Initialize the data dictionary
data = {f"{size}+{b}": [] for size in benchmarks_table for b in benchmarks_list}

# Iterate through all files in the directory
for filename in os.listdir(results_dir):
    for size in benchmarks_table:
        if f'vinh_tournament_reduce_{size}' in filename:
            # Construct the full file path
            file_path = os.path.join(results_dir, filename)

            # Extract benchmark name
            benchmark_match = re.match(r'(\d+\.\w+_\w+-\d+B)', filename)
            if benchmark_match:
                benchmark = benchmark_match.group(1)
                if benchmark in benchmarks_list:
                    # Read the contents of the file
                    with open(file_path, 'r') as file:
                        content = file.read()
                        accuracy = extract_accuracy_rate(content)
                        data[f"{size}+{benchmark}"].append(accuracy)

print(data)
# Prepare data for plotting
benchmarks = list(set(key.split('+')[1] for key in data.keys()))
sizes = sorted(set(key.split('+')[0] for key in data.keys()))

# Sort the sizes and prepare accuracies
sorted_sizes = sorted(sizes, key=int)  # Sort sizes as integers
accuracies = {size: [data[f"{size}+{b}"][0] for b in benchmarks] for size in sorted_sizes}

# Set up bar positions
x = np.arange(len(benchmarks))
width = 0.15  # Width of the bars

# Create the plot
plt.figure(figsize=(12, 7))

# Plot each size as a separate set of bars
for i, size in enumerate(sorted_sizes):
    plt.bar(x + i * width, accuracies[size], width=width, label=size)

# Add labels and title
plt.xticks(x + 3*width , benchmarks, rotation=45, ha='right')
plt.ylabel("Accuracy (%)")
plt.title("Branch Prediction Accuracy by Benchmark and Size for Tournament Predictor")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(80, 100)  # Set y-limits for better visibility

# Add a legend
plt.legend(title="Sizes", bbox_to_anchor=(1.05, 1), loc='upper left')

# Tight layout and show plot
plt.tight_layout()
plt.savefig(save_dir + "branch_prediction_accuracy_tournament_reduce.png")