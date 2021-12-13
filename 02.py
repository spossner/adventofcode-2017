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


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        #CODE HERE
        sum = 0
        for row in data:
            nums = [int(d) for d in row.split()]
            if modified:
                print(nums)
                d = 0
                for a, b in itertools.combinations(nums, 2):
                    a, b = max(a,b), min(a,b)
                    if a % b == 0:
                        d = int(a / b)
                        break
                assert d != 0
            else:
                d = max(nums) - min(nums)
            print(nums, d)
            sum += d
        return sum


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

    with open(f'{script}-dev2.txt') as f:
        result = s.solve(f.read().strip().splitlines(), True)
        print(result)

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines(), True)
        print(result)
