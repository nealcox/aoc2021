import re
import sys
from collections import defaultdict
from itertools import permutations


def main():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):
    instructions = []
    lights = defaultdict(int)
    for line in input_text.splitlines():
        onoff, _ = line.split()
        if onoff == "on":
            onoff = 1
        elif onoff == "off":
            onoff = 0
        else:
            raise ValueError(f"Unknown instructions {onoff} in line {line}")
        nums = get_all_ints(line)
        assert nums[1] >= nums[0]
        assert nums[3] >= nums[2]
        assert nums[5] >= nums[4]
        if (
            nums[0] <= 50
            and nums[1] >= -50
            and nums[2] <= 50
            and nums[3] >= -50
            and nums[4] <= 50
            and nums[5] >= -50
        ):

            nums[0] = max(nums[0], -50)
            nums[1] = min(nums[1], 50)
            nums[2] = max(nums[2], -50)
            nums[3] = min(nums[3], 50)
            nums[4] = max(nums[4], -50)
            nums[5] = min(nums[5], 50)
            instructions.append((onoff, nums))

    for onoff, nums in instructions:
        for x in range(nums[0], nums[1] + 1):
            for y in range(nums[2], nums[3] + 1):
                for z in range(nums[4], nums[5] + 1):
                    lights[x, y, z] = onoff

    answer = sum(lights.values())

    return answer


def get_all_ints(s):
    return [int(i) for i in re.findall(r"(-?\d+)", s)]


example = """\
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""

example_answer = 39


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
