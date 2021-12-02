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
    given = get_one_int_per_line(input_text)
    last = given[0]
    for current in given[1:]:
        if current > last:
            answer += 1
        last = current

    return answer


def get_one_int_per_line(s):
    ints = []
    for line in s.split("\n"):
        ints.append(int(line))
    return ints


example = """\
199
200
208
210
200
207
240
269
260
263 """


def test_example():
    assert calculate(example) == 7


if __name__ == "__main__":
    exit(main())
