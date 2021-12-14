import itertools
import os
import re
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
        re_node = re.compile('(\w+) \((\d+)\)(?: -> )?(.*)')

        if type(data) is not list:
            data = [data]
        root = None
        nodes = {}
        for row in data:
            m = re_node.match(row)
            name = m.group(1)
            weight = int(m.group(2))
            childs = m.group(3).split(', ') if m.group(3) != '' else []
            nodes[name] = [name, weight, childs, None] # name, weight, childs, parent
                                                       #   0      1       2       3
        for k, v in nodes.items():
            for child in v[2]:
                nodes[child][3] = k

        for k, v in nodes.items():
            if v[3] is None:
                root = nodes[k]
                break

        print(self.balance(root[0], nodes))


    def balance(self, name, nodes):
        node = nodes[name]
        total_sum = node[1]
        sub_weights = [self.balance(n, nodes) for n in node[2]]

        if sub_weights and min(sub_weights) != max(sub_weights):
            print(f"{node}: {sub_weights}")
            self.dump_subtree(input(), nodes)
        total_sum += sum(sub_weights)
        return total_sum

    def dump_subtree(self, name, nodes, indent=0):
        node = nodes[name]
        print(" "*indent, nodes[name])
        for n in node[2]:
            self.dump_subtree(n, nodes, indent+2)


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
