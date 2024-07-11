###############################################################################
#
# Author: Lorenzo D. Moon
# Professor: Anthony Rhodes
# Course: CS-441
# Assignment: Programming Assignment 1
# Description: Solves the Sliding Tiles problem using 3 different heuristic
#              functions: Manhattan Distance, Misplaced Tiles, and TBD.
#              The program uses the A* algorithm to find the optimal solution.
#              As well as the Best-First Search algorithm to find a solution
#              For how to use, please read README.md
#
###############################################################################

import datetime
import getopt
import os
import sys
import re

import numpy as np

SETTINGS = {}
MATRIX_DIM = 3


def main(argv):
    sys.setrecursionlimit(10000)
    process_command_line(argv)
    puzzle = set_puzzle()

    verbose(f"Starting Search\n", 2)
    verbose(f"Start State: {b_replace(puzzle)}\n")

    previous_states = {}
    solution = SETTINGS["Algorithm"](puzzle, previous_states)
    if solution is None:
        print("No solution found")
    else:
        generate_report(puzzle, solution)
    exit(0)


def set_puzzle():
    if SETTINGS["random"]:
        return random_puzzle(SETTINGS["size"])

    puzzle = user_puzzle()

    if solvable(puzzle) is False:
        print("The puzzle is not solvable. Exiting...")
        exit(1)

    return puzzle


def process_command_line(argv):
    options = "hvsrH:a:"
    DEFAULT_SIZE = 9
    HEURISTICS = [h1_misplaced, h2_manhattan, h3_tbd]
    ALGORITHMS = [best_first_search, a_star]
    SETTINGS["verbose"] = 0  # Verbose mode
    SETTINGS["random"] = False  # Random mode
    SETTINGS["size"] = DEFAULT_SIZE  # Size of the puzzle
    SETTINGS["Heuristic"] = None  # Heuristic mode
    SETTINGS["Algorithm"] = None  # Algorithm mode
    SETTINGS["solve_state"] = solved_state()

    try:
        opts, args = getopt.getopt(argv, options)
    except getopt.GetoptError:
        help_simple()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            help()
            sys.exit()
        elif opt in ("-v", "--verbose"):
            SETTINGS["verbose"] += 1
            verbose(f"Verbose mode: {SETTINGS['verbose']}\n")
        elif opt in ("-r", "--random"):
            SETTINGS["random"] = True
        elif opt in ("-s", "--size"):
            SETTINGS["size"] = int(arg)
            SETTINGS["solve_state"] = solved_state()
        elif opt in ("-H", "--heuristic"):
            heuristic = int(arg)
            if heuristic < 1 or heuristic > len(HEURISTICS):
                print(f"Invalid heuristic: {arg}")
                help_simple()
                print("Run with -h for help")
                sys.exit(2)
            SETTINGS["Heuristic"] = HEURISTICS[heuristic - 1]
        elif opt in ("-a", "--algorithm"):
            algorithm = int(arg)
            if algorithm < 1 or algorithm > len(ALGORITHMS):
                print(f"Invalid algorithm: {arg}")
                help_simple()
                print("Run with -h for help")
                sys.exit(2)
            SETTINGS["Algorithm"] = ALGORITHMS[algorithm - 1]

    SETTINGS["matrix_dim"] = int(SETTINGS["size"] ** 0.5)
    verbose(f"Size: {SETTINGS['size']}\n")

    if SETTINGS["matrix_dim"] ** 2 != SETTINGS["size"]:
        print("Invalid size: Size is not a square number")
        exit(1)

    if SETTINGS["Heuristic"] is None:
        SETTINGS["Heuristic"] = h1_misplaced

    if SETTINGS["Algorithm"] is None:
        SETTINGS["Algorithm"] = best_first_search

    verbose("Settings:\n")
    verbose(f"Verbose: {SETTINGS['verbose']}\n")
    verbose(f"Random: {SETTINGS['random']}\n")
    verbose(f"Size: {SETTINGS['size']}\n")
    verbose(f"Heuristic: {SETTINGS['Heuristic'].__name__}\n")
    verbose(f"Algorithm: {SETTINGS['Algorithm'].__name__}\n")
    verbose(f"Solve State: {b_replace(SETTINGS['solve_state'])}\n")
    return


def help():
    print("Usage: slidingtiles.py [OPTIONS]")
    print("Options:")
    print("  -h, --help\t\t\t\tShow this help message")
    print("  -v, --verbose\t\t\t\tIncrease verbosity (up to 2 times)")
    print("  -r, --random\t\t\t\tGenerate a random puzzle")
    print("  -s, --size [N]\t\t\tSet the size of the puzzle (default 9)")
    print("  -H, --heuristic [1,2,3]\t\tChoose the heuristic function")
    print("      1: Misplaced Tiles (default)")
    print("      2: Manhattan Distance")
    print("      3: TBD")
    print("  -a, --algorithm [1,2]\t\tChoose the algorithm")
    print("      1: Best-First Search (default)")
    print("      2: A* algorithm")
    print("Example: slidingtiles.py -v -v -r -H 2")
    print("Verbose:2, Random puzzle, Manhattan Distance, Best-First Search")
    print("Supports < some_puzzle.txt for input")
    exit(0)


def help_simple():
    print("Usage: slidingtiles.py [OPTIONS] See -h for full options")
    pass


def verbose(message, level=1):
    if SETTINGS["verbose"] >= level:
        sys.stderr.write(message)


def random_puzzle(size):
    puzzle = np.random.permutation(size)
    verbose(f"Random puzzle: {b_replace(puzzle)}\n")

    while solvable(puzzle) is False:
        verbose("Unsolvable Reshuffling puzzle\n")
        puzzle = np.random.permutation(size)
        verbose(f"Random puzzle: {b_replace(puzzle)}\n")
    return puzzle


def user_puzzle():
    user_input = input("Enter the puzzle: ")

    # If one input is b convert it to 0
    user_input = user_input.replace("b", "0")

    # Split the input by spaces into a python list
    puzzle = np.array([int(x) for x in user_input.split()])

    # Check if the input is a square number
    if int(len(puzzle) ** 0.5) ** 2 != len(puzzle):
        print("Invalid puzzle: Puzzle is not a square")
        exit(1)

    # Check if the input is a permutation of the numbers 0 to n
    if sorted(puzzle) != list(range(len(puzzle))):
        print("Invalid puzzle: Not a permutation of b, 1 to n")
        exit(1)

    # Update global settings
    SETTINGS["size"] = len(puzzle)
    SETTINGS["matrix_dim"] = int(len(puzzle) ** 0.5)
    SETTINGS["solve_state"] = solved_state()
    verbose(f"\nUser puzzle: {b_replace(puzzle)}\n")
    verbose(f"Size: {SETTINGS['size']}\n")
    verbose(f"Matrix Dim: {SETTINGS['matrix_dim']}\n")
    verbose(f"Solve State: {b_replace(SETTINGS['solve_state'])}\n")
    return puzzle


def solvable(puzzle):
    verbose("Start Solvable\n", 2)
    # Count the number of inversions
    # If the number of inversons is even, the puzzle is solvable
    inversions = 0
    for i in range(len(puzzle)):
        if puzzle[i] == 0:
            continue
        for j in range(i + 1, len(puzzle)):
            if puzzle[j] == 0:
                continue
            if puzzle[i] > puzzle[j]:
                inversions += 1
                verbose(f"({puzzle[i]},{puzzle[j]}) ", 2)

    can_solve = inversions % 2 == 0
    verbose(f"\nInversions: {inversions}\n", 2)
    verbose(f"Solvable: {can_solve}\n", 2)
    verbose("End Solvable\n", 2)
    return can_solve


def h1_misplaced(puzzle):
    verbose("Start Misplaced Tiles\n", 2)
    misplaced = 0
    for i in range(len(puzzle)):
        # Don't count the blank tile
        if puzzle[i] == 0:
            continue
        # Check if the tile is in the correct position
        # Since 0th spot is 1, 1st spot is 2, etc.
        # Add 1 to i to get the correct value of the tile
        if puzzle[i] != i + 1:
            misplaced += 1
            verbose(f"{puzzle[i]} ", 2)
    verbose(f"Misplaced tiles: {misplaced}\n")
    verbose("End Misplaced Tiles\n", 2)
    return misplaced


def h2_manhattan(puzzle):
    verbose("Start Manhattan Distance\n", 2)
    distance = 0
    verbose("(COL,ROW) -> (COL,ROW)\n", 2)
    matrix_dim = int(len(puzzle) ** 0.5)
    for i in range(len(puzzle)):
        if puzzle[i] == 0:
            continue
        cur_distance = 0
        cur_num = puzzle[i]
        cur_row = i // matrix_dim
        cur_col = i % matrix_dim
        pref_row = (cur_num - 1) // matrix_dim
        pref_col = (cur_num - 1) % matrix_dim
        cur_distance = abs(cur_row - pref_row) + abs(cur_col - pref_col)
        distance += cur_distance
        verbose(f"{cur_num}@({cur_col + 1},{cur_row + 1})", 2)
        verbose(f"->({pref_col + 1},{pref_row + 1})", 2)
        verbose(f" Distance: {cur_distance}\n", 2)

    verbose(f"Manhattan Distance: {distance}\n")
    return distance


def h3_tbd(puzzle):
    pass


def b_replace(puzzle, as_matrix=False):
    if as_matrix:
        dim = SETTINGS["matrix_dim"]
        string = ""
        for i in range(len(puzzle)):
            if puzzle[i] == 0:
                string += "b "
            else:
                string += str(puzzle[i]) + " "
            if (i + 1) % dim == 0:
                string += "\n"
        return string

    string = "[ "
    for i in range(len(puzzle)):
        if puzzle[i] == 0:
            string += "b "
        else:
            string += str(puzzle[i]) + " "
    string += "]"
    return string


def legal_moves(puzzle):
    dim = SETTINGS["matrix_dim"]
    moves = []
    # Find all the combinations of the puzzle for a single move
    verbose("Start Legal Moves\n", 2)
    verbose("Legal Moves: \n", 2)
    for i in range(len(puzzle)):
        if puzzle[i] == 0:
            row = i // dim
            col = i % dim
            verbose(f"Blank tile: ({col + 1},{row + 1})\n", 2)

            if row > 0:
                verbose(f"Move up: ({col + 1},{row})\n", 2)
                move = puzzle.copy()
                move[i] = move[i - dim]
                move[i - dim] = 0
                moves.append(move)
            if row < dim - 1:
                verbose(f"Move down: ({col + 1},{row + 2})\n", 2)
                move = puzzle.copy()
                move[i] = move[i + dim]
                move[i + dim] = 0
                moves.append(move)
            if col > 0:
                verbose(f"Move left: ({col},{row + 1})\n", 2)
                move = puzzle.copy()
                move[i] = move[i - 1]
                move[i - 1] = 0
                moves.append(move)
            if col < dim - 1:
                verbose(f"Move right: ({col + 2},{row + 1})\n", 2)
                move = puzzle.copy()
                move[i] = move[i + 1]
                move[i + 1] = 0
                moves.append(move)

    verbose(f"Total moves: {len(moves)}\n", 2)
    verbose(f"Start State: \n{b_replace(puzzle, True)}\n", 2)
    for move in moves:
        verbose(f"{b_replace(move, True)}\n", 2)
    verbose("End Legal Moves\n", 2)
    return moves


def a_star(puzzle):
    print("A* Not implemented")
    pass


def best_first_search(puzzle, previous_states):
    # Base Case Return the Solved State
    h_val = SETTINGS["Heuristic"](puzzle)
    if h_val == 0:
        # An empty list is returned to signal the end of the solution
        return []

    # Otherwise we need to store the solution on the way back
    solution = []
    previous_states[bad_hash(puzzle)] = True
    moves = legal_moves(puzzle)
    m_h = []
    for move in moves:
        m_h.append([SETTINGS["Heuristic"](move), move])

    # sort by heuristic
    m_h.sort(key=lambda x: x[0])

    verbose("Start Best-First Search\n", 2)
    verbose(f"Start State: \n{b_replace(puzzle)}\n", 2)
    verbose(f"Start Heuristic: {h_val}\n", 2)
    verbose(f"Moves: {len(moves)}\n", 2)
    verbose("Moves: \n", 2)
    for move in m_h:
        verbose(f"{b_replace(move[1])} Heuristic: {move[0]}\n", 2)

    for move in m_h:
        if bad_hash(move[1]) in previous_states:
            continue

        verbose(f"Move: {b_replace(move[1])}\n", 2)

        temp = best_first_search(move[1], previous_states)
        if temp is not None:
            solution = [move[1]] + temp
            return solution

    # No solution found
    return None


def solved_state():
    solved = np.array(range(1, SETTINGS["size"] + 1))
    solved[SETTINGS["size"] - 1] = 0
    return solved


def bad_hash(puzzle):
    str = ""
    for i in range(len(puzzle)):
        str += "{:02d}".format(puzzle[i])
    return str


def generate_report(puzzle, solution):
    name_of_algorithm = SETTINGS["Algorithm"].__name__
    name_of_heuristic = SETTINGS["Heuristic"].__name__

    if name_of_algorithm == "best_first_search":
        name_of_algorithm = "Best-First Search"
    else:
        name_of_algorithm = "A* Algorithm"

    if name_of_heuristic == "h1_misplaced":
        name_of_heuristic = "Misplaced Tiles"
    elif name_of_heuristic == "h2_manhattan":
        name_of_heuristic = "Manhattan Distance"
    else:
        name_of_heuristic = "TBD"

    # Create the directory if it doesn't exist
    directory = "./reports/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the file if it doesn't exist
    noa = name_of_algorithm.replace(" ", "_")
    noh = name_of_heuristic.replace(" ", "_")
    file_name = f"{directory}{noa}_{noh}.txt"

    if not os.path.exists(file_name):
        header = f"Algorithm: {name_of_algorithm}\n"
        header += f"Heuristic: {name_of_heuristic}\n"
        with open(file_name, "w") as file:
            file.write(header)

    string = f"{len(solution)}: \t"
    puzzle_as_string = b_replace(puzzle)
    puzzle_as_string = puzzle_as_string.replace("\n", "_")
    puzzle_as_string = puzzle_as_string.replace(" ", "")
    puzzle_as_string = puzzle_as_string.replace("[", "")
    puzzle_as_string = puzzle_as_string.replace("]", "")
    string += f"{puzzle_as_string} -> "
    for state in solution:
        string += f"{b_replace(state)}->"
    string = string[:-2] + "\n"

    # Append to the file 
    with open(file_name, "a") as file:
        file.write(string)


if __name__ == "__main__":
    main(sys.argv[1:])
