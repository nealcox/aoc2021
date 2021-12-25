import sys


def main():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):

    area, height, width = get_map(input_text)
    easts = set()
    souths = set()
    for k, v in area.items():
        if v == ">":
            easts.add(k)
        elif v == "v":
            souths.add(k)
    steps = 0
    moved = True
    while moved:
        moved = False
        steps += 1
        next_easts = set()
        next_souths = set()
        for cucumber in easts:
            target = (cucumber[0], (cucumber[1] + 1) % width)
            if target not in easts and target not in souths:
                next_easts.add(target)
                moved = True
            else:
                next_easts.add(cucumber)
        for cucumber in souths:
            target = ((cucumber[0] + 1) % height, cucumber[1])
            if target not in next_easts and target not in souths:
                next_souths.add(target)
                moved = True
            else:
                next_souths.add(cucumber)
        easts = next_easts
        souths = next_souths
    return steps


def get_map(s):
    area = {}
    lines = s.splitlines()
    height = len(lines)
    width = len(lines[0])

    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            area[r, c] = char
    given = (area, height, width)
    return given


example = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

example_answer = 58


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
