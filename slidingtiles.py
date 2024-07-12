###############################################################################
#
# Author: Lorenzo D. Moon
# Professor: Dr. Anthony Rhodes
# Course: CS-441
# Assignment: Programming Assignment 1
# Description: Solves the Sliding Tiles problem using 3 different heuristic
#              functions: Manhattan Distance, Misplaced Tiles, and TBD.
#              The program uses the A* algorithm to find the optimal solution.
#              As well as the Best-First Search algorithm to find a solution
#              For how to use, please read README.md
#
###############################################################################

import getopt
import heapq
import os
import sys

import numpy as np

SETTINGS = {}  # Global settings dictionary


def main(argv):
    process_command_line(argv)
    puzzle = set_puzzle()
    solution = get_solution(puzzle)
    show_solution(solution)  # If verbose is set
    generate_report(puzzle, solution)  # Generate data file of the solution
    exit(0)


def process_command_line(argv):
    options = "hvsrH:a:g:"
    DEFAULT_SIZE = 9
    HEURISTICS = [h1_misplaced, h2_manhattan, h3_pnld]
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
                perror(f"Invalid heuristic: {arg}")
                help_simple()
                perror("Run with -h for help")
                sys.exit(2)
            SETTINGS["Heuristic"] = HEURISTICS[heuristic - 1]
        elif opt in ("-a", "--algorithm"):
            algorithm = int(arg)
            if algorithm < 1 or algorithm > len(ALGORITHMS):
                perror(f"Invalid algorithm: {arg}")
                help_simple()
                perror("Run with -h for help")
                sys.exit(2)
            SETTINGS["Algorithm"] = ALGORITHMS[algorithm - 1]
        elif opt in ("-g", "--generate"):
            generate_solvable(int(arg))
            exit(0)

    setup_after_command_line()
    return


def setup_after_command_line():
    SETTINGS["matrix_dim"] = int(SETTINGS["size"] ** 0.5)

    if SETTINGS["matrix_dim"] ** 2 != SETTINGS["size"]:
        perror("Invalid size: Size is not a square number")
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
    perror("Usage: slidingtiles.py [OPTIONS]")
    perror("Options:")
    perror("  -h, --help\t\t\t\tShow this help message")
    perror("  -v, --verbose\t\t\t\tIncrease verbosity (up to 2 times)")
    perror("  -r, --random\t\t\t\tGenerate a random puzzle")
    perror("  -s, --size [N]\t\t\tSet the size of the puzzle (default 9)")
    perror("  -H, --heuristic [1,2,3]\t\tChoose the heuristic function")
    perror("      1: Misplaced Tiles (default)")
    perror("      2: Manhattan Distance")
    perror("      3: TBD")
    perror("  -a, --algorithm [1,2]\t\tChoose the algorithm")
    perror("      1: Best-First Search (default)")
    perror("      2: A* algorithm")
    perror("Example: slidingtiles.py -v -v -r -H 2")
    perror("Verbose:2, Random puzzle, Manhattan Distance, Best-First Search")
    perror("Supports < some_puzzle.txt for input")
    exit(0)


def help_simple():
    perror("Usage: slidingtiles.py [OPTIONS] See -h for full options")
    pass


def verbose(message, level=1):
    if SETTINGS["verbose"] >= level:
        perror(message)


def perror(message):
    sys.stderr.write(message)


def get_solution(puzzle):
    # Grab the algorithm from the settings and run it
    # For the args, we pass the puzzle, the solved state, and the heuristic
    # These are all generated from process_command_line
    return SETTINGS["Algorithm"](puzzle, SETTINGS["solve_state"], SETTINGS["Heuristic"])


def show_solution(solution):
    # Show the solution to the user and final step count if verbose is on
    if SETTINGS["verbose"] > 1:
        for step in solution:
            print(f"{b_replace(step)}")
        print(f"Total Steps: {len(solution)}")
    return


def set_puzzle():
    # Set the puzzle based on the settings
    if SETTINGS["random"]:
        return random_puzzle(SETTINGS["size"])

    puzzle = user_puzzle()

    if solvable(puzzle) is False:
        perror("The puzzle is not solvable. Exiting...")
        exit(1)

    return puzzle


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
        perror("Invalid puzzle: Puzzle is not a square")
        exit(1)

    # Check if the input is a permutation of the numbers 0 to n
    if sorted(puzzle) != list(range(len(puzzle))):
        perror("Invalid puzzle: Not a permutation of b, 1 to n")
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
    return misplaced


def h2_manhattan(puzzle):
    distance = 0
    matrix_dim = int(len(puzzle) ** 0.5)
    verbose("(COL,ROW) -> (COL,ROW)\n", 2)
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


def h3_pnld(puzzle):
    # My Heuristic "Porque No Los Dos" PNLD
    # Combines Misplaced Tiles and Manhattan Distance
    misplaced = h1_misplaced(puzzle)
    manhattan = h2_manhattan(puzzle)
    pnld = misplaced + manhattan
    verbose(f"PNLD: {pnld}\n")
    return pnld


def b_replace(puzzle, as_matrix=False):
    # This will replace the 0 with a b
    # If as_matrix is True, the puzzle will be perrored as a matrix
    # This helps with trouble shooting and debugging to make
    # sure the moves are happening properly
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
    # This returns all legal moves. It does not account for any heuristics.
    # It simply returns all the possible moves that can be made from this
    # Position
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


def solved_state():
    # Returns the solved state of the puzzle.
    # Not hardcoded to support different sizes for the puzzle
    solved = np.array(range(1, SETTINGS["size"] + 1))
    solved[SETTINGS["size"] - 1] = 0
    return solved


def lazy_hash(puzzle):
    str = ""
    for i in range(len(puzzle)):
        str += "{:02d}".format(puzzle[i])
    return str


def generate_report(puzzle, solution):
    dir = "./reports"
    dir += f"/{SETTINGS['Algorithm'].__name__}"
    dir += f"_{SETTINGS['Heuristic'].__name__}"
    dir += f"_{SETTINGS['size']}"
    if not os.path.exists(dir):
        os.makedirs(dir)

    filename = f"{b_replace(puzzle)}"
    # Remove all excess characters
    filename = filename.replace("[", "")
    filename = filename.replace("]", "")
    filename = filename.replace(" ", "")

    steps = len(solution)

    filename = dir + f"/{filename}_{steps}.txt"

    with open(filename, "w") as f:
        f.write(f"{b_replace(puzzle)} ")
        for step in solution:
            f.write(f"{b_replace(step)} ")

    # Print to stderr
    sys.stderr.write(f"Report generated: {filename}\n")
    return


def generate_solvable(n):
    # Create directory called "solvable" if it doesn't exist
    if not os.path.exists("solvable"):
        os.makedirs("solvable")

    # Create n solvable puzzles
    for i in range(n):
        puzzle = random_puzzle(SETTINGS["size"])

        # Write the puzzle to a file
        text = f"{b_replace(puzzle)}"
        # remove the brackets
        text = text.replace("[", "")
        text = text.replace("]", "")

        title = text.replace(" ", "")

        # check if title already exists
        if os.path.exists(f"solvable/{title}.txt"):
            i -= 1
            continue

        with open(f"solvable/{title}.txt", "w") as f:
            f.write(text)
            f.write("\n")


def best_first_search(puzzle, solve_state, h_func):
    # Best First Search will use the heuristic to determine the best
    # next move to take. It will keep making the best move until it
    # finds a solution. This is a guaranteed result, but not the shortest
    # path since it doesn't take steps into account.

    start_state = puzzle
    visited = {}

    # Create the initial node
    root = Node(start_state, h_func(start_state))

    # Create a queue of nodes to visit
    frontier = [root]
    heapq.heapify(frontier)

    # While there are still nodes to visit, keep going
    while len(frontier) > 0:
        # Get the node with the lowest heuristic value
        # The f == h for this algorithm.
        node = heapq.heappop(frontier)

        # Check if the node is the solution
        if lazy_hash(node.state) == lazy_hash(solve_state):
            solution = []
            while node is not None:
                solution.insert(0, node.state)
                node = node.parent
            return solution

        # Add the node to the visited list
        visited[lazy_hash(node.state)] = node.f

        # Get all the legal moves
        moves = legal_moves(node.state)

        # Create the new nodes
        for move in moves:
            new_node = Node(move, h_func(move), node)
            if lazy_hash(new_node.state) not in visited:
                heapq.heappush(frontier, new_node)


def a_star(puzzle, solve_state, h_func):
    # A* is uses most of the same code as Best First Search, but it
    # takes into account the steps taken to get to the current state.
    # This will guarantee the shortest path to the solution, but might take
    # longer to find the solution

    start_state = puzzle
    visited = {}

    # Create the initial node
    root = Node(start_state, h_func(start_state), g=0)

    # Create a queue of nodes to visit
    frontier = [root]
    heapq.heapify(frontier)

    # While there are still nodes to visit, keep going
    while len(frontier) > 0:
        # Get the node with the lowest f value (g + h)
        node = heapq.heappop(frontier)

        # Check if the node is the solution
        if lazy_hash(node.state) == lazy_hash(solve_state):
            solution = []
            while node is not None:
                solution.insert(0, node.state)
                node = node.parent
            return solution

        # Add the node to the visited list
        visited[lazy_hash(node.state)] = node.f

        # Get all the legal moves
        moves = legal_moves(node.state)

        # Create the new nodes
        for move in moves:
            new_node = Node(move, h_func(move), node, node.g + 1)
            if lazy_hash(new_node.state) not in visited:
                heapq.heappush(frontier, new_node)
            elif visited[lazy_hash(new_node.state)] > node.f:
                heapq.heappush(frontier, new_node)

    return None


class Node:
    def __init__(self, state, h, parent=None, g=0):
        self.parent = parent
        self.state = state
        self.h = h
        self.g = g
        self.f = g + h
        return

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.state == other.state

    def __lte__(self, other):
        return self.f <= other.f

    def __gt__(self, other):
        return self.f > other.f

    def __gte__(self, other):
        return self.f >= other.f


if __name__ == "__main__":
    main(sys.argv[1:])
