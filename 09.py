import itertools
import os
import re
import sys
from collections import defaultdict, deque

DIRECT_ADJACENTS = {(0, -1),(-1, 0), (1, 0),(0, 1),} # 4 adjacent nodes
ALL_ADJACENTS = {(-1, -1), (0, -1), (1, -1),(-1, 0), (1, 0),(-1, 1), (0, 1), (1, 1,)}

class Solution:
    def solve(self, data, modified=False):
        stack = deque()
        skip_garbage = False
        escape = False
        score = 0
        count_garbage = 0
        for c in data:
            if skip_garbage:
                if escape:
                    escape = False
                    continue
                elif c == '!':
                    escape = True
                    continue
                elif c == '>': # garbage finished
                    skip_garbage = False
                else:
                    count_garbage += 1
            elif c == '<':
                skip_garbage = True
            elif c == '{':
                stack.append('}')
            elif c == '}':
                score += len(stack)
                assert stack.pop() == c
        return score if not modified else count_garbage


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    ## PART1

    assert s.solve('<>') == 0
    assert s.solve('<random characters>') == 0
    assert s.solve('<<<<>') == 0
    assert s.solve('<{!>}>') == 0
    assert s.solve('<!!>') == 0
    assert s.solve('<!!!>>') == 0
    assert s.solve('<{o"i!a,<{i<a>') == 0

    assert s.solve('{}') == 1
    assert s.solve('{{{}}}') == 6
    assert s.solve('{{},{}}') == 5
    assert s.solve('{{{},{},{{}}}}') == 16
    assert s.solve('{<a>,<a>,<a>,<a>}') == 1
    assert s.solve('{{<ab>},{<ab>},{<ab>},{<ab>}}') == 9
    assert s.solve('{{<!!>},{<!!>},{<!!>},{<!!>}}') == 9
    assert s.solve('{{<a!>},{<a!>},{<a!>},{<ab>}}') == 3

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip())
        print(result)

    ## MODIFIED -> PART2

    assert s.solve('<>', True) == 0
    assert s.solve('<random characters>', True) == 17
    assert s.solve('<<<<>', True) == 3
    assert s.solve('<{!>}>', True) == 2
    assert s.solve('<!!>', True) == 0
    assert s.solve('<!!!>>', True) == 0
    assert s.solve('<{o"i!a,<{i<a>', True) == 10

    #
    # with open(f'{script}-dev.txt') as f:
    #     result = s.solve(f.read().strip().splitlines(), True)
    #     print(result)
    #
    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip(), True)
        print(result)
    #
