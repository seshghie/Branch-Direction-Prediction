import os
import re
import matplotlib.pyplot as plt
import numpy as np

save_dir = "/data/home/qvd/Assignments/a2-the-squad/plots/"

# Function to extract accuracy rate from the file content
def extract_accuracy_rate(file_content):
    match = re.search(
        r'Branch Prediction Accuracy:\s*([0-9.]+)%\s*MPKI:\s*([0-9.]+)\s*Average ROB Occupancy at Mispredict:\s*([0-9.]+)', 
        file_content
    )
    if match:
        return float(match.group(1))
    return 0

# Directory where the result files are stored
results_dir = "/data/home/qvd/Assignments/a2-the-squad/results_10M/"

# Benchmark to compare (choose one from the list)
benchmark_to_compare = "648.exchange2_s-1699B"  # Change this if needed

# Predictors, sizes, and their display names
predictors = {
    "vinh_bimodal": "bimodal",
    "shaheen_global": "global fixed CPU bits",
    "shaheen_global_fixGH": "global fixed GH bits"
}
sizes = ["4096", "65536", "1048576", "16777216"]  # 2^12, 2^16, 2^20, 2^24

# Initialize data storage
data = {f"{predictor}+{size}": [] for predictor in predictors for size in sizes}

# Iterate through all files in the directory
for filename in os.listdir(results_dir):
    for predictor in predictors:
        for size in sizes:
            if f"{predictor}_{size}" in filename and benchmark_to_compare in filename:
                file_path = os.path.join(results_dir, filename)

                # Read the content and extract accuracy
                with open(file_path, 'r') as file:
                    content = file.read()
                    accuracy = extract_accuracy_rate(content)
                    data[f"{predictor}+{size}"].append(accuracy)

print(data)  # Verify data extraction

# Prepare data for plotting
sorted_sizes = sorted(sizes, key=int)  # Sort sizes as integers

# Extract accuracies for each predictor and size
accuracies = {
    predictors[predictor]: [data[f"{predictor}+{size}"][0] for size in sorted_sizes]
    for predictor in predictors
}

# Set up bar positions
x = np.arange(len(sorted_sizes))  # One position for each size
width = 0.2  # Width for each bar

# Create the plot
plt.figure(figsize=(10, 6))

# Plot data for each predictor
for i, (predictor_name, accuracy_values) in enumerate(accuracies.items()):
    plt.bar(
        x + i * width, accuracy_values, width=width, 
        label=predictor_name
    )

# Add labels, title, and grid
plt.xticks(x + width, sorted_sizes, rotation=0)
plt.xlabel("Size (log2)")
plt.ylabel("Accuracy (%)")
plt.title(f"Branch Prediction Accuracy Comparison for {benchmark_to_compare}")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(80, 100)  # Set y-limits for better visibility

# Add legend
plt.legend(title="Predictors", bbox_to_anchor=(1.05, 1), loc='upper left')

# Tight layout and save the plot
plt.tight_layout()
plt.savefig(f"{save_dir}branch_prediction_accuracy_{benchmark_to_compare}.png")
plt.show()
