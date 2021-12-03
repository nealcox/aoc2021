import sys
from collections import defaultdict


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "input.txt"
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):

    answer = 0
    given = partlines(input_text)
    num_lines = len(given)
    ones = defaultdict(int)
    for line in given:
        for i, digit in enumerate(line):
            if digit == "1":
                ones[i] += 1

    s = ""
    for i in range(len(given[0])):
        if ones[i] > num_lines / 2:
            s = s + "1"
        elif ones[i] < num_lines / 2:
            s = s + "0"
        else:
            raise ValueError("equal")
    gamma = int(s, 2)
    epsilon = 2 ** len(s) - gamma - 1
    answer = gamma * epsilon

    return answer


def partlines(s):
    given = []
    for line in s.split("\n"):
        line = line.strip()
        given.append(line)
    return given


example = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


def test_example():
    assert calculate(example) == 198


if __name__ == "__main__":
    exit(main())
