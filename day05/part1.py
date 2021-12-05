import re
import sys
from collections import Counter
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

    points = defaultdict(int)
    given = get_re(input_text)
    for line in given:
        x1, y1, x2, y2 = line
        if x1 != x2 and y1 != y2:
            continue
        else:
            if x1 > x2 or y1 > y2:
                sign = -1
            else:
                sign = 1
            for x in range(x1, x2 + sign, sign):
                for y in range(y1, y2 + sign, sign):
                    points[x, y] += 1

    counts = Counter(points.values())
    return len(points.values()) - counts[1]


def get_re(s):
    given = []
    r = re.compile(r"(\d+)")
    for line in s.split("\n"):
        print(line)
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

example_answer = 5


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
