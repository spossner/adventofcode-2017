import operator
import os
import sys
from collections import deque, defaultdict, namedtuple
from functools import total_ordering, reduce
import bisect
from itertools import permutations, zip_longest, count

from aoc import fetch, Point, translate, rot_ccw, rot_cw, SOUTH
from hex import Hex
import networkx as nx


def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


DIRECTIONS = {
    '|': (Point(0, 1), Point(0, -1)),
    '-': (Point(1, 0), Point(-1, 0)),
}


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
        start_pos = None
        for x in count():
            if self.data[0][x] == '|':
                start_pos = Point(x, 0)
                break

        d = deque()
        d.append((start_pos, SOUTH))
        result = []
        steps = 0
        while d:
            pos, dir = d.popleft()
            if pos.x < 0 or pos.y < 0 or pos.y >= len(self.data) or pos.x >= len(self.data[pos.y]):
                continue  # point outside grid
            c = self.data[pos.y][pos.x]
            if c == ' ':
                continue  # illegal position
            elif c == '+':
                cw = rot_cw(dir)
                d.append((translate(pos, cw), cw))
                ccw = rot_ccw(dir)
                d.append((translate(pos, ccw), ccw))
                steps += 1
            else:
                # continue
                if c not in ('|', '-', '+'):
                    result.append(c)
                d.append((translate(pos, dir), dir))
                steps += 1
        if self.modified:
            return steps
        return ''.join(result)


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    STRIP = False
    SPLIT_LINES = True
    SPLIT_CHAR = ''

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read(), PART2, STRIP, SPLIT_LINES, SPLIT_CHAR)  # w/o strip!
        print(s.solve())
