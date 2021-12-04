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

    answer = None
    numbers, boards = parse(input_text)

    finished = False
    line_length = len(boards[0])
    for number in numbers:
        print(f"Call {number}")
        for board in boards:
            for line in board:
                for i in range(line_length):
                    if line[i] == number:
                        line[i] = "X"
                        finished = check_house(board)
            if finished:
                break
        if finished:
            break
    print(f"{board}")
    answer = score(board) * number


    return answer

def score(board):
    score = 0
    for row in board:
        for n in row:
            if n != "X":
                score += n
    return score

def check_house(board):
    length = len(board[0])
    for line in board:
        if all( [n == "X" for n in line] ):
            return True
    
    for col_num in range(length):
        col_found = True
        for row in range(length):
            if board[row][col_num] != "X":
                col_found = False
        if col_found:
            return True
    return False
            
        


def parse(s):
    data = s.split("\n\n")
    numbers,board_data = data[0], data[1:]
    numbers = [int(n) for n in numbers.split(",")]

    boards = []
    r = re.compile(r"(\d+)")
    for board_s in board_data:
        board = []
        for line in board_s.split("\n"):
            nums = r.findall(line)
            nums = [int(n) for n in nums]
            board.append(nums)
        boards.append(board)

    return numbers, boards


def partlines(s):
    given = []
    for line in s.split("\n"):
        line = line.strip()
        given.append(line)
    return given


def get_one_int_per_line(s):
    ints = []
    for line in s.split("\n"):
        ints.append(int(line))
    return ints


def get_re(s):
    given = []
    r = re.compile(r"(\w+) (\d+)")
    for m in r.findall(s):
        given.append((m[0], int(m[1])))
    return given


example = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


def test_example():
    assert calculate(example) == 4512

b = [
[27, 48, 10, 81, 89],
[30, 35, 79,  2, 97],
[18, 64, 19, 57, 78],
[76,  1, 94, 33, 53],
[34, 66, 74, 49, 90],
]

b1 = [
[27, 48, "X", 81, 89],
[30, 35, "X",  2, 97],
[18, 64, "X", 57, 78],
[76,  1, "X", 33, 53],
[34, 66, "X", 49, 90],
]

def test_col_found():
    assert check_house(b1) == True


if __name__ == "__main__":
    exit(main())
