import os
import sys
from collections import deque, defaultdict
from functools import total_ordering, reduce
import bisect
from itertools import permutations

from hex import Hex
import networkx as nx

DIRECT_ADJACENTS = ((0, -1), (-1, 0), (1, 0), (0, 1))  # 4 adjacent nodes
ALL_ADJACENTS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
HEX_ADJACENTS = ((1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1))

class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self):
        G = nx.Graph()
        for node, edges in self.data:
            for e in edges.split(', '):
                G.add_edge(e,node)
                G.add_edge(node,e)
        #print(G.nodes)
        #print(list(G.edges))
        if self.modified:
            return len(list(nx.connected_components(G)))
        return len(nx.node_connected_component(G, '0'))


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    SPLIT_LINES = True
    SPLIT_CHAR = ' <-> '

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())

