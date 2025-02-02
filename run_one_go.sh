#!/bin/bash
#
#SBATCH --cpus-per-task=8
#SBATCH --time=40:00
#SBATCH --mem=4G

export TRACE_DIR=/data/dpc3_traces/

# List of sizes for shaheen_global
sizes=(4096 65536 1048576)

# List of benchmarks
benchmarks=(
    "600.perlbench_s-210B.champsimtrace.xz"
    "602.gcc_s-734B.champsimtrace.xz"
    "625.x264_s-18B.champsimtrace.xz"
    "641.leela_s-800B.champsimtrace.xz"
    "648.exchange2_s-1699B.champsimtrace.xz"
)

# Build and run for each size
for size in "${sizes[@]}"; do
    # Build the binary
    binary="shaheen_global_fixGH_${size}-no-no-no-no-lru-1core"
    ./build_champsim.sh shaheen_global_fixGH_${size} no no no no lru 1

    # Run the binary on each benchmark
    for benchmark in "${benchmarks[@]}"; do
        ./run_champsim.sh ${binary} 1 10 ${benchmark}
    done
done