import sys
from collections import Counter
from functools import lru_cache
STEPS=40


def main():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):

    template, rules_in = input_text.split("\n\n")
    rules = set()
    for line in rules_in.splitlines():
         rule = line.split()
         rules.add( (rule[0][0],rule[0][1], rule[2]) )
    rules = frozenset(rules)
 
    for step  in range(STEPS,STEPS+1):
        counts = Counter()
        prev = template[0]
        result = prev
        counts.update(prev)
        for i,letter in enumerate(template[1:]):
            subcounts,prev = expand(prev,letter,step,rules)
            counts.update(subcounts)
        most = max(counts.values())
        least = min(counts.values())
 
    return most - least

@lru_cache(maxsize=100000)
def expand(prev,letter,steps,rules):
    counts = Counter()
    if steps == 0:
        counts.update(letter)
        prev = letter
    else:
        mid = None
        while not mid:
            for x,y,z in rules:
                if (prev == x and letter == y):
                    mid=z
        first,_ =  expand(prev,mid,steps -1, rules) 
        second,prev =   expand(mid,letter,steps - 1,rules)
        counts = ( first + second)
    return counts, prev
         

example = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

example_answer = 2188189693529


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
