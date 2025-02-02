import matplotlib.pyplot as plt
import numpy as np

# Sample data
data = {
    '256+600.perlbench_s-210B': [92.6472],
    '256+602.gcc_s-734B': [94.6666],
    '256+625.x264_s-18B': [87.2027],
    '256+641.leela_s-800B': [83.173],
    '256+648.exchange2_s-1699B': [79.2106],
    '1024+600.perlbench_s-210B': [97.179],
    '1024+602.gcc_s-734B': [94.7056],
    '1024+625.x264_s-18B': [87.7628],
    '1024+641.leela_s-800B': [86.3872],
    '1024+648.exchange2_s-1699B': [81.7015],
    '4096+600.perlbench_s-210B': [97.3323],
    '4096+602.gcc_s-734B': [94.7057],
    '4096+625.x264_s-18B': [88.3935],
    '4096+641.leela_s-800B': [86.9575],
    '4096+648.exchange2_s-1699B': [83.8617],
    '65536+600.perlbench_s-210B': [97.4218],
    '65536+602.gcc_s-734B': [94.7056],
    '65536+625.x264_s-18B': [88.5231],
    '65536+641.leela_s-800B': [87.4292],
    '65536+648.exchange2_s-1699B': [84.0343],
}

# Prepare data for plotting
benchmarks = list(set(key.split('+')[1] for key in data.keys()))
sizes = sorted(set(key.split('+')[0] for key in data.keys()))
accuracies = {size: [data[f"{size}+{b}"][0] for b in benchmarks] for size in sizes}

# Set up bar positions
x = np.arange(len(benchmarks))
width = 0.2  # Width of the bars

# Create the plot
plt.figure(figsize=(12, 7))

for i, size in enumerate(sizes):
    plt.bar(x + i * width, accuracies[size], width=width, label=size)

# Add labels and title
plt.xticks(x + width, benchmarks, rotation=45, ha='right')
plt.ylabel("Accuracy (%)")
plt.title("Branch Prediction Accuracy by Benchmark and Size")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(70, 100)  # Set y-limits for better visibility

# Add a legend
plt.legend(title="Sizes", bbox_to_anchor=(1.05, 1), loc='upper left')

# Tight layout and show plot
plt.tight_layout()
plt.savefig("branch_prediction_accuracy.png")
plt.show()
