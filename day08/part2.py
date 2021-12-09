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

    answer = 0
    given = parselines(input_text)
    for line in given:
        answer += solve(line)

    return answer


def solve(line):
    val = 0
    ins, outs = line
    to_solve = ins[:]
    solved = {}
    num_to_s = {}

    # Solve_order = (1,7,4,8,9,0,6,3,5,2)

    # Solve 1 - the only one with 2 segments
    for n in to_solve:
        if len(n) == 2:
            solved[n] = 1
            num_to_s[1] = n
            break
    assert 1 in num_to_s
    to_solve.remove(n)

    # Solve 7 - the only one with 3 segments
    for n in to_solve:
        if len(n) == 3:
            solved[n] = 7
            num_to_s[7] = n
            break
    assert 7 in num_to_s
    to_solve.remove(n)

    # Solve 4 - the only one with 4 segments
    for n in to_solve:
        if len(n) == 4:
            solved[n] = 4
            num_to_s[4] = n
            break
    assert 4 in num_to_s
    to_solve.remove(n)

    # Solve 8 - the only one with 7 segments
    for n in to_solve:
        if len(n) == 7:
            solved[n] = 8
            num_to_s[8] = n
            break
    assert 8 in num_to_s
    to_solve.remove(n)

    # Solve 9 - the only one with 6 segments, and all of 4's segments lit
    for n in to_solve:
        if len(n) == 6:
            is_9 = True
            for segment in num_to_s[4]:
                if segment not in n:
                    is_9 = False
            if is_9:
                solved[n] = 9
                num_to_s[9] = n
                break
    assert 9 in num_to_s
    to_solve.remove(n)

    # Solve 0 - the only one with 6 segments, and all of 1's segments lit
    #           now 9 has been removed
    for n in to_solve:
        if len(n) == 6:
            is_0 = True
            for segment in num_to_s[1]:
                if segment not in n:
                    is_0 = False
            if is_0:
                solved[n] = 0
                num_to_s[0] = n
                break
    assert 0 in num_to_s
    to_solve.remove(n)

    # Solve 6, the final one with 6 segments after 0 and 9 removed
    for n in to_solve:
        if len(n) == 6:
            solved[n] = 6
            num_to_s[6] = n
            break
    assert 6 in num_to_s
    to_solve.remove(n)

    # Solve 3 - the only one with 5 segments, and all of 1's segments lit
    for n in to_solve:
        if len(n) == 5:
            is_3 = True
            for segment in num_to_s[1]:
                if segment not in n:
                    is_3 = False
            if is_3:
                solved[n] = 3
                num_to_s[3] = n
                break
    assert 3 in num_to_s
    to_solve.remove(n)

    # Solve 5 - the only one with 5 segments, and matching 3 of 4's segments
    for n in to_solve:
        if len(n) == 5:
            matches = 0
            for segment in num_to_s[4]:
                if segment in n:
                    matches += 1
            if matches == 3:
                solved[n] = 5
                num_to_s[5] = n
                break
    assert 5 in num_to_s
    to_solve.remove(n)

    # Solve 2 - the only one left!
    assert len(to_solve) == 1
    solved[to_solve[0]] = 2
    num_to_s[2] = to_solve[0]

    val = 0
    for o in outs:
        val = val * 10 + solved[o]
    return val


def parselines(s):
    given = []
    for line in s.split("\n"):
        parts = " ".join(
                    [ "".join(sorted(word)) for word in line.split() ]
                    ).split(" | ")

        given.append([parts[0].split(), parts[1].split()])
    return given


example = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | \
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | \
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | \
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | \
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | \
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | \
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | \
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | \
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | \
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | \
fgae cfgab fg bagce"""
example_answer = 61229


def test_example():
    assert calculate(example) == example_answer


if __name__ == "__main__":
    exit(main())
