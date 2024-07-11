#!/bin/bash

command='python slidingtiles.py -a1 -H1 -r'
algos=(1)
heuristics=(1 2)
rounds=5

for round in $(seq 1 $rounds)
do
    for algo in ${algos[@]}
    do
        for heuristic in ${heuristics[@]}
        do
            $command -a $algo -H $heuristic -r
        done
    done
done




