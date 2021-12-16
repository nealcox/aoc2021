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

    result, _ = chomp(b)

    return result


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
        result = int(literal_s, 2)
    else:
        # Operator
        operator_type = b[pos]
        pos += 1

        # Operands
        vals = []
        if operator_type == "0":
            sub_len = int(b[pos : pos + 15], 2)
            pos += 15
            sub_pos = 0
            while sub_pos < sub_len:
                sub_val, sub_progres = chomp(b[pos + sub_pos : pos + sub_len])
                vals.append(sub_val)
                sub_pos += sub_progres
            pos += sub_len
        else:
            num_subpackets = int(b[pos : pos + 11], 2)
            pos += 11
            for i in range(num_subpackets):
                sub_val, l = chomp(b[pos:])
                vals.append(sub_val)
                pos += l

        # Evaluate
        if type_id == 0:  # Sum
            result = sum(vals)
        elif type_id == 1:  # Product
            result = 1
            for v in vals:
                result *= v
        elif type_id == 2:  # Minimum
            result = min(vals)
        elif type_id == 3:  # Maximun
            result = max(vals)
        elif type_id == 5:  # Greater than
            if vals[0] > vals[1]:
                result = 1
            else:
                result = 0
        elif type_id == 6:  # Less than
            if vals[0] < vals[1]:
                result = 1
            else:
                result = 0
        elif type_id == 7:  # Equal
            if vals[0] == vals[1]:
                result = 1
            else:
                result = 0
        else:
            raise ValueError(f"Unknown type id {type_id}")

    return result, pos


ex_1 = "C200B40A82"
ex_1_ans = 3


def test_ex1():
    assert calculate(ex_1) == ex_1_ans


ex_2 = "04005AC33890"
ex_2_ans = 54


def test_ex2():
    assert calculate(ex_2) == ex_2_ans


ex_3 = "880086C3E88112"
ex_3_ans = 7


def test_ex3():
    assert calculate(ex_3) == ex_3_ans


ex_4 = "CE00C43D881120"
ex_4_ans = 9


def test_ex5():
    assert calculate(ex_4) == ex_4_ans


ex_5 = "D8005AC2A8F0"
ex_5_ans = 1


def test_ex6():
    assert calculate(ex_5) == ex_5_ans


ex_6 = "F600BC2D8F"
ex_6_ans = 0


def test_ex7():
    assert calculate(ex_6) == ex_6_ans


ex_7 = "9C005AC2F8F0"
ex_7_ans = 0


def test_ex8():
    assert calculate(ex_7) == ex_7_ans


ex_8 = "9C0141080250320F1802104A08"
ex_8_ans = 1


def test_ex9():
    assert calculate(ex_8) == ex_8_ans


if __name__ == "__main__":
    exit(main())
