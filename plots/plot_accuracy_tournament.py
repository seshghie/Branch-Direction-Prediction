import os
import re
import matplotlib.pyplot as plt
import numpy as np

save_dir = "/data/home/qvd/Assignments/a2-the-squad/plots/"

def extract_accuracy_rate(file_content):
    match = re.search(r'Branch Prediction Accuracy:\s*([0-9.]+)%\s*MPKI:\s*([0-9.]+)\s*Average ROB Occupancy at Mispredict:\s*([0-9.]+)', file_content)
    if match:
        accuracy = float(match.group(1))
        return accuracy
    return 0

results_dir = "/data/home/qvd/Assignments/a2-the-squad/results_10M/"

benchmarks_list = [
    "600.perlbench_s-210B",
    "602.gcc_s-734B",
    "625.x264_s-18B",
    "641.leela_s-800B",
    "648.exchange2_s-1699B"
]

# Original predictor names
predictors = [
    "vinh_bimodal",
    "shaheen_local_fixPC",
    "shaheen_global",
    "vinh_tournament"
]

# Mapping of original to display-friendly names
predictor_labels = {
    "vinh_bimodal": "Bimodal",
    "shaheen_local_fixPC": "Local fix PC",
    "shaheen_global": "Global fix PC",
    "vinh_tournament": "Tournament"
}

data = {f"{predictor}": {b: 0 for b in benchmarks_list} for predictor in predictors}

for filename in os.listdir(results_dir):
    for predictor in predictors:
        if f'{predictor}_4096' in filename:
            file_path = os.path.join(results_dir, filename)
            benchmark_match = re.match(r'(\d+\.\w+_\w+-\d+B)', filename)
            if benchmark_match:
                benchmark = benchmark_match.group(1)
                if benchmark in benchmarks_list:
                    with open(file_path, 'r') as file:
                        content = file.read()
                        accuracy = extract_accuracy_rate(content)
                        data[predictor][benchmark] = accuracy

plt.figure(figsize=(12, 7))
x = np.arange(len(benchmarks_list))
width = 0.2

for i, predictor in enumerate(predictors):
    accuracies = [data[predictor][b] for b in benchmarks_list]
    plt.bar(x + i * width, accuracies, width=width, label=predictor_labels[predictor])

plt.xlabel("Benchmarks")
plt.ylabel("Accuracy (%)")
plt.title("Branch Prediction Accuracy by Benchmark and Predictor")
plt.xticks(x + 1.5 * width, benchmarks_list, rotation=45, ha='right')
plt.legend(title="Predictors", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(80, 100)

plt.tight_layout()
plt.savefig(os.path.join(save_dir, "Compare_with_tournament.png"))
