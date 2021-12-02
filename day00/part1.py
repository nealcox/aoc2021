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

    answer = 0
    given = parse(input_text)
    print(given)

    return answer


def parse(s):
    given = None
    # given = partlines(s)
    given = get_one_int_per_line(s)
    # given = get_re(s)
    return given


def partlines(s):
    given = []
    for line in s.split("\n"):
        line = line.strip()
        given.append(line)
    return given


def get_one_int_per_line(s):
    ints = []
    for line in s.split("\n"):
        ints.append(int(line))
    return ints


def get_re(s):
    given = []
    r = re.compile(r"(\w+) (\d+)")
    for m in r.findall(s):
        given.append((m[0], int(m[1])))
    return given


example = """\
X"""


def test_example():
    assert calculate(example) == X


if __name__ == "__main__":
    exit(main())
