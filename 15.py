import operator
import os
import sys
from collections import deque, defaultdict
from functools import total_ordering, reduce
import bisect
from itertools import permutations, zip_longest

from hex import Hex
import networkx as nx

DIRECT_ADJACENTS = ((0, -1), (-1, 0), (1, 0), (0, 1))  # 4 adjacent nodes
ALL_ADJACENTS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
HEX_ADJACENTS = ((1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1))
BITS = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111',
}
BITS_LIST = (
    '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111',)


def direct_adjacents(x, y, w, h):
    for dx, dy in DIRECT_ADJACENTS:
        nx = x + dx
        ny = y + dy
        if nx < 0 or ny < 0 or nx >= w or ny >= h:
            continue
        yield (nx, ny)

def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def to_hex(n):
    result = []
    for c in n:
        result.append(BITS[c])
    return ''.join(result)


class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self, a, b):
        fa = 16807
        fb = 48271
        m = 2147483647

        print(f"{'--Gen. A--':>10} {'--Gen. B--':>10}")
        total = 0
        #for i in range(40000000):
        for i in range(5000000):
        #for i in range(5):
            if i % 10000 == 0:
                print('.', end='')
            if i % 100000 == 0:
                print()
            while True:
                a = (a * fa) % m
                if not self.modified or (a & 0b11) == 0b00:
                    break
            while True:
                b = (b * fb) % m
                if not self.modified or (b & 0b111) == 0b000:
                    break
            # print(f"{a:>10} {b:>10}")
            ba = bin(a)[-16:]
            bb = bin(b)[-16:]
            if ba == bb:
                total += 1
                #print(f"{ba:>10}\n{bb:>10}")
        print()
        return total



if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    SPLIT_LINES = False
    SPLIT_CHAR = None

    # for i in range(32):
    #     print(i, bin(i), (i & 0b111) == 0b000)

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
        # print(s.solve(65, 8921))
        print(s.solve(634, 301))
