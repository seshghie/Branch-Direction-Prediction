import os
import re
import matplotlib.pyplot as plt

# Function to extract misprediction rate for conditional branches
def extract_misprediction_rate(file_content):
    # Search for second occurrence of "BRANCH_CONDITIONAL" in the branch misprediction section
    branch_mispredict_match = re.search(r'Branch misprediction for individual branch types\n.*?BRANCH_CONDITIONAL:\s*\d+\s*([0-9.]+)%', file_content, re.DOTALL)
    if branch_mispredict_match:
        return float(branch_mispredict_match.group(1))
    return None

# Directory where all result files are stored
results_dir = "../results_10M/"

# Benchmark list
benchmarks_list = [
    "600.perlbench_s-210B",
    "602.gcc_s-734B",
    "625.x264_s-18B",
    "641.leela_s-800B",
    "648.exchange2_s-1699B"
]

# Store misprediction rates in array
always_taken = {}
never_taken = {}

# Init arrays with 0 for each benchmark
for benchmark in benchmarks_list:
    always_taken[benchmark] = 0
    never_taken[benchmark] = 0

# Iterate over all result files
for result_file in os.listdir(results_dir):
    if result_file.endswith(".txt"):
        # Determine whether always taken or never taken based on filename
        if "alway" in result_file:
            config = "Always Taken"
        elif "never" in result_file:
            config = "Never Taken"
        else:
            continue
        
        # Extract benchmark name
        benchmark_match = re.match(r'(\d+\.\w+_\w+-\d+B)', result_file)
        if benchmark_match:
            benchmark = benchmark_match.group(1)
        else:
            continue
        
        # Read file content
        with open(os.path.join(results_dir, result_file), 'r') as file:
            content = file.read()
            misprediction_rate = extract_misprediction_rate(content)
            
            # Store misprediction rate based on config
            if misprediction_rate is not None:
                if config == "Always Taken":
                    always_taken[benchmark] = misprediction_rate
                elif config == "Never Taken":
                    never_taken[benchmark] = misprediction_rate


# Create bar chart
x = range(len(benchmarks_list))
width = 0.4 

plt.figure(figsize=(10, 6))

plt.bar(x, [always_taken[b] for b in benchmarks_list], width=width, label="Always Taken", align='center')
plt.bar([i + width for i in x], [never_taken[b] for b in benchmarks_list], width=width, label="Never Taken", align='center')

plt.xticks([i + width/2 for i in x], benchmarks_list, rotation=45, ha="right")
plt.ylabel("Misprediction Rate (%)")
plt.title("Misprediction Rate for Always Taken vs Never Taken Branch Prediction")
plt.legend()

plt.tight_layout()
plt.savefig("shaheen_static_mispred_rates.png")