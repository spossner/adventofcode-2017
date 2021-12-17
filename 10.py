from __future__ import annotations
import itertools
import os
import re
import sys
from collections import defaultdict, deque
from functools import reduce

DIRECT_ADJACENTS = {(0, -1), (-1, 0), (1, 0), (0, 1), }  # 4 adjacent nodes
ALL_ADJACENTS = {(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1,)}


class ListNode:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def set_next(self, next: ListNode):
        self.next = next


class Solution:
    def solve(self, data, n=10, modified=False):
        numbers = list(range(n))
        ptr = 0
        skip_size = 0
        rounds = 1

        if modified:
            data = [*[ord(c) for c in data], *[17, 31, 73, 47, 23]]
            rounds = 64
        else:
            data = [int(d) for d in data]

        for r in range(rounds):
            for s in data:
                # self.dump_numbers(numbers, ptr)
                stripe = list(reversed([*numbers, *numbers][ptr:ptr + s]))
                # print(f"({stripe})")
                for i in range(s):
                    numbers[(ptr + i) % n] = stripe[i]
                ptr = (ptr + s + skip_size) % n
                skip_size += 1
            print(f"After round {r + 1}")
            self.dump_numbers(numbers, ptr)

        if not modified:
            return numbers[0] * numbers[1]

        result = []
        for i in range(len(numbers) >> 4):
            result.append(reduce(lambda a, b: a ^ b, numbers[i << 4:(i << 4) + 16]))
        print(''.join([f"{d:02x}" for d in result]))

    def dump_numbers(self, numbers, ptr=None):
        print(', '.join([str(d) if ptr is None or i != ptr else f"[{d}]" for i, d in enumerate(numbers)]))


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    ## PART1
    # with open(f'{script}-dev.txt') as f:
    #     result = s.solve(f.read().strip(), 5)
    #     print(result)
    #
    # with open(f'{script}.txt') as f:
    #     result = s.solve(f.read().strip(), 256)
    #     print(result)

    ## MODIFIED -> PART2

    # with open(f'{script}-dev.txt') as f:
    #     result = s.solve(f.read().strip(), 5, True)
    #     print(result)
    #
    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip(), 256, True)
        print(result)
    #
