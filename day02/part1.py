import re
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

    h = 0
    d = 0
    given = get_re(input_text)
    for direction, dist in given:
        if direction == "forward":
            h += dist
        elif direction == "down":
            d += dist
        elif direction == "up":
            d -= dist
        else:
            raise ValueError(f"unknown direction {direction}")

    return h * d


def get_re(s):
    given = []
    r = re.compile(r"(\w+) (\d+)")
    for m in r.findall(s):
        given.append((m[0], int(m[1])))
    return given


example = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2"""


def test_example():
    assert calculate(example) == 150


if __name__ == "__main__":
    exit(main())
