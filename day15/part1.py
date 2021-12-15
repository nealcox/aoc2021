import sys
from collections import defaultdict


def main():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):

    answer = 0
    area, height, width = get_map(input_text)
    best = defaultdict(lambda: float("inf"))

    best[0, 0] = 0
    todo = neighbours(0, 0)
    while todo:
        r, c = todo.pop(0)
        possible = area[r, c] + min(best[p] for p in neighbours(r, c))
        if possible < best[r, c]:
            best[r, c] = possible
            todo.extend(neighbours(r, c))

    return best[height - 1, width - 1] - best[0, 0]


def neighbours(r, c):
    return [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]


def get_map(s):
    area = defaultdict(lambda: float("inf"))

    lines = s.splitlines()
    height = len(lines)
    width = len(lines[0])

    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            area[r, c] = int(char)
    given = (area, height, width)
    return given


example = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

example_answer = 40


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
