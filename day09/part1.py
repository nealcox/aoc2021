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

    answer = 0
    given = input_text.split("\n")
    height = len(given)
    width = len(given[0])
    for r, row in enumerate(given):
        for c, h in enumerate(row):
            neighbours = set()
            if r > 0:
                neighbours.add(int(given[r - 1][c]))
            if r < height - 1:
                neighbours.add(int(given[r + 1][c]))
            if c > 0:
                neighbours.add(int(given[r][c - 1]))
            if c < width - 1:
                neighbours.add(int(given[r][c + 1]))
            low = True
            for n in neighbours:
                if int(h) >= int(n):
                    low = False
            if low:
                answer += 1 + int(h)

    return answer


example = """\
2199943210
3987894921
9856789892
8767896789
9899965678"""

example_answer = 15


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
