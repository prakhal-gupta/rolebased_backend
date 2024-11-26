def first(iterable):
    if len(iterable) == 0:
        return None
    return iterable[0]


def next(data):
    return data[1:]


def arithmetic_progression(step=1, start=1):
    i = start
    while True:
        yield i
        i += step
