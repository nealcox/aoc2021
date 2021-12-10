import re
import sys
from collections import defaultdict
from itertools import permutations


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
    lines = input_text.split("\n")
    scores = []
    for line in lines:
        s = score(line)
        if s == 0:
            scores.append(score2(line))

    scores.sort()
    m = ((len(scores) + 1) // 2) - 1
    return scores[m]


def score2(line):
    stack = []
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}
    for c in line:
        if c in "([{<":
            stack.append(c)
        else:
            last = stack.pop()
    score = 0
    for last in stack[::-1]:
        score = score * 5 + scores[last]
    return score


def score(line):
    stack = []
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    for c in line:
        if c in "([{<":
            stack.append(c)
        else:
            last = stack.pop()
            if (last, c) not in (("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")):
                return scores[c]
    return 0


example = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

example_answer = 288957


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
