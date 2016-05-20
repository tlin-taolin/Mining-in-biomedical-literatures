def magicsplit(l, *splitters):
    return [subl for subl in _itersplit(l, splitters) if subl]


def _itersplit(l, splitters):
    current = []
    for item in l:
        if item in splitters:
            yield current
            current = []
        else:
            current.append(item)
    yield current
