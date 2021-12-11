import sys
from collections import defaultdict


def main():
    STEPS = 100
    filename = "input.txt"
    if len(sys.argv) > 1:
        STEPS = int(sys.argv[1])
        if len(sys.argv) > 2:
            filename = sys.argv[2]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text, STEPS)}")


def calculate(input_text, STEPS):

    answer = 0
    octs, height, width = get_map(input_text)
    for step in range(1, STEPS + 1):
        flashed = set()
        for r in range(height):
            for c in range(width):
                octs, flashed = increment(octs, r, c, flashed)
        for r in range(height + 1):
            for c in range(width + 1):
                if octs[r, c] > 9:
                    octs[r, c] = 0
                    answer += 1

    printocts(octs, height, width, step, len(flashed))
    return answer


def printocts(octs, height, width, step, f):
    print(f"After step {step}:")
    for r in range(height):
        for c in range(width):
            print(octs[r, c], end="")
        print()
    print(f"{f} flashes")
    print()


def increment(octs, r, c, flashed):
    octs[r, c] += 1
    if octs[r, c] > 9 and (r, c) not in flashed:
        flashed.add((r, c))
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx, dy) != (0, 0):
                    octs, flashed = increment(octs, r + dx, c + dy, flashed)
    return octs, flashed


def get_map(s):
    area = defaultdict(lambda: float("-inf"))

    height = 0
    width = 0

    for r, row in enumerate(s.split("\n")):
        if r > height:
            height = r
        for c, char in enumerate(row):
            area[r, c] = int(char)
            if c > width:
                width = c
    given = (area, height + 1, width + 1)
    return given


example = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

example_answer = 1656


def test_example():
    assert calculate(example, 100) == example_answer


if __name__ == "__main__":
    exit(main())
