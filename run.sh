#!/bin/bash

command='python slidingtiles.py'
solv_dir='./solvable/'
algos=(1 2)
heuristics=(1 2 3)
rounds=5

pipenv shell

echo "This will destroy the files in /solvable/ are you sure?"
read -p "Press [Enter] to continue or [Ctrl+C] to cancel..."

rm -rf solvable

# Create 5 solvable puzzles
echo "Generating $rounds solvable puzzles..." 
$command -g $rounds

# Put the files in solvable into a list of files
files=$(ls solvable)

echo $files

# Run the tests
for algo in ${algos[@]}; do
    for heuristic in ${heuristics[@]}; do
        for file in $files; do
            echo "$command -a $algo -h $heuristic < $solv_dir$file"
            $command -a $algo -H $heuristic < $solv_dir$file
        done
    done
done

echo "All tests completed. Results are in the /results/ directory."
