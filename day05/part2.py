import re
import sys
from collections import Counter
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

    points = defaultdict(int)
    given = get_re(input_text)
    for line in given:
        x1, y1, x2, y2 = line
        if x1 == x2:
            sign_x = 0
        elif x1 > x2:
            sign_x = -1
        else:
            sign_x = 1
        if y1 == y2:
            sign_y = 0
        elif y1 > y2:
            sign_y = -1
        else:
            sign_y = 1
        x = x1
        y = y1
        num_points = max(abs(x2 - x1), abs(y2 - y1)) + 1
        for _ in range(num_points):
            points[x, y] += 1
            x += sign_x
            y += sign_y
    counts = Counter(points.values())
    return len(points.values()) - counts[1]


def get_re(s):
    given = []
    r = re.compile(r"(\d+)")
    for line in s.split("\n"):
        m = [int(i) for i in r.findall(line)]
        given.append(m)
    return given


example = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

example_answer = 12


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
