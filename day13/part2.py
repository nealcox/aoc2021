import re
import sys
from collections import defaultdict
from itertools import permutations


def main():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):

    dots = []
    dots_s, instrs = input_text.split("\n\n")

    for line in dots_s.split("\n"):
        dot = [int(i) for i in line.split(",")]
        dots.append(dot)

    for instruction in instrs.split("\n"):
        instruction = instruction.split("=")

        xory = instruction[0][-1]
        n = int(instruction[1])
        dots = fold(dots, xory, n)

    max_x, max_y = 0, 0
    for dot in dots:
        if dot[0] > max_x:
            max_x = dot[0]
        if dot[1] > max_y:
            max_y = dot[1]
    width, height = max_x + 1, max_y + 1
    print_paper(dots, height, width)


def fold(dots, xory, n):
    if xory == "x":
        for dot in dots:
            dot[0] = n - abs((n - dot[0]))
    if xory == "y":
        for dot in dots:
            dot[1] = n - abs((n - dot[1]))
    return dots


def print_paper(dots, height, width):
    for r in range(height):
        for c in range(width):
            if [c, r] in dots:
                print("#", end="")
            else:
                print(" ", end="")

        print()
    print()


if __name__ == "__main__":
    exit(main())
