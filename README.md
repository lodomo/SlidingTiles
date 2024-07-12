> Author: Lorenzo D. Moon

> Professor: Dr. Anthony Rhodes

> Course: CS-441

> Assignment: Programming Assignment 1 - Sliding Tiles

# Sliding Tiles

## Description

This program is a Sliding Tiles puzzle game solver.
It can use 3 different heuristic functions to solve the puzzle:
- Misplaced Tiles
- Manhattan Distance
- PNLD Distance (Misplaced Tiles + Manhattan Distance)

It can use 2 different search algorithms to solve the puzzle:
- Best First Search
- A* Search

## Modes 

The program has a few different modes, as well as a random generator for
creating guaranted solvable starting points and outputting the results
to a text file that can be piped into the program by using the < operator.

### Generation Mode
```bash
python3 sliding_tiles.py -g <num> [-s <size>]
```

The -g flag sets the mode to generate a random starting point for the puzzle.
The -s flag sets the size of the puzzle. The size must be a perfect square.
The size is optional and defaults to 9. (3x3 puzzle, 8 tiles)

### Solve Mode

If you want to test a specific combination, you can use the solve mode.
```bash
python3 sliding_tiles.py
```

This will prompt you to enter a starting point. 
Format is number separated by spaces, b is the empty tile.

If you want to test a combination that you generated, use the < operator.
```bash 
python3 sliding_tiles.py < test.txt
```

If you want to just run from a random point, use the -r flag.
```bash
python3 sliding_tiles.py -r
```

#### Options for Solve Mode
- -h, --help: Show help message
- -v, --verbose: Show the steps taken to solve the puzzle, use twice for deeper verbosity
- -r, --random: Use a random starting point
- -s, --size: Set the size of the puzzle (Optional, only used for -r flag, and -g flag)
            Size calculated automatically on user input
- -H, --heuristic: Set the heuristic function to use (Optional, defaults to misplaced)
                 1 misplaced
                 2 manhattan, 
                 3 pnld (porque no los dos, misplaced + manhattan)
- -a, --algorithm: Set the search algorithm to use (Optional, defaults to best first)
                 1 best first
                 2 a*

##### Example Usage
```bash
python slidingtiles.py -v -v -r -H 2
```
Verbose Mode 2, Random Starting Point, Heuristic 2 (Manhattan Distance),
Default Algorithm (Best First Search)

## Files

- sliding_tiles.py: The main program
- compile_reports.py: A script to compile the reports into a single file
- /reports: A directory containing the reports for the program
- /solvable: A directory containing solvable starting points for the puzzle (from -g flag)
- run.sh: A script that runs the tests required for the assignment
