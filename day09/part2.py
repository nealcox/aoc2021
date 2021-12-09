import sys


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "input.txt"
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):

    given = input_text.split("\n")
    basin_points = set()
    for r, row in enumerate(given):
        for c, h in enumerate(row):
            if h != "9":
                basin_points.add((r, c))

    basins = []
    while basin_points:
        p = basin_points.pop()
        this_basin = {p}
        used_points = {p}

        merged = True
        while merged:
            merged = False
            neighbours = set()
            for r, c in used_points:
                neighbours |= {(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)}
            used_points = set()
            for p in basin_points:
                if p in neighbours:
                    used_points.add(p)
                    merged = True
            this_basin |= used_points
            basin_points -= used_points
        basins.append(this_basin)

    lengths = sorted([len(b) for b in basins])

    return lengths[-1] * lengths[-2] * lengths[-3]


example = """\
2199943210
3987894921
9856789892
8767896789
9899965678"""

example_answer = 1134


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
