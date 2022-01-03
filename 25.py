import math
import operator
import os
import re
import sys
from collections import deque, defaultdict, namedtuple
from functools import total_ordering, reduce
import bisect
from itertools import permutations, zip_longest, count

import networkx as nx
import pygame as pg
import numpy as np

from aoc import Point, NORTH, rot_ccw, rot_cw, translate


class Solution:
    def __init__(self, data, modified=False, do_strip=False, do_splitlines=True, split_char=None):
        if data and do_strip:
            data = data.strip()
        if data and do_splitlines:
            data = data.splitlines()
        if data and split_char:
            if split_char == '':
                data = [list(row) for row in data] if do_splitlines else list(data)
            else:
                data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self):
        n = int(re.match('Perform a diagnostic checksum after (\d+)', self.data[1]).group(1))

        edges = {}
        for i in range(3, len(self.data), 10):
            state = self.data[i][-2]
            zero = (int(self.data[i+2][-2]), -1 if self.data[i+3][-5] == 'l' else 1, self.data[i+4][-2])
            one = (int(self.data[i+6][-2]), -1 if self.data[i+7][-5] == 'l' else 1, self.data[i+8][-2])
            edges[state] = (zero, one)
        print(edges)
        ptr = 0
        tape = defaultdict(int)
        state = 'A'
        for i in range(n):
            rule = edges[state]
            cmd = rule[0] if tape[ptr] == 0 else rule[1]
            tape[ptr] = cmd[0]
            ptr += cmd[1]
            state = cmd[2]
        return sum(tape.values())

if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = False
    STRIP = True
    SPLIT_LINES = True
    SPLIT_CHAR = None

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read(), PART2, STRIP, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())
