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
    instructions = []
    lights = defaultdict(int)
    for line in input_text.splitlines():
        onoff, regions = line.split()
        if onoff == "on":
            onoff = 1
        elif onoff == "off":
            onoff = 0
        else:
            raise ValueError(f"Unknown instructions {onoff} in line {line}")
        nums = get_all_ints(line)
        assert nums[1] >= nums[0]
        assert nums[3] >= nums[3]
        assert nums[5] >= nums[4]
        instructions.append((onoff, nums))
    # Create a list of disjoint "on" instructions
    #
    # Work from end of list to get final state of each point in that instruction
    # and go through other instructions, removing parts that overlap with
    # the later instructions

    ons = []
    while instructions:
        next_instructions = []
        onoff, nums = instructions.pop()
        if onoff == 1:
            ons.append(nums)
        for i in instructions:
            next_instructions.extend(eliminate(i, nums))
        instructions = next_instructions

    answer = 0
    for x0, x1, y0, y1, z0, z1 in ons:
        answer += (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)

    return answer


def eliminate(instruction, nums):
    onoff, coords = instruction
    cubes = []
    cubes.append(coords)

    # if disjoint, just return the one we've got
    if (
        coords[0] > nums[1]
        or coords[2] > nums[3]
        or coords[4] > nums[5]
        or coords[1] < nums[0]
        or coords[3] < nums[2]
        or coords[5] < nums[4]
    ):
        return [instruction]

    # if wholly contained, then nothing to return
    if (
        coords[0] >= nums[0]
        and coords[2] >= nums[2]
        and coords[4] >= nums[4]
        and coords[1] <= nums[1]
        and coords[3] <= nums[3]
        and coords[5] <= nums[5]
    ):
        return []

    # split on x
    next_cubes = []
    for c in cubes:
        x0, x1, y0, y1, z0, z1 = c
        if x0 <= nums[0] <= x1:
            next_cubes.append((x0, nums[0] - 1, y0, y1, z0, z1))
            next_cubes.append((nums[0], x1, y0, y1, z0, z1))
        else:
            next_cubes.append(c)
    cubes = [c for c in next_cubes if c[0] <= c[1]]
    next_cubes = []
    for c in cubes:
        x0, x1, y0, y1, z0, z1 = c
        if x0 <= nums[1] <= x1:
            next_cubes.append((x0, nums[1], y0, y1, z0, z1))
            next_cubes.append((nums[1] + 1, x1, y0, y1, z0, z1))
        else:
            next_cubes.append(c)
    cubes = [c for c in next_cubes if c[0] <= c[1]]

    # split on y
    next_cubes = []
    for c in cubes:
        x0, x1, y0, y1, z0, z1 = c
        if y0 <= nums[2] <= y1:
            next_cubes.append(
                (x0, x1, y0, nums[2] - 1, z0, z1),
            )
            next_cubes.append(
                (x0, x1, nums[2], y1, z0, z1),
            )
        else:
            next_cubes.append(c)
    cubes = next_cubes
    cubes = [c for c in next_cubes if c[2] <= c[3]]
    next_cubes = []
    for c in cubes:
        x0, x1, y0, y1, z0, z1 = c
        if y0 <= nums[3] <= y1:
            next_cubes.append(
                (x0, x1, y0, nums[3], z0, z1),
            )
            next_cubes.append(
                (x0, x1, nums[3] + 1, y1, z0, z1),
            )
        else:
            next_cubes.append(c)
    cubes = next_cubes
    cubes = [c for c in next_cubes if c[2] <= c[3]]

    # split on z
    next_cubes = []
    for c in cubes:
        x0, x1, y0, y1, z0, z1 = c
        if z0 <= nums[4] <= z1:
            next_cubes.append((x0, x1, y0, y1, z0, nums[4] - 1))
            next_cubes.append((x0, x1, y0, y1, nums[4], z1))
        else:
            next_cubes.append(c)
    cubes = next_cubes
    cubes = [c for c in next_cubes if c[4] <= c[5]]

    next_cubes = []
    for c in cubes:
        x0, x1, y0, y1, z0, z1 = c
        if z0 <= nums[5] <= z1:
            next_cubes.append((x0, x1, y0, y1, z0, nums[5]))
            next_cubes.append((x0, x1, y0, y1, nums[5] + 1, z1))
        else:
            next_cubes.append(c)
    cubes = next_cubes
    cubes = [c for c in next_cubes if c[4] <= c[5]]

    # Remove mini-cubes which don't belong
    next_cubes = []
    for c in cubes:
        x0, x1, y0, y1, z0, z1 = c
        if not (
            nums[0] <= x0 <= nums[1]
            and nums[2] <= y0 <= nums[3]
            and nums[4] <= z0 <= nums[5]
        ):
            next_cubes.append(c)
    cubes = next_cubes

    return [(onoff, c) for c in cubes]


def get_all_ints(s):
    return [int(i) for i in re.findall(r"(-?\d+)", s)]


example = """\
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""

example_answer = 2758514936282235


def test_example():
    assert calculate(example) == example_answer


example1 = """\
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29"""


def test_example1():
    assert calculate(example1) == 474140


def test_eliminate_disjoint():
    assert eliminate(("on", (10, 10, 10, 10, 10, 10)), (0, 0, 0, 0, 0, 0)) == [
        ("on", (10, 10, 10, 10, 10, 10))
    ]


def test_eliminate_all():
    assert eliminate(("on", (10, 15, 10, 15, 10, 15)), (0, 20, 0, 20, 0, 20)) == []


def test_eliminate_equal():
    assert eliminate(("on", (10, 15, 10, 15, 10, 15)), (10, 15, 10, 15, 10, 15)) == []


def test_eliminate_left_face():
    assert eliminate(("on", (0, 10, 0, 10, 0, 10)), (-10, 0, -10, 20, -10, 20)) == [
        ("on", (1, 10, 0, 10, 0, 10))
    ]


def test_eliminate_left_face_exact():
    assert eliminate(("on", (0, 10, 0, 10, 0, 10)), (0, 0, 0, 10, 0, 10)) == [
        ("on", (1, 10, 0, 10, 0, 10))
    ]


def test_eliminate_left_face_partial():
    assert (
        eliminate(("on", (0, 10, 0, 10, 0, 10)), (0, 0, 5, 5, 5, 5))
        ==
        #            Eight for left face (rows 1-8 start (0,0...
        #                   z
        #              01234567890
        #            0 11111233333
        #            2 11111233333
        #            3 11111233333
        #            4 11111233333
        #        y   5 44444 55555
        #            6 66666788888
        #            7 66666788888
        #            8 66666788888
        #            9 66666788888
        #            0 66666788888
        #            Covers all for rest  (rows 9- uuse letters start (1,10...
        #              01234567890
        #            0 AAAAABCCCCC
        #            2 AAAAABCCCCC
        #            3 AAAAABCCCCC
        #            4 AAAAABCCCCC
        #            5 DDDDDEFFFFF
        #            6 GGGGGHIIIII
        #            7 GGGGGHIIIII
        #            8 GGGGGHIIIII
        #            9 GGGGGHIIIII
        #            0 GGGGGHIIIII
        #
        [
            (
                "on",
                (0, 0, 0, 4, 0, 4),
            ),
            (
                "on",
                (0, 0, 0, 4, 5, 5),
            ),
            (
                "on",
                (0, 0, 0, 4, 6, 10),
            ),
            (
                "on",
                (0, 0, 5, 5, 0, 4),
            ),
            (
                "on",
                (0, 0, 5, 5, 6, 10),
            ),
            (
                "on",
                (0, 0, 6, 10, 0, 4),
            ),
            (
                "on",
                (0, 0, 6, 10, 5, 5),
            ),
            (
                "on",
                (0, 0, 6, 10, 6, 10),
            ),
            (
                "on",
                (1, 10, 0, 4, 0, 4),
            ),
            (
                "on",
                (1, 10, 0, 4, 5, 5),
            ),
            (
                "on",
                (1, 10, 0, 4, 6, 10),
            ),
            (
                "on",
                (1, 10, 5, 5, 0, 4),
            ),
            (
                "on",
                (1, 10, 5, 5, 5, 5),
            ),
            (
                "on",
                (1, 10, 5, 5, 6, 10),
            ),
            (
                "on",
                (1, 10, 6, 10, 0, 4),
            ),
            (
                "on",
                (1, 10, 6, 10, 5, 5),
            ),
            ("on", (1, 10, 6, 10, 6, 10)),
        ]
    )


def test_eliminate_on_all():
    assert eliminate(("on", (0, 30, 0, 30, 0, 30)), (11, 19, 11, 19, 11, 19)) == [
        (
            "on",
            (0, 10, 0, 10, 0, 10),
        ),
        (
            "on",
            (0, 10, 0, 10, 11, 19),
        ),
        (
            "on",
            (0, 10, 0, 10, 20, 30),
        ),
        (
            "on",
            (0, 10, 11, 19, 0, 10),
        ),
        (
            "on",
            (0, 10, 11, 19, 11, 19),
        ),
        (
            "on",
            (0, 10, 11, 19, 20, 30),
        ),
        (
            "on",
            (0, 10, 20, 30, 0, 10),
        ),
        (
            "on",
            (0, 10, 20, 30, 11, 19),
        ),
        (
            "on",
            (0, 10, 20, 30, 20, 30),
        ),
        (
            "on",
            (11, 19, 0, 10, 0, 10),
        ),
        (
            "on",
            (11, 19, 0, 10, 11, 19),
        ),
        (
            "on",
            (11, 19, 0, 10, 20, 30),
        ),
        (
            "on",
            (11, 19, 11, 19, 0, 10),
        ),
        (
            "on",
            (11, 19, 11, 19, 20, 30),
        ),
        (
            "on",
            (11, 19, 20, 30, 0, 10),
        ),
        (
            "on",
            (11, 19, 20, 30, 11, 19),
        ),
        (
            "on",
            (11, 19, 20, 30, 20, 30),
        ),
        (
            "on",
            (20, 30, 0, 10, 0, 10),
        ),
        (
            "on",
            (20, 30, 0, 10, 11, 19),
        ),
        (
            "on",
            (20, 30, 0, 10, 20, 30),
        ),
        (
            "on",
            (20, 30, 11, 19, 0, 10),
        ),
        (
            "on",
            (20, 30, 11, 19, 11, 19),
        ),
        (
            "on",
            (20, 30, 11, 19, 20, 30),
        ),
        (
            "on",
            (20, 30, 20, 30, 0, 10),
        ),
        (
            "on",
            (20, 30, 20, 30, 11, 19),
        ),
        ("on", (20, 30, 20, 30, 20, 30)),
    ]


if __name__ == "__main__":
    exit(main())
