import math
import os
import sys
from collections import deque, defaultdict
from functools import total_ordering, reduce

import pygame as pg
import numpy as np


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
        components = defaultdict(list)
        for i, (a, b) in enumerate(self.data):
            a, b = int(a), int(b)
            components[a].append((b, i))
            components[b].append((a, i))
        d = deque()
        d.append(([0], [], 0)) # tuple(pins), used components, score
        winner = None
        while d:
            state, used, score = d.popleft()
            pins = state[-1]
            for next_pins, id in components[pins]:
                if id in used:
                    continue
                new_score = score + pins + next_pins
                new_bridge = ([*state,next_pins], [*used, id], new_score)
                d.append(new_bridge)
                if winner is None or len(winner[1][0]) < len(new_bridge[0]) or (len(winner[1][0]) == len(new_bridge[0]) and winner[0] < new_score):
                    winner = (new_score, new_bridge)




        return winner


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = False
    STRIP = True
    SPLIT_LINES = True
    SPLIT_CHAR = '/'

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read(), PART2, STRIP, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())
