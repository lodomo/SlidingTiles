#!/bin/bash

command='python slidingtiles.py'
solv_dir='./solvable/'
reports_dir='./reports/'
algos=(1 2)
heuristics=(1 2 3)
rounds=100
size=16

# Create 5 solvable puzzles
echo "Generating $rounds solvable puzzles..." 
$command -g $rounds -s $size

# Put the files in solvable into a list of files
# ??? Are the num of digits for 0-15
files=$(find solvable -type f -name '??????????????????????.txt' -printf "%f\n")

# Create a file in reports called "failed.txt" if it doesnt exist
if [ ! -f $reports_dir"failed.txt" ]; then
    touch $reports_dir"failed.txt"
fi

# Run the tests
for algo in ${algos[@]}; do
    for heuristic in ${heuristics[@]}; do
        for file in $files; do
            echo "$command -a $algo -h $heuristic < $solv_dir$file"
            # Timeout at 20 seconds
            timeout 20 $command -a $algo -H $heuristic < $solv_dir$file
            # If timeout, append previous command to failed.txt
            if [ $? -eq 124 ]; then
                echo "$command -a $algo -h $heuristic < $solv_dir$file" >> $reports_dir"failed.txt"
            fi
        done
    done
done

python3 compile_reports.py 16
echo "All tests completed. Results are in the /results/ directory."
