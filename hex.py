from __future__ import nested_scopes
from __future__ import division
import math
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


class Hex:
    def __init__(self, q, r, s):
        assert (round(q + r + s) == 0), "q + r + s must be 0"
        self.q = q
        self.r = r
        self.s = s

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __sub__(self, other):
        return Hex(self.q - other.q, self.r - other.r, self.s - other.s)

    def __add__(self, other):
        return Hex(self.q + other.q, self.r + other.r, self.s + other.s)

    def __mul__(self, k):
        return Hex(self.q * k, self.r * k, self.s * k)

    def __str__(self):
        return f"({self.q},{self.r},{self.s})"

    def rotate_left(self):
        return Hex(-self.s, -self.q, -self.r)

    def rotate_right(self):
        return Hex(-self.r, -self.s, -self.q)

    def direction(self, dir):
        return HEX_DIRECTIONS[dir] if type(dir) == int else HEX_NAMED_DIRECTIONS[dir]

    def neighbor(self, dir):
        return self + self.direction(dir)

    def diagonal_neighbor(self, dir):
        return self + HEX_DIAGONALS[dir]

    def length(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2

    def distance(self, b):
        return (self - b).length()

    def round(self):
        qi = int(round(self.q))
        ri = int(round(self.r))
        si = int(round(self.s))
        q_diff = abs(qi - self.q)
        r_diff = abs(ri - self.r)
        s_diff = abs(si - self.s)
        if q_diff > r_diff and q_diff > s_diff:
            qi = -ri - si
        else:
            if r_diff > s_diff:
                ri = -qi - si
            else:
                si = -qi - ri
        return Hex(qi, ri, si)

    def lerp(self, b, t):
        return Hex(self.q * (1.0 - t) + b.q * t, self.r * (1.0 - t) + b.r * t, self.s * (1.0 - t) + b.s * t)

    def linedraw(self, b):
        N = self.distance(b)
        a_nudge = Hex(self.q + 1e-06, self.r + 1e-06, self.s - 2e-06)
        b_nudge = Hex(b.q + 1e-06, b.r + 1e-06, b.s - 2e-06)
        results = []
        step = 1.0 / max(N, 1)
        for i in range(0, N + 1):
            results.append(a_nudge.lerp(b_nudge, step * i).round())
        return results


HEX_DIRECTIONS = [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]
HEX_NAMED_DIRECTIONS = {'n': Hex(0, -1, 1), 'ne': Hex(1, -1, 0), 'se': Hex(1, 0, -1), 's': Hex(0, 1, -1), 'sw': Hex(-1, 1, 0), 'nw': Hex(-1, 0, 1)}
HEX_DIAGONALS = [Hex(2, -1, -1), Hex(1, -2, 1), Hex(-1, -1, 2), Hex(-2, 1, 1), Hex(-1, 2, -1), Hex(1, 1, -2)]


# Tests
def test_hex_arithmetic():
    assert Hex(1, -3, 2) + Hex(3, -7, 4) == Hex(4, -10, 6)
    assert Hex(1, -3, 2) - Hex(3, -7, 4) == Hex(-2, 4, -2)


def test_hex_direction():
    assert Hex(0, -1, 1) == HEX_DIRECTIONS[2]
    assert Hex(0, 1, -1) == HEX_NAMED_DIRECTIONS['s']
    for h in HEX_DIRECTIONS:
        assert h.length() == 1

def test_hex_neighbor():
    assert Hex(1, -2, 1).neighbor(2) == Hex(1, -3, 2)


def test_hex_diagonal():
    assert Hex(1, -2, 1).diagonal_neighbor(3) == Hex(-1, -1, 2)


def test_hex_distance():
    assert Hex(3, -7, 4).distance(Hex(0, 0, 0)) == 7


def test_hex_rotate_right():
    assert Hex(1, -3, 2).rotate_right() == Hex(3, -2, -1)


def test_hex_rotate_left():
    assert Hex(1, -3, 2).rotate_left() == Hex(-2, -1, 3)


def test_hex_round():
    a = Hex(0.0, 0.0, 0.0)
    b = Hex(1.0, -1.0, 0.0)
    c = Hex(0.0, -1.0, 1.0)
    assert Hex(0.0, 0.0, 0.0).lerp(Hex(10.0, -20.0, 10.0), 0.5).round() == Hex(5, -10, 5)
    # equal_hex("hex_round 2", hex_round(a), hex_round(hex_lerp(a, b, 0.499)))
    # equal_hex("hex_round 3", hex_round(b), hex_round(hex_lerp(a, b, 0.501)))
    # equal_hex("hex_round 4", hex_round(a),
    #           hex_round(Hex(a.q * 0.4 + b.q * 0.3 + c.q * 0.3, a.r * 0.4 + b.r * 0.3 + c.r * 0.3, a.s * 0.4 + b.s * 0.3 + c.s * 0.3)))
    # equal_hex("hex_round 5", hex_round(c),
    #           hex_round(Hex(a.q * 0.3 + b.q * 0.3 + c.q * 0.4, a.r * 0.3 + b.r * 0.3 + c.r * 0.4, a.s * 0.3 + b.s * 0.3 + c.s * 0.4)))


# def test_hex_linedraw():
#     equal_hex_array("hex_linedraw", [Hex(0, 0, 0), Hex(0, -1, 1), Hex(0, -2, 2), Hex(1, -3, 2), Hex(1, -4, 3), Hex(1, -5, 4)],
#                     hex_linedraw(Hex(0, 0, 0), Hex(1, -5, 4)))


def test_all():
    test_hex_arithmetic()
    test_hex_direction()
    test_hex_neighbor()
    test_hex_diagonal()
    test_hex_distance()
    test_hex_rotate_right()
    test_hex_rotate_left()
    test_hex_round()
    # test_hex_linedraw()
    # test_layout()


if __name__ == '__main__':
    test_all()
