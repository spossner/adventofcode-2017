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

##
# 0        0, 0          0
# 1r 1o    1,0 | 1,-1     1 | 2
# 2l 2u    0,-1 -1,-1 | -1,0 -1,1         1 2 | 1 2
# 3r 3o             1 2 3 | 2 3 4
# 4l 4u             3 2 3 4 | 3 2 3 4
# 5r 5o             3 2 3 4 5 | 4 3 4 5 6


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        #CODE HERE
        result = 0
        for passphrase in data:
            words = passphrase.split()
            if modified:
                for i in range(len(words)):
                    words[i] = ''.join(sorted(words[i]))
            unique = set(words)
            if len(words) == len(unique):
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

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines())
        print(result)

    ## MODIFIED -> PART2
    #
    # with open(f'{script}-dev2.txt') as f:
    #     result = s.solve(f.read().strip().splitlines(), True)
    #     print(result)
    #
    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines(), True)
        print(result)
    #
