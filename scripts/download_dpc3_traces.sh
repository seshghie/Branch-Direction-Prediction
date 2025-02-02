#!/bin/bash

mkdir -p $PWD/../dpc3_traces
while read LINE
do
    aria2c -x 16 -s 16 -d $PWD/../dpc3_traces -c http://hpca23.cse.tamu.edu/champsim-traces/speccpu/$LINE
done < dpc3_max_simpoint.txt
