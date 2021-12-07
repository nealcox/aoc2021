import re
import sys
from collections import defaultdict
from itertools import permutations


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "input.txt"
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):

    fuel = float("inf")
    crabs = get_re(input_text)
    for i in range(min(crabs), max(crabs) + 1):
        f = fuel_for_pos(crabs, i)
        fuel = min(fuel, f)

    return fuel


def fuel_for_pos(crabs, pos):
    return sum(abs(c - pos) for c in crabs)


def get_re(s):
    crabs = []
    r = re.compile(r"(\d+)")
    return [int(i) for i in r.findall(s)]


example = """\
16,1,2,0,4,2,7,1,2,14"""

example_answer = 37


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
