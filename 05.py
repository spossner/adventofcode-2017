import itertools
import os
import sys
from collections import defaultdict, deque

WAYS = {
            (0, -1),
    (-1, 0),        (1, 0),
            (0, 1),
}

OFFSETS = {
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),           (1, 0),
    (-1, 1), (0, 1),   (1, 1,)
}

SPIRAL = [
    ((1,0), (0,-1)),
    ((-1,0),(0,1)),
]

class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]
        steps = [int(d) for d in data] # gives the number of steps to jmp each time
        #CODE HERE
        result = 0
        ptr = 0
        while ptr >= 0 and ptr < len(steps):
            i = ptr
            ptr += steps[i]
            if modified and steps[i] >= 3:
                steps[i] -= 1
            else:
                steps[i] += 1
            result += 1

        return result

if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    ## PART1

    # with open(f'{script}-dev.txt') as f:
    #     result = s.solve(f.read().strip().splitlines())
    #     print(result)
    #
    # with open(f'{script}.txt') as f:
    #     result = s.solve(f.read().strip().splitlines())
    #     print(result)

    ## MODIFIED -> PART2
    #
    with open(f'{script}-dev.txt') as f:
        result = s.solve(f.read().strip().splitlines(), True)
        print(result)

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines(), True)
        print(result)
    #
