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
        row = data[0]
        sum = 0
        n = len(row)
        delta = n >> 1
        for i in range(n):
            d = delta if modified else 1
            if row[i] == row[(i+d) % n]:
                sum += int(row[i])

        return sum


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    ## PART1

    assert s.solve('1122') == 3
    assert s.solve('1111') == 4
    assert s.solve('1234') == 0
    assert s.solve('91212129') == 9

    # with open(f'{script}-dev.txt') as f:
    #     result = s.solve(f.read().strip().splitlines())
    #     print(result)

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines())
        print(result)


    ## MODIFIED -> PART2

    assert s.solve('1212', True) == 6
    assert s.solve('1221', True) == 0
    assert s.solve('123425', True) == 4
    assert s.solve('123123', True) == 12
    assert s.solve('12131415', True) == 4


    # with open(f'{script}-dev.txt') as f:
    #     result = s.solve(f.read().strip().splitlines(), True)
    #     print(result)

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines(), True)
        print(result)
