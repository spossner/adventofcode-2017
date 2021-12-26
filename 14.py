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


def knot_hash(lengths, lst=range(256)):
    lst = list(lst)
    pos = 0
    for skip, n in enumerate(lengths):
        lst = lst[pos:] + lst[:pos]
        lst[:n] = lst[n - 1::-1]
        lst = lst[-pos:] + lst[:-pos]
        pos += n + skip
        pos %= len(lst)
    return lst


def knot_hash_mul(lengths, lst=range(256)):
    a, b, *_ = knot_hash(lengths, lst)
    return a * b


def knot_hash_rounds(chars, lst=range(256)):
    lengths = list(map(ord, chars)) + [17, 31, 73, 47, 23]
    sparse = knot_hash(lengths * 64, lst)
    dense = (reduce(operator.xor, block) for block in grouper(sparse, 16))
    return ''.join(map('{:02x}'.format, dense))


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

    def solve(self):
        total = 0
        grid = []
        todos = deque()
        for i in range(128):
            k = f"{self.data}-{i}"
            bits = list(map(int, list(to_hex(knot_hash_rounds(k)))))
            grid.append(bits)
            total += sum(bits)
            for x, v in enumerate(bits):
                if v == 1:
                    todos.append((x, i))  # (x, y) in deque
        print(f"PART 1: {total}")
        seen = set()
        r_count = 0
        regions = defaultdict(list)
        while todos:  # as long as there are entries in d
            k = (x, y) = todos.popleft()
            if k in seen:
                continue
            r_count += 1
            # print(f"new region {r_count}")
            seen.add(k)
            regions[r_count].append(k)
            d = deque()
            d.append(k)
            while d:
                x, y = d.popleft()
                for ax, ay in direct_adjacents(x, y, 128, 128):
                    l = (ax, ay)
                    if grid[ay][ax] == 0:
                        continue
                    if l in seen:
                        continue
                    seen.add(l)
                    d.append(l)
                    regions[r_count].append(l)
        print(f"PART 2: {len(regions.keys())}")



if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = False
    SPLIT_LINES = None
    SPLIT_CHAR = None

    #s = Solution('flqrgnkx', PART2, SPLIT_LINES, SPLIT_CHAR)
    s = Solution('hwlqcszp', PART2, SPLIT_LINES, SPLIT_CHAR)
    s.solve()
