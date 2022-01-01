import collections
from itertools import chain
from typing import Union

Point = collections.namedtuple('Point', 'x,y', defaults=[0, 0])
Point3d = collections.namedtuple('Point3d', 'x,y,z', defaults=[0, 0, 0])

NORTH = Point(0, -1)
EAST = Point(1, 0)
SOUTH = Point(0, 1)
WEST = Point(-1, 0)


def translate(p: Union[Point, Point3d, tuple], offset: Union[Point, Point3d, tuple]) -> Union[Point, Point3d, tuple]:
    if type(p) == Point:
        return Point(p.x + offset.x, p.y + offset.y)
    if type(p) == Point3d:
        return Point3d(p.x + offset.x, p.y + offset.y, p.z + offset.z)
    if type(p) == tuple:
        assert len(p) == len(offset)
        result = []
        for i in range(len(p)):
            result.append(p[i]+offset[i])
        return tuple(result)
    raise ValueError(f'can not translate {type(p)}')


def rot_cw(p: Point) -> Point:
    return Point(-p.y, p.x)


def rot_ccw(p: Point) -> Point:
    return Point(p.y, -p.x)


def manhattan_distance(p) -> int:
    return sum(map(abs, p))


def fetch(iterable, n, fillvalue=None):
    if len(iterable) >= n:
        return iterable[0:n]
    fill = [fillvalue] * (n - len(iterable))
    return chain(iterable, fill)


if __name__ == '__main__':
    assert rot_cw(Point(0, 1)) == (-1, 0)
    assert rot_ccw(Point(0, 1)) == (1, 0)
    assert rot_ccw(Point(1, 0)) == (0, -1)

    assert manhattan_distance((1, 2, -3)) == 6
    assert manhattan_distance(Point3d(1, 2, -3)) == 6
    assert manhattan_distance(Point(-2, -4)) == 6
