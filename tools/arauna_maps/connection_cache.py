"""Source rectangles copied by Emerald's four Fill*Connection functions.

The engine expands the destination by seven cells on each side. East copies
eight source columns; the other directions copy seven rows/columns.
"""
def rectangle(cw, ch, pw, ph, offset, direction):
    if direction in ('left', 'right'):
        start = offset + 7
        source_start = max(0, -start)
        length = min(start + ph, ch + 14) if start < 0 else min(ph, ch + 14 - start)
        xs = range(pw - 7, pw) if direction == 'left' else range(8)
        points = [(x, y) for y in range(source_start, source_start + max(0, length)) for x in xs]
    else:
        if direction not in ('up', 'down'):
            raise ValueError(direction)
        start = offset + 7
        source_start = max(0, -start)
        length = min(start + pw, cw + 14) if start < 0 else min(pw, cw + 14 - start)
        ys = range(ph - 7, ph) if direction == 'up' else range(7)
        points = [(x, y) for y in ys for x in range(source_start, source_start + max(0, length))]
    assert all(0 <= x < pw and 0 <= y < ph for x, y in points)
    return points
