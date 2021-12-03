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

    nums = partlines(input_text)
    digits = len(nums[0])

    oxygens = nums[:]
    while len(oxygens) > 1:
        for d in range(digits):
            oxygens = oxygen_rating(oxygens, d)

    co2s = nums[:]
    while len(co2s) > 1:
        for d in range(digits):
            co2s = co2_rating(co2s, d)

    answer = int(co2s[0], 2) * int(oxygens[0], 2)

    return answer


def co2_rating(nums, digit):
    if len(nums) == 1:
        return nums

    ones = []
    zeroes = []
    for n in nums:
        if n[digit] == "1":
            ones.append(n)
        else:
            zeroes.append(n)

    if len(ones) >= len(zeroes):
        return zeroes
    else:
        return ones


def oxygen_rating(nums, digit):

    ones = []
    zeroes = []
    for n in nums:
        if n[digit] == "1":
            ones.append(n)
        else:
            zeroes.append(n)

    if len(ones) >= len(zeroes):
        return ones
    else:
        return zeroes


def partlines(s):
    given = []
    for line in s.split("\n"):
        line = line.strip()
        given.append(line)
    return given


example = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


def test_example():
    assert calculate(example) == 230


if __name__ == "__main__":
    exit(main())
