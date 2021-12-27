import operator
import os
import sys
from collections import deque, defaultdict, namedtuple
from functools import total_ordering, reduce
import bisect
from itertools import permutations, zip_longest

from aoc import fetch
from hex import Hex
import networkx as nx

FINISHED = 0
RUNNING = 1
WAITING = 2

def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

class Thread:
    def __init__(self, id):
        self.id = id
        self.ptr = 0
        self.registers = defaultdict(int)
        self.registers['p'] = self.id
        self.queue = deque()
        self.status = RUNNING
        self.msg_count = 0

    def __str__(self):
        return f"{self.id} ({self.status}): {self.registers} with {self.queue} ({self.msg_count})"

    def __repr__(self):
        return self.__str__()

    def send(self, msg):
        self.msg_count += 1
        self.queue.append(msg)

    def has_messages(self):
        return len(self.queue) > 0

    def receive(self):
        if self.queue:
            self.status = RUNNING
            return self.queue.popleft()
        self.status = WAITING
        return None

    def is_finished(self):
        return self.status == FINISHED

    def is_blocked(self):
        return self.status == WAITING and not self.queue

    def set(self, key, value):
        self.registers[key] = self.get(value)

    def get(self, value_or_key):
        try:
            return int(value_or_key)
        except ValueError:
            return self.registers[value_or_key]


class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if data and do_splitlines:
            data = data.splitlines()
        if data and split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified


    def solve(self, n=1):
        threads = []
        for i in range(n):
            threads.append(Thread(i))

        last_sound = None
        running = True
        while running:
            running = False
            for thread in threads:
                if thread.is_finished() or thread.is_blocked():
                    continue # finished or blocked
                running = True # at least one thread is running
                ops = self.data[thread.ptr]
                cmd, a1, a2 = fetch(ops, 3)
                # print(ops, a1, a2)
                if cmd == 'snd':
                    last_sound = thread.get(a1)
                    if self.modified:
                        threads[(thread.id + 1) % len(threads)].send(last_sound)
                    else:
                        print(f"playing sound {last_sound}")
                elif cmd == 'set':
                    thread.set(a1, a2)
                elif cmd == 'add':
                    thread.set(a1, thread.get(a1)+thread.get(a2))
                elif cmd == 'mul':
                    thread.set(a1, thread.get(a1)*thread.get(a2))
                elif cmd == 'mod':
                    thread.set(a1, thread.get(a1) % thread.get(a2))
                elif cmd == 'rcv':
                    if self.modified:
                        msg = thread.receive()
                        if msg:
                            thread.set(a1, msg)
                        else:
                            continue # keep thread.ptr
                    elif thread.get(a1) > 0:
                        print(f"recover sound {last_sound}")
                        if last_sound > 0:
                            return last_sound
                elif cmd == 'jgz':
                    if thread.get(a1) > 0:
                        thread.ptr += thread.get(a2)
                        continue
                thread.ptr += 1
        return threads

if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    SPLIT_LINES = True
    SPLIT_CHAR = ' '

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve(2))


