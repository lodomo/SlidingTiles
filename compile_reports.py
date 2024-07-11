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

HEURISTICS = ["h1_misplaced", "h2_manhattan", "h3_pnld"]
ALGORITHMS = ["best_first_search", "a_star"]
SIZE = 9


def main():
    main_dir = "./reports"
    time = datetime.datetime.now()
    time = time.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"report_{time}.txt"

    # Create the report file
    with open(f"{main_dir}/{file_name}", "w") as file:
        file.write(f"Report: {time}\n")
        file.write("--------------------\n\n")

    for algorithm in ALGORITHMS:
        for heuristic in HEURISTICS:
            dir = main_dir
            dir += f"/{algorithm}"
            dir += f"_{heuristic}"
            dir += f"_{SIZE}"
            results = ls(dir)
            with open(f"{main_dir}/{file_name}", "a") as file:
                file.write(f"Algorithm: {algorithm}\n")
                file.write(f"Heuristic: {heuristic}\n")
                file.write(f"Size: {SIZE}\n")
                for result in results:
                    file.write(parsed_result(dir, result))
    return


def ls(path):
    return os.listdir(path)


def parsed_result(dir, result):
    # result format is ####_##.txt
    # Get the first up to the _
    puzzle = result.split("_")[0]
    # Get the second up to the .
    moves = result.split("_")[1].split(".")[0]
    print(f"{puzzle} {moves}")
    return "junk"


if __name__ == "__main__":
    main()
