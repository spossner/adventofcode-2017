import math
import operator
import os
import sys
from collections import deque, defaultdict, namedtuple
from functools import total_ordering, reduce
import bisect
from itertools import permutations, zip_longest, count

import networkx as nx
import pygame as pg
import numpy as np

from aoc import Point, NORTH, rot_ccw, rot_cw, translate

STATES = ".W#F"

SIZE = WIDTH, HEIGHT = 800, 600  # the width and height of our screen
CENTER = Point(WIDTH >> 1, HEIGHT >> 1)
BACKGROUND_COLOR = pg.Color('white')  # The background color of our window
FPS = 24  # Frames per second


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

    def solve(self, rounds=10000):
        grid = defaultdict(int)  # 0 = clean; 1 = infected
        for y, row in enumerate(self.data):
            for x, c in enumerate(row):
                if c == '#':
                    grid[(x, y)] = 2
        pos = (len(self.data[0]) >> 1, len(self.data) >> 1)
        dir = NORTH

        # pg.init()
        # screen = pg.display.set_mode(SIZE)
        # font = pg.font.SysFont('OpenSans', 72)
        # clock = pg.time.Clock()
        total = 0
        for i in range(rounds):
            #self.dump(grid, pos, dir)

            # for event in pg.event.get():
            #     if event.type == pg.QUIT:
            #         pg.quit()
            #         sys.exit(0)
            # clock.tick(FPS)
            # screen.fill(BACKGROUND_COLOR)
            if grid[pos] == 0:
                dir = rot_ccw(dir)
            elif grid[pos] == 1:
                total += 1
            elif grid[pos] == 2:
                dir = rot_cw(dir)
            elif grid[pos] == 3:
                dir = Point(-dir.x, -dir.y)
            grid[pos] = (grid[pos] + 1) % 4
            pos = translate(pos, dir)

            # pg.display.flip()

        return total

    def dump(self, grid, pos, dir):
        for y in range(-5, 5):
            for x in range(-10, 10):
                v = grid[(x, y)]
                print(f"{STATES[v]}", end='')
                if pos[1] == y and pos[0] == x + 1:
                    print('[', end='')
                elif pos[1] == y and pos[0] == x:
                    print(']', end='')
                else:
                    print(' ', end='')
            print()
        print()


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
        print(s.solve(10000000))
