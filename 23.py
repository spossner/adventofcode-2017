
import os
import sys
from collections import deque, defaultdict
from copy import deepcopy
from itertools import  zip_longest
import pygame as pg

from aoc import fetch
from colorama import   Cursor

SIZE = WIDTH, HEIGHT = 800, 600  # the width and height of our screen
CENTER = (WIDTH >> 1, HEIGHT >> 1)
BACKGROUND_COLOR = pg.Color('white')  # The background color of our window
FPS = 60  # Frames per second

RUNNING = 1
WAITING = 2

MINY, MAXY = 1, 24
MINX, MAXX = 1, 80

pos = lambda x, y: Cursor.POS(x, y)


def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Thread:
    def __init__(self, id, data, clone_data=False):
        self.id = id
        self.ptr = 0
        self.registers = defaultdict(int)
        self.registers['p'] = self.id
        self.queue = deque()
        self.status = RUNNING
        self.msg_count = 0
        self.data = deepcopy(data) if clone_data else data

    def __str__(self):
        return f"{self.id} ({self.status}): {self.registers} with {self.queue} ({self.msg_count})"

    def __repr__(self):
        return self.__str__()

    def has_next(self):
        return 0 <= self.ptr < len(self.data)

    def next(self):
        return self.data[self.ptr]

    def increase_ptr(self, offset=1):
        self.ptr += offset

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
        return not self.has_next()

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
        pg.init()
        screen = pg.display.set_mode(SIZE)
        font = pg.font.SysFont('OpenSans', 22)
        clock = pg.time.Clock()


        threads = []
        for i in range(n):
            t = Thread(i, self.data)
            if self.modified:
                t.set('a', 1)
            threads.append(t)

        last_sound = None
        running = True
        paused = False
        step = 0
        count = 0
        while running:
            for e in pg.event.get():
                if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_SPACE:
                        paused = not paused
                    elif e.key == pg.K_RIGHT:
                        step = 1

            clock.tick(FPS)
            screen.fill(BACKGROUND_COLOR)

            t = threads[0]
            for i, cmd in enumerate(t.data):
                text = font.render(f"{i:<2}: {cmd}", True, pg.Color('black'),  pg.Color('red') if t.ptr == i else BACKGROUND_COLOR)
                screen.blit(text, (20, 10+i*(font.get_height()+3)))

            for i, k in enumerate('abcdefgh'):
                text = font.render(f"{k}: {t.get(k)}", True, pg.Color('black'))
                screen.blit(text, (200, 10 + i * (font.get_height() + 3)))

            pg.display.flip()

            if step > 0:
                step -= 1
                paused = True
            elif paused:
                continue

            running = False
            for thread in threads:
                if thread.is_finished() or thread.is_blocked():
                    continue  # finished or blocked
                running = True  # at least one thread is running
                ops = thread.next()  # self.data[thread.ptr]
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
                    thread.set(a1, thread.get(a1) + thread.get(a2))
                elif cmd == 'sub':
                    thread.set(a1, thread.get(a1) - thread.get(a2))
                elif cmd == 'mul':
                    count += 1
                    thread.set(a1, thread.get(a1) * thread.get(a2))
                elif cmd == 'mod':
                    thread.set(a1, thread.get(a1) % thread.get(a2))
                elif cmd == 'rcv':
                    if self.modified:
                        msg = thread.receive()
                        if msg:
                            thread.set(a1, msg)
                        else:
                            continue  # keep thread.ptr
                    elif thread.get(a1) > 0:
                        print(f"recover sound {last_sound}")
                        if last_sound > 0:
                            return last_sound
                elif cmd == 'jgz':
                    if thread.get(a1) > 0:
                        thread.increase_ptr(thread.get(a2))
                        continue
                elif cmd == 'jnz':
                    if thread.get(a1) != 0:
                        thread.increase_ptr(thread.get(a2))
                        continue
                thread.increase_ptr()

        #print(Back.WHITE)
        print(count)
        return threads


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    SPLIT_LINES = True
    SPLIT_CHAR = ' '

    # colorama.init()
    # clear_screen()

    # with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
    #     s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
    #     print(s.solve())

    # get no of non prime numbers from 107900 to 124900 (incl) with step width 17
    # 107900, 107917, 107934,..., 124866, 124883, 124900 --> 907 times non prime

    total = 0
    a, b = 107900, 124900
    for i in range(a, b + 1, 17):
        flag = 1

        for j in range(2, i // 2 + 1):
            if i % j == 0:
                flag = 0
                break

        # flag = 1 means i is prime
        # and flag = 0 means i is not prime
        if flag == 0:
            total += 1
            print(i, total)


# 906 -> TOO LOW
# 907 -> correct
