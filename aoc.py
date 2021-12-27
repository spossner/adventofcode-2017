import collections
from itertools import chain

Point = collections.namedtuple('Point', 'x,y', defaults=[0, 0])
Point3d = collections.namedtuple('Point3d', 'x,y,z', defaults=[0, 0, 0])

NORTH = Point(0, -1)
EAST = Point(1, 0)
SOUTH = Point(0, 1)
WEST = Point(-1, 0)


def translate(p: Point, offset: Point) -> Point:
    return Point(p.x + offset.x, p.y + offset.y)


def rot_cw(p: Point) -> Point:
    return Point(-p.y, p.x)


def rot_ccw(p: Point) -> Point:
    return Point(p.y, -p.x)


def fetch(iterable, n, fillvalue=None):
    if len(iterable) >= n:
        return iterable[0:n]
    fill = [fillvalue] * (n - len(iterable))
    return chain(iterable, fill)


if __name__ == '__main__':
    assert rot_cw(Point(0, 1)) == (-1, 0)
    assert rot_ccw(Point(0, 1)) == (1, 0)
    assert rot_ccw(Point(1, 0)) == (0, -1)
