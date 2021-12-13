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
        break

    max_x, max_y = 0, 0
    for dot in dots:
        if dot[0] > max_x:
            max_x = dot[0]
        if dot[1] > max_y:
            max_y = dot[1]
    width, height = max_x + 1, max_y + 1
    s = set()
    for dot in dots:
        s.add(tuple(dot))
    return len(s)


def fold(dots, xory, n):
    if xory == "x":
        for dot in dots:
            dot[0] = n - abs((n - dot[0]))
    if xory == "y":
        for dot in dots:
            dot[1] = n - abs((n - dot[1]))
    return dots


example = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

example_answer = 17


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
