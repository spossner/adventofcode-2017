import os
import sys
from collections import deque, defaultdict
from functools import total_ordering, reduce
import bisect
from itertools import permutations

from hex import Hex

DIRECT_ADJACENTS = ((0, -1), (-1, 0), (1, 0), (0, 1))  # 4 adjacent nodes
ALL_ADJACENTS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
HEX_ADJACENTS = ((1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1))

class Solution:
    def __init__(self, data, is_dev=False, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self):
        pos = Hex(0, 0, 0)
        max_away = 0
        for step in self.data:
            pos = pos.neighbor(step)
            max_away = max(pos.length(), max_away)
        return (pos.length(), max_away)


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = False
    SPLIT_LINES = False
    SPLIT_CHAR = ','

    print(Solution("ne,ne,ne", PART2, DEV, SPLIT_LINES, SPLIT_CHAR).solve())
    print(Solution("ne,ne,sw,sw", PART2, DEV, SPLIT_LINES, SPLIT_CHAR).solve())
    print(Solution("ne,ne,s,s", PART2, DEV, SPLIT_LINES, SPLIT_CHAR).solve())
    print(Solution("se,sw,se,sw,sw", PART2, DEV, SPLIT_LINES, SPLIT_CHAR).solve())

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read().strip(), PART2, DEV, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())

    # 1117 is too high.. 720 is correct

