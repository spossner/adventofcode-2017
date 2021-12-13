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
    def solve(self):
        #CODE HERE
        numbers = {}
        p = (0,0)
        numbers[p] = 1
        step = 1
        dir = 0
        while True:
            sp = SPIRAL[dir]
            for i in range(2):
                delta = SPIRAL[dir][i]
                for s in range(step):
                    np = (p[0]+delta[0], p[1]+delta[1])
                    sum = 0
                    for adj in OFFSETS:
                        ap = (np[0]+adj[0], np[1]+adj[1])
                        if ap in numbers:
                            sum += numbers[ap]
                    numbers[np] = sum
                    if numbers[np] > 325489:
                        return numbers[np]
                    p = np
            dir = 1 - dir # switch direction
            step += 1 # and increase step


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()
    print(s.solve())
