import itertools
import os
import re
import sys
from collections import defaultdict, deque

DIRECT_ADJACENTS = {(0, -1),(-1, 0), (1, 0),(0, 1),} # 4 adjacent nodes
ALL_ADJACENTS = {(-1, -1), (0, -1), (1, -1),(-1, 0), (1, 0),(-1, 1), (0, 1), (1, 1,)}

class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]
        # c inc -20 if c == 10
        registers = defaultdict(int)
        max_value = None
        ops = [(a.split(), b.split()) for a, b in [row.split(' if ') for row in data]]
        for cmd, cond in ops:
            register, operator, operand = cond
            value = registers[register]
            operand = int(operand)
            if operator == '<' and value >= operand: # skip
                continue
            elif operator == '>' and value <= operand: # skip
                continue
            elif operator == '<=' and value > operand: # skip
                continue
            elif operator == '>=' and value < operand: # skip
                continue
            elif operator == '==' and value != operand: # skip
                continue
            elif operator == '!=' and value == operand: # skip
                continue
            register, operator, operand = cmd
            operand = int(operand)
            if operator == 'dec':
                operand = -operand
            registers[register] += operand
            if max_value is None or max_value < registers[register]:
                max_value = registers[register]
            # print(registers)
        return max_value if modified else max(registers.values())

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
