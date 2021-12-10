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

    lines = input_text.split("\n")
    answer = 0
    for line in lines:
        s = score(line)
        answer += s

    return answer


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
<{([{{}}[<[[[<>{}]]]>[]]
"""

example_answer = 26397


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
