import operator
import os
import sys
from collections import deque, defaultdict, namedtuple
from functools import total_ordering, reduce
import bisect
from itertools import permutations, zip_longest, count

from aoc import fetch, Point, translate, rot_ccw, rot_cw, SOUTH, Point3d, manhattan_distance
from hex import Hex
import networkx as nx
import pygame as pg

SIZE = WIDTH, HEIGHT = 800, 600  # the width and height of our screen
BACKGROUND_COLOR = pg.Color('white')  # The background colod of our window
FPS = 50  # Frames per second


def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


DIRECTIONS = {
    '|': (Point(0, 1), Point(0, -1)),
    '-': (Point(1, 0), Point(-1, 0)),
}


class Dot:
    def __init__(self, p: Point3d, v: Point3d, a: Point3d):
        self.p = p
        self.v = v
        self.a = a

    def move(self):
        self.v = translate(self.v, self.a)
        self.p = translate(self.p, self.v)


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
        pg.init()
        # getting the screen of the specified size
        screen = pg.display.set_mode(SIZE)
        font = pg.font.SysFont('OpenSans', 72)
        # getting the pg clock for handling fps
        clock = pg.time.Clock()

        swarm = [Dot(*[Point3d(*map(int, p[3:-1].split(','))) for p in row]) for row in self.data]
        scale = 0.01
        for i in range(2000):
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
            pg.draw.circle(screen, pg.Color('blue'), ((WIDTH >> 1), (HEIGHT >> 1)), 1)

            if self.modified:
                seen = set()
                collide = set()
                for d in swarm:
                    if d.p in seen:
                        collide.add(d.p)
                        continue
                    seen.add(d.p)
                swarm = list(filter(lambda d: d.p not in collide, swarm))

            result = None
            for j,d in enumerate(swarm):
                pg.draw.circle(screen, pg.Color('red'), ((WIDTH >> 1) + d.p.x * scale, (HEIGHT >> 1) + d.p.y * scale), 1)
                if result is None or manhattan_distance(d.p) < result[0]:
                    result = (manhattan_distance(d.p), d, j)
                d.move()
            if i % 10 == 0:
                if self.modified:
                    print(len(swarm))
                else:
                    print(result[2], result[1].p)
                if result[1].p.x * scale > (WIDTH >>1) or result[1].p.y * scale > (HEIGHT >>1):
                    scale = min((WIDTH >>1) / result[1].p.x, (HEIGHT>>1)/result[1].p.y) / 2.3
            pg.draw.line(screen, pg.Color('green'), (WIDTH >> 1, HEIGHT >> 1), ((WIDTH >> 1) + result[1].p.x * scale, (HEIGHT >> 1) + result[1].p.y * scale))

            pg.display.flip()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    STRIP = False
    SPLIT_LINES = True
    SPLIT_CHAR = ', '

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read(), PART2, STRIP, SPLIT_LINES, SPLIT_CHAR)  # w/o strip!
        print(s.solve())
