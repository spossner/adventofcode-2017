import math
import operator
import os
import sys
from collections import deque, defaultdict, namedtuple
from functools import total_ordering, reduce
import bisect
from itertools import permutations, zip_longest, count

from aoc import fetch, Point, translate, rot_ccw, rot_cw, SOUTH, Point3d, manhattan_distance
import networkx as nx
import pygame as pg
import numpy as np

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
        self.grid = None

    def split_pattern(self, s):
        return [tuple(map(lambda c: 0 if c == '.' else 1, list(row))) for row in s.split('/')]

    def solve(self, grid_string):
        pg.init()
        # getting the screen of the specified size
        screen = pg.display.set_mode(SIZE)
        font = pg.font.SysFont('OpenSans', 72)
        # getting the pg clock for handling fps
        clock = pg.time.Clock()

        rules = [[self.split_pattern(p) for p in row] for row in self.data]
        patterns = {}  # (size, tuple of flat left pattern): tuple of replacement
        for r in rules:
            source = np.array(r[0])
            dest = tuple(np.array(r[1]).flat)
            for i in range(4):
                a = np.rot90(source, i)
                patterns[tuple(a.flat)] = dest
                patterns[tuple(np.flipud(a).flat)] = dest
                patterns[tuple(np.fliplr(a).flat)] = dest
        print(patterns)

        self.grid = self.split_pattern(grid_string)
        print(self.grid)

        block_size = 20

        for _ in range(18):
            # getting the events
            for event in pg.event.get():
                # if the event is quit means we clicked on the close window button
                if event.type == pg.QUIT:
                    # quit the game
                    pg.quit()
                    sys.exit(0)

            clock.tick(FPS)
            # filling the screen with background color
            screen.fill(BACKGROUND_COLOR)
            # pg.draw.circle(screen, pg.Color('blue'), CENTER, 1)

            size = self.size()
            block_count = int(len(self.grid) / size)
            new_size = block_count * (size + 1)
            new_grid = [[0] * new_size for _ in range(new_size)]
            for row in range(block_count):
                for col in range(block_count):
                    block = tuple(self.block(row, col))
                    # print(block, patterns[block])
                    self.set_block(new_grid, row, col, patterns[block])
            self.grid = new_grid

            if block_size * len(self.grid) > min(WIDTH, HEIGHT):
                block_size = max(1, (min(WIDTH, HEIGHT) / len(self.grid)))

            offset = (len(self.grid) >> 1) * block_size
            TOP_LEFT = Point(CENTER.x - offset, CENTER.y - offset)
            for y in range(len(self.grid)):
                for x in range(len(self.grid)):
                    if self.grid[y][x]:
                        pg.draw.rect(screen, pg.Color('blue'),
                                     (TOP_LEFT.x + x * block_size, TOP_LEFT.y + y * block_size, block_size, block_size))

            pg.display.flip()

        total = 0
        for row in self.grid:
            total += sum(row)
        return total

    def size(self):
        if len(self.grid) & 1:  # odd
            return 3
        return 2

    def block(self, row, col):
        size = self.size()
        for y in range(size):
            for x in range(size):
                yield self.grid[row * size + y][col * size + x]

    def set_block(self, new_grid, row, col, pattern):
        size = int(math.sqrt(len(pattern)))
        for y in range(size):
            for x in range(size):
                new_grid[row * size + y][col * size + x] = pattern[y * size + x]


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = False
    STRIP = True
    SPLIT_LINES = True
    SPLIT_CHAR = ' => '

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read(), PART2, STRIP, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve('.#./..#/###'))
