import re
import sys
from collections import defaultdict
from itertools import permutations

# Example sf:
# [[1,9],[8,5]]
# Let's have a tuple, including a level indicator:
# (x,y,0)  where x = (1,9,1) and y = (8,5,1)


def main():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):

    answer = []
    in_lines = input_text.splitlines()
    for i, line in enumerate(in_lines):
        print(f"{i:3}:{line}")
        sf = parse_sf(line)
        # print(f"    {sf}")
        # print(f"Starting answer: {answer}\nAdding: {sf}")

        if not answer:
            answer = sf
        else:
            answer = ["["] + answer + sf + ["]"]
        answer = reduce_sf(answer[:])

    mag = magnitude(answer)

    return mag


def magnitude(sf):
    if len(sf) == 1:
        return sf[0]
    depth = 0
    idx = 0
    while True:
        if sf[idx] == "[":
            depth += 1
        elif sf[idx] == "]":
            depth -= 1
            if depth == 0:
                # Got to end, simple snailfish number
                left, right = sf[1], sf[2]
                print(f"{sf} -> {left} , {right}")
                return 3 * left + 2 * right
            if depth == 1:
                # Found end of complex snailfish number
                left, right = sf[1 : idx + 1], sf[idx + 1 : -1]
                print(f"{sf} -> {left} , {right}")
                return 3 * magnitude(left) + 2 * magnitude(right)
        idx += 1


def parse_sf(s):
    sf = []
    for c in s:
        if c.isnumeric():
            sf.append(int(c))
        elif c != ",":
            sf.append(c)
    return sf


def reduce_sf(sf):
    # print(f"Reducing {c for c in sf}")

    # Explode
    explode_done = False
    changed = True
    while changed:
        changed = False
        depth = 0
        i = 0
        while i < len(sf):
            c = sf[i]
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
            if depth > 5:
                raise ValueError("Max depth of SF number exceeded")
            if depth == 5:
                changed = True
                explode_done = True
                left, right = sf[i + 1], sf[i + 2]
                # breakpoint()

                prev_num_idx = i - 1
                while prev_num_idx > 0 and not (isinstance(sf[prev_num_idx], int)):
                    prev_num_idx -= 1
                if prev_num_idx > 0:
                    sf[prev_num_idx] += left

                next_num_idx = i + 4
                while next_num_idx < len(sf) and not (
                    isinstance(sf[next_num_idx], int)
                ):
                    next_num_idx += 1
                if next_num_idx < len(sf):
                    sf[next_num_idx] += right

                new_left_sf = sf[:i]
                new_right_sf = sf[i + 4 :]
                # print(f"New left : {new_left_sf} \nNew right: {new_right_sf}")
                sf = new_left_sf + [0] + new_right_sf
                depth -= 1
            i += 1

    # Split
    split_done = False
    i = 0
    while i < len(sf) and not (split_done):
        if isinstance(sf[i], int):
            if sf[i] > 9:
                split_done = True
                left = sf[i] // 2
                right = (sf[i] + 1) // 2
                mid = ["[", left, right, "]"]
                sf = sf[:i] + mid + sf[i + 1 :]
        i += 1
    if split_done:
        sf = reduce_sf(sf)
    # print(f"Reduced to  {c for c in sf}")
    return sf


def test_reduce1():
    ex1 = parse_sf("[[[[[9,8],1],2],3],4]")
    ans1 = parse_sf("[[[[0,9],2],3],4]")

    assert reduce_sf(ex1) == ans1


def test_reduce2():
    ex2 = parse_sf("[7,[6,[5,[4,[3,2]]]]]")
    ans2 = parse_sf("[7,[6,[5,[7,0]]]]")

    assert reduce_sf(ex2) == ans2


def test_reduce3():
    ex3 = parse_sf("[[6,[5,[4,[3,2]]]],1]")
    ans3 = parse_sf("[[6,[5,[7,0]]],3]")

    assert reduce_sf(ex3) == ans3


def test_reduce4():
    ex4 = parse_sf("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    ans4 = parse_sf("[[3,[2,[8,0]]],[9,[5,[7,0]]]]")

    assert reduce_sf(ex4) == ans4


def test_reduce5():
    ex5 = parse_sf("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
    ans5 = parse_sf("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

    assert reduce_sf(ex5) == ans5


def test_magnitude1():
    ex1 = parse_sf("[[1,2],[[3,4],5]]")
    ans1 = 143

    assert magnitude(ex1) == ans1


def test_magnitude2():
    ex2 = parse_sf("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
    ans2 = 1384

    assert magnitude(ex2) == ans2


def test_magnitude3():
    ex3 = parse_sf("[[[[1,1],[2,2]],[3,3]],[4,4]]")
    ans3 = 445

    assert magnitude(ex3) == ans3


def test_magnitude4():
    ex4 = parse_sf("[[[[3,0],[5,3]],[4,4]],[5,5]]")
    ans4 = 791

    assert magnitude(ex4) == ans4


def test_magnitude5():
    ex5 = parse_sf("[[[[5,0],[7,4]],[5,5]],[6,6]]")
    ans5 = 1137

    assert magnitude(ex5) == ans5


def test_magnitude6():
    ex6 = parse_sf("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
    ans6 = 3488

    assert magnitude(ex6) == ans6


example = """\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""

example_answer = 4140
# example_answer = parse_sf("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
