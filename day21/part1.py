import re
import sys
from collections import defaultdict


def main():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):
    players = []
    scores = [0, 0]
    for line in input_text.splitlines():
        players.append(int(line.split()[-1]))
    finished = False
    d = Die()
    while True:
        die = 0
        for _ in range(3):
            die += d.roll()
        players[0] = (players[0] - 1 + die) % 10 + 1
        scores[0] += players[0]
        if scores[0] >= 1000:
            break
        die = 0
        for _ in range(3):
            die += d.roll()
        players[1] = (players[1] - 1 + die) % 10 + 1
        scores[1] += players[1]
        if scores[1] >= 1000:
            break
    answer = min(scores) * d.rolls

    return answer


class Die:
    def __init__(self):
        self.val = -1
        self.rolls = 0

    def roll(self):
        self.val = (self.val + 1) % 100
        self.rolls += 1
        return self.val + 1


example = """\
Player 1 starting position: 4
Player 2 starting position: 8
"""

example_answer = 739785


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
