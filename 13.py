import os
import sys
from collections import deque, defaultdict
from functools import total_ordering, reduce
import bisect
from itertools import permutations

from hex import Hex
import networkx as nx

DIRECT_ADJACENTS = ((0, -1), (-1, 0), (1, 0), (0, 1))  # 4 adjacent nodes
ALL_ADJACENTS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
HEX_ADJACENTS = ((1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1))

class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self):
        self.data = [tuple(map(int, row)) for row in self.data]

        if not self.modified:
            return self.get_severity(0)

        n = 0
        while True:
            if self.is_winner(n):
                return n
            n += 1

    def is_winner(self, n):
        for i, r in self.data:
            full_range = (r << 1) - 2
            if (n+i) % full_range == 0:
                return False
        return True

    def get_severity(self, n):
        severity = 0
        for i, r in self.data:
            full_range = (r << 1) - 2
            if (n+i) % full_range == 0:
                severity += i * r
        return severity



if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    SPLIT_LINES = True
    SPLIT_CHAR = ': '

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())

