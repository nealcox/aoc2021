import re
import sys
from collections import Counter
from collections import defaultdict


def main():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):

    moves = get_re(input_text)
    r = re.compile(r"[A-Z+]")
    smalls = set()
    for m in moves:
        if not r.findall(m[0]):
            smalls.add(m[0])
    complete_paths = []
    paths = [["start"]]
    while paths:
        next_paths = []
        finished = True
        for p in paths:
            at = p[-1]
            for move_from,move_to in moves:
                if at == move_from:
                    if (
                            (move_to not in smalls) or
                            (move_to not in p) or
                            (move_to != "start" and no_twice(p, smalls))
                            ):
                        new_p = p + [move_to]
                        if new_p[-1] == "end":
                            complete_paths.append(new_p)
                        else:
                            next_paths.append( new_p)
        paths = next_paths

    return len(complete_paths)


def no_twice(p,smalls):
    visited = Counter(p)
    num_visited_twice = 0
    for s in smalls:
        if s in p:
            if visited[s] > 1:
                num_visited_twice += 1
    no_twice_smalls =  num_visited_twice == 0
    return no_twice_smalls

def get_re(s):
    given = set()
    r = re.compile(r"(\w+)-(\w+)")
    for m in r.findall(s):
        given.add( (m[0],m[1]) )
        given.add( (m[1],m[0]) )
    return given


def get_all_ints(s):
    return [int(i) for i in re.findall(r"(\d+)", s)]


example = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

example_answer = 36


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
