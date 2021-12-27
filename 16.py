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

    def solve(self, chars, rounds=1):
        chars = list(chars)

        # pre-compile
        ops = []
        for cmd in self.data:
            if cmd[0] == 's':
                ops.append(('s', int(cmd[1:])))
            elif cmd[0] == 'x':
                p1, p2 = map(int, cmd[1:].split('/'))
                ops.append(('x', p1, p2))
            else:
                p1, p2 = cmd[1:].split('/')
                ops.append(('p', p1, p2))


        result = ''.join(chars)
        seen = set()
        seen.add(result)
        found_patterns = {}
        found_patterns[0] = result
        # print(1000000000 % 30)
        #for r in range(1000000000 % 30):
        for r in range(rounds):
            for cmd in ops:
                if cmd[0] == 's':
                    chars = chars[-cmd[1]:] + chars[:-cmd[1]]
                elif cmd[0] == 'x':
                    chars[cmd[2]], chars[cmd[1]] = chars[cmd[1]], chars[cmd[2]]
                else:
                    found = 0
                    for i in range(len(chars)):
                        if chars[i] == cmd[1]:
                            chars[i] = cmd[2]
                            found += 1
                        elif chars[i] == cmd[2]:
                            chars[i] = cmd[1]
                            found += 1
                        if found == 2:
                            break
            dances = r + 1
            result = ''.join(chars)
            print(f"{dances}: {result}")
            if result in seen:
                print(f"{r+1} already found {result}")
                return found_patterns[(rounds % dances)]
            seen.add(result)
            found_patterns[dances] = result

        return ''.join(chars)


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    INPUT = 'abcdefghijklmnop'
    # INPUT = 'abcde'
    PART2 = False
    SPLIT_LINES = False
    SPLIT_CHAR = ','

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve(INPUT, 1000))
