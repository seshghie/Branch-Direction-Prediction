import matplotlib.pyplot as plt
import pandas as pd

# Function to extract data from the file
def extract_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize variables
    total_branches = 0
    mispredictions = 0

    # Extracting data
    total_branch_direct_jump = int(lines[65].split()[1])
    total_branch_direct_jump_miss = int(lines[74].split()[1])
    total_branch_indirect = int(lines[66].split()[1])
    total_branch_indirect_miss = int(lines[75].split()[1])
    total_branch_condition = int(lines[67].split()[1])
    total_branch_condition_miss = int(lines[76].split()[1])
    total_branch_direct_call = int(lines[68].split()[1])
    total_branch_direct_call_miss = int(lines[77].split()[1])
    total_branch_indirect_call = int(lines[69].split()[1])
    total_branch_indirect_call_miss = int(lines[78].split()[1])
    total_branch_return = int(lines[70].split()[1])
    total_branch_return_miss = int(lines[79].split()[1])
    total_branch_other = int(lines[71].split()[1])
    total_branch_other_miss = int(lines[80].split()[1])

    # Calculate total branches
    total_branches = (
        total_branch_direct_jump +
        total_branch_indirect +
        total_branch_condition +
        total_branch_direct_call +
        total_branch_indirect_call +
        total_branch_return +
        total_branch_other
    )
    total_branches_misses = (
        total_branch_direct_jump_miss +
        total_branch_indirect_miss +
        total_branch_condition_miss +
        total_branch_direct_call_miss +
        total_branch_indirect_call_miss +
        total_branch_return_miss +
        total_branch_other_miss
    )

    # Create a dictionary for the DataFrame row
    data = {
        'Direct Jump': total_branch_direct_jump,
        'Direct Jump Miss': total_branch_direct_jump_miss,
        'Indirect': total_branch_indirect,
        'Indirect Miss': total_branch_indirect_miss,
        'Conditional': total_branch_condition,
        'Conditional Miss': total_branch_condition_miss,
        'Direct Call': total_branch_direct_call,
        'Direct Call Miss': total_branch_direct_call_miss,
        'Indirect Call': total_branch_indirect_call,
        'Indirect Call Miss': total_branch_indirect_call_miss,
        'Return': total_branch_return,
        'Return Miss': total_branch_return_miss,
        'Other': total_branch_other,
        'Other Miss': total_branch_other_miss,
        'Total': total_branches,
        'Total Misses': total_branches_misses
    }

    # Create a DataFrame
    df = pd.DataFrame([data])
    return df

# File path
file_path = 'results_10M/600.perlbench_s-210B.champsimtrace.xz-vinh_alwayTaken-no-no-no-no-lru-1core.txt'

# Extract data
df = extract_data(file_path)
print(df)
