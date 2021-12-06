import re
import sys
from collections import defaultdict
from itertools import permutations

DAYS = 80
PERIOD = 7


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "input.txt"
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text, days=DAYS):

    answer = 0
    fish = get_re(input_text)
    for day in range(days):
        fish = [f - 1 for f in fish]
        new_fish = 0
        for i, f in enumerate(fish):
            if f < 0:
                fish[i] = PERIOD - 1
                new_fish += 1
        for i in range(new_fish):
            fish.append(PERIOD - 1 + 2)

    return len(fish)


def get_re(s):
    given = []
    r = re.compile(r"(\d+)")
    m = r.findall(s)
    return [int(i) for i in m]


example = """\
3,4,3,1,2"""

example_answer1 = 26
example_answer2 = 5934


def test_example():
    assert calculate(example, 18) == example_answer1
    assert calculate(example) == example_answer2


if __name__ == "__main__":
    exit(main())
