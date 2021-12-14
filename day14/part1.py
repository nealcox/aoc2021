import sys
from collections import Counter
STEPS=10


def main():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):

    template, rules_in = input_text.split("\n\n")
    rules = {}
    for line in rules_in.splitlines():
         rule = line.split()
         rules[rule[0]] = rule[2]
 
    for step in range(1,STEPS+1):
        pairs = []
        for i in range(1,len(template)):
            pairs.append( template[i-1:i+1] )
        tozip = "".join( rules[p] for p in pairs)
        next_temp = []
        for i in range(len(template)-1):
            next_temp.append(template[i])
            next_temp.append(tozip[i])
        next_temp.append(template[-1])
        template = "".join(next_temp)
        
 
    letters = Counter(template)
    most = max(letters.values())
    least = min(letters.values())
 
 
    return most - least
 

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

example_answer = 1588


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
