#!/bin/bash
#
#SBATCH --cpus-per-task=8
#SBATCH --time=40:00
#SBATCH --mem=4G
export TRACE_DIR=/data/dpc3_traces/
binary="vinh_tournament_reduce_16777216-no-no-no-no-lru-1core"
./run_champsim.sh ${binary} 1 10 600.perlbench_s-210B.champsimtrace.xz
./run_champsim.sh ${binary} 1 10 602.gcc_s-734B.champsimtrace.xz
./run_champsim.sh ${binary} 1 10 625.x264_s-18B.champsimtrace.xz
./run_champsim.sh ${binary} 1 10 641.leela_s-800B.champsimtrace.xz
./run_champsim.sh ${binary} 1 10 648.exchange2_s-1699B.champsimtrace.xz
