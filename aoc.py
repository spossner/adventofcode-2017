from itertools import chain


def fetch(iterable, n, fillvalue=None):
    if len(iterable) >= n:
        return iterable[0:n]
    fill = [fillvalue] * (n-len(iterable))
    return chain(iterable, fill)