from __future__ import annotations

import os
import sys
from copy import deepcopy
from functools import reduce

from knot_hash import KnotHash

DIRECT_ADJACENTS = {(0, -1), (-1, 0), (1, 0), (0, 1), }  # 4 adjacent nodes
ALL_ADJACENTS = {(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1,)}

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
}
BITS_LIST = (
'0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111',)


class Solution:
    def solve(self, data, n=10, modified=False):
        numbers = list(range(n))
        rounds = 1
        if modified:
            data = [*[ord(c) for c in data], *[17, 31, 73, 47, 23]]
            rounds = 64
        else:
            data = [int(d) for d in data]

        numbers = KnotHash.encrypt(numbers, data, rounds)

        if not modified:
            return numbers[0] * numbers[1]

        result = []
        for i in range(len(numbers) >> 4):
            result.append(reduce(lambda a, b: a ^ b, numbers[i << 4:(i << 4) + 16]))
        print(''.join([f"{d:02x}" for d in result]))




if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    ## PART1
    with open(f'{script}-dev.txt') as f:
        result = s.solve(f.read().strip().split(','), 5)
        print(result)
    #
    # with open(f'{script}.txt') as f:
    #     result = s.solve(f.read().strip(), 256)
    #     print(result)

    ## MODIFIED -> PART2

    # with open(f'{script}-dev.txt') as f:
    #     result = s.solve(f.read().strip(), 5, True)
    #     print(result)
    #
    # with open(f'{script}.txt') as f:
    #     result = s.solve(f.read().strip(), 256, True)
    #     print(result)
    #
