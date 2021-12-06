import re
import sys
from collections import Counter
from collections import defaultdict


DAYS = 256
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

    start_fish = get_re(input_text)
    fish = Counter(start_fish)
    for day in range(days):
        next_fish = defaultdict(int)
        for f in range(PERIOD + 2):
            next_fish[f] += fish[f + 1]
        next_fish[6] += fish[0]
        next_fish[8] += fish[0]
        fish = next_fish

    return sum(fish.values())


def get_re(s):
    given = []
    r = re.compile(r"(\d+)")
    m = r.findall(s)
    return [int(i) for i in m]


example = """\
3,4,3,1,2"""

example_answer = 26984457539


def test_example():
    assert calculate(example, 256) == example_answer


if __name__ == "__main__":
    exit(main())
