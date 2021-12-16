import re
import sys
from collections import defaultdict
from itertools import permutations


def main():
    filename = "input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        input_text = f.read().strip()
    print(f"Answer: {calculate(input_text)}")


def calculate(input_text):

    b_length = 4 * len(input_text)
    b = f"{int(input_text,16):0{b_length}b}"

    version_sum, _ = chomp(b)

    return version_sum


def chomp(b):
    if len(b) < 6:
        # End padding
        return 0, 0
    version = int(b[0:3], 2)
    type_id = int(b[3:6], 2)
    pos = 6
    if type_id == 4:
        # Literal value
        last_digit = False
        literal_s = ""
        while not last_digit:
            digit_s = b[pos : pos + 5]
            last_digit = digit_s[0] == "0"
            literal_s += digit_s[1:5]
            pos += 5
    else:
        # Operator
        operator_type = b[pos]
        pos += 1
        if operator_type == "0":
            # Fixed length subpacket
            sub_len = int(b[pos : pos + 15], 2)
            pos += 15
            sub_pos = 0
            while sub_pos < sub_len:
                sub_version, sub_progres = chomp(b[pos + sub_pos : pos + sub_len])
                version += sub_version
                sub_pos += sub_progres
            pos += sub_len
        else:
            # Fixed number of subpackets
            num_subpackets = int(b[pos : pos + 11], 2)
            pos += 11
            for i in range(num_subpackets):
                sub_version, sub_length = chomp(b[pos:])
                version += sub_version
                pos += sub_length
    return version, pos


ex_1 = "D2FE28"
ex_1_ans = 6


def test_ex1():
    assert calculate(ex_1) == ex_1_ans


ex_2 = "38006F45291200"
ex_2_ans = 1 + 6 + 2  # main + A + B


def test_ex2():
    assert calculate(ex_2) == ex_2_ans


ex_3 = "EE00D40C823060"
ex_3_ans = 7 + 2 + 4 + 1  # main + A + B


def test_ex3():
    assert calculate(ex_3) == ex_3_ans


ex_4 = "8A004A801A8002F478"
ex_4_ans = 16


def test_ex4():
    assert calculate(ex_4) == ex_4_ans


ex_5 = "620080001611562C8802118E34"
ex_5_ans = 12


def test_ex5():
    assert calculate(ex_5) == ex_5_ans


ex_6 = "C0015000016115A2E0802F182340"
ex_6_ans = 23


def test_ex6():
    assert calculate(ex_6) == ex_6_ans


ex_7 = "A0016C880162017C3686B18A3D4780"
ex_7_ans = 31


def test_ex7():
    assert calculate(ex_7) == ex_7_ans


if __name__ == "__main__":
    exit(main())
