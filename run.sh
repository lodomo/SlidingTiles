#!/bin/bash

command='python slidingtiles.py'
solv_dir='./solvable/'
algos=(1 2)
heuristics=(1 2 3)
rounds=5

echo "If you run into errors, try pipenv shell before running"

echo "This will destroy the files in /solvable/ and /reports/"
echo "are you sure?"
read -p "Press [Enter] to continue or [Ctrl+C] to cancel..."

rm -rf solvable
rm -rf reports

# Create 5 solvable puzzles
echo "Generating $rounds solvable puzzles..." 
$command -g $rounds

# Put the files in solvable into a list of files
files=$(find solvable -type f -name '?????????.txt' -printf "%f\n")

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

python3 compile_reports.py
# Now run 5 4x4 puzzles 
size=16

echo "Generating $rounds solvable puzzles of size $size..."
$command -g $rounds -s $size

# Put the files in solvable into a list of files
# ??? Are the num of digits for 0-15
files=$(find solvable -type f -name '??????????????????????.txt' -printf "%f\n")

# Run the tests
for algo in ${algos[@]}; do
    for heuristic in ${heuristics[@]}; do
        for file in $files; do
            echo "$command -a $algo -h $heuristic < $solv_dir$file"
            $command -a $algo -H $heuristic < $solv_dir$file
        done
    done
done

python3 compile_reports.py 16
echo "All tests completed. Results are in the /results/ directory."

