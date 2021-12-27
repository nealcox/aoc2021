import re
import sys
from collections import defaultdict

WIN = 21


def main():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):
    # Three rolls so values are 111,112,113,121,etc ie 27 combinations
    # in 1 universe - score is 3
    # in 3 universe - score is 4
    # in 6 universe - score is 5
    # in 7 universe - score is 6
    # in 6 universe - score is 7
    # in 3 universe - score is 8
    # in 1 universe - score is 9
    scores = [(1, 3), (3, 4), (6, 5), (7, 6), (6, 7), (3, 8), (1, 9)]
    players = []
    wins = [0, 0]
    for line in input_text.splitlines():
        players.append(int(line.split()[-1]))

    state = defaultdict(int)
    # state [ (player0-position, player0-score,
    #          player1-position, player1-score)] = number of universes with that state
    state[players[0], 0, players[1], 0] = 1

    while state:
        next_state = defaultdict(int)
        countuniverses = 0
        # first player takes their turn
        for player_state, prev_universes in state.items():
            pos0, score0, pos1, score1 = player_state
            for universes, dice in scores:
                new_pos0 = (pos0 - 1 + dice) % 10 + 1
                new_score0 = score0 + new_pos0
                next_state[new_pos0, new_score0, pos1, score1] += (
                    prev_universes * universes
                )
        state = defaultdict(int)
        for player_state, universes in next_state.items():
            pos0, score0, pos1, score1 = player_state
            if score0 >= WIN:
                wins[0] += universes
            else:
                state[player_state] += universes

        # second player takes their turn
        next_state = defaultdict(int)
        for player_state, prev_universes in state.items():
            pos0, score0, pos1, score1 = player_state
            for universes, dice in scores:
                new_pos1 = (pos1 - 1 + dice) % 10 + 1
                new_score1 = score1 + new_pos1
                next_state[pos0, score0, new_pos1, new_score1] += (
                    prev_universes * universes
                )
        state = defaultdict(int)
        for player_state, universes in next_state.items():
            pos0, score0, pos1, score1 = player_state
            if score1 >= WIN:
                wins[1] += universes
            else:
                state[player_state] += universes

    return max(wins)


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

example_answer = 444356092776315


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
