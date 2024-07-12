###############################################################################
#
# Author: Lorenzo D. Moon
# Professor: Anthony Rhodes
# Course: CS-441
# Assignment: Programming Assignment 1
# Description: Compiles the reports needed for the assignment
#
###############################################################################

import datetime
import os
import sys


def main(argv):
    HEURISTICS = ["h1_misplaced", "h2_manhattan", "h3_pnld"]
    ALGORITHMS = ["best_first_search", "a_star"]
    SIZE = 9

    if argv is not None:
        SIZE = int(argv)

    main_dir = "./reports"
    time = datetime.datetime.now()
    time = time.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"report_{time}.txt"
    lazy_file_name = f"report_{time}_simple.txt"

    # Create the report file
    with open(f"{main_dir}/{file_name}", "w") as file:
        file.write(f"Report: {time}\n")
        file.write("--------------------\n\n")

    # Create the lazy report file
    with open(f"{main_dir}/{lazy_file_name}", "w") as file:
        file.write(f"Lazy Report: {time}\n")
        file.write("--------------------\n\n")

    for algorithm in ALGORITHMS:
        for heuristic in HEURISTICS:
            dir = main_dir
            dir += f"/{algorithm}"
            dir += f"_{heuristic}"
            dir += f"_{SIZE}"
            results = ls(dir)
            avg = 0
            with open(f"{main_dir}/{file_name}", "a") as file:
                file.write(f"Algorithm: {format_algorithm(algorithm)}\n")
                file.write(f"Heuristic: {format_heuristic(heuristic)}\n")
                file.write(f"Size: {SIZE}\n")
                sum = 0
                for result in results:
                    parsed = parsed_result(dir, result)
                    sum += int(parsed[1])
                    file.write(f"{parsed[0]}\n")
                avg = sum / len(results)
                file.write(f"Average number of steps: {avg}\n\n")

            # Create a Lazy Report
            with open(f"{main_dir}/{lazy_file_name}", "a") as file:
                file.write(f"Algorithm: {format_algorithm(algorithm)}\n")
                file.write(f"Heuristic: {format_heuristic(heuristic)}\n")
                file.write(f"Size: {SIZE}\n")
                file.write(f"Average number of steps: {avg}\n\n")


    return


def ls(path):
    return os.listdir(path)


def parsed_result(dir, result):
    # result format is ####_##.txt
    # Get the first up to the _
    puzzle = result.split("_")[0]
    # Get the second up to the .
    num_moves = result.split("_")[1].split(".")[0]

    # Read the entire file into a string
    with open(f"{dir}/{result}", "r") as file:
        data = file.read()

    puzzle = f"( {puzzle} )->"

    # Convert ] [ to )->(
    data = data.replace("] [", ")->(")

    # Convert [ to (
    data = data.replace("[", "(")

    # Convert ] to )
    data = data.replace("]", ")")

    return [puzzle + data, num_moves]


def format_algorithm(algorithm):
    if algorithm == "best_first_search":
        return "Best First Search"
    elif algorithm == "a_star":
        return "A*"


def format_heuristic(heuristic):
    if heuristic == "h1_misplaced":
        return "Misplaced Tiles"
    elif heuristic == "h2_manhattan":
        return "Manhattan Distance"
    elif heuristic == "h3_pnld":
        return "PNLD Distance"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        main(None)
    else:
        main(sys.argv[1])
