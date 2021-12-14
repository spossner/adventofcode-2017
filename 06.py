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

        bank = [int(d) for d in data[0].split()]
        n = len(bank)
        #CODE HERE
        seen = {}
        steps = 0
        while True:
            key = str(bank)
            print(key)
            if key in seen:
                return steps-seen[key]
            seen[key] = steps
            pos = 0
            m = -1
            for i, v in enumerate(bank):
                if v > m:
                    m = v
                    pos = i
            bank[pos] = 0
            full, rest = int(m / n), m % n
            for i in range(n):
                bank[i] += full
            for i in range(rest):
                bank[(pos+i+1) % n] += 1
            steps += 1

if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    ## PART1

    with open(f'{script}-dev.txt') as f:
        result = s.solve(f.read().strip().splitlines())
        print(result)

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines())
        print(result)

    ## MODIFIED -> PART2
    #
    # with open(f'{script}-dev.txt') as f:
    #     result = s.solve(f.read().strip().splitlines(), True)
    #     print(result)
    #
    # with open(f'{script}.txt') as f:
    #     result = s.solve(f.read().strip().splitlines(), True)
    #     print(result)
    #
