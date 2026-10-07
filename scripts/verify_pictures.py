import itertools
from collections import Counter

PTS = list(itertools.product([0, 1], repeat=4))
IDX = {x: i for i, x in enumerate(PTS)}
GRAY = [(0, 0), (0, 1), (1, 1), (1, 0)]
CELLS = [(i, j) for i in range(4) for j in range(4)]  # cell k = 4*i + j


def cell_to_input_index(sigma):
    out = []
    for (i, j) in CELLS:
        x = [0] * 4
        x[sigma[0]], x[sigma[1]] = GRAY[i]
        x[sigma[2]], x[sigma[3]] = GRAY[j]
        out.append(IDX[tuple(x)])
    return out


def grid_perms():
    def rot(c):
        i, j = c
        return (j, 3 - i)

    def refl(c):
        i, j = c
        return (i, 3 - j)

    perms = set()
    for r in range(4):
        for fl in range(2):
            for si in range(4):
                for sj in range(4):
                    p = []
                    for c in CELLS:
                        d = c
                        for _ in range(r):
                            d = rot(d)
                        if fl:
                            d = refl(d)
                        d = ((d[0] + si) % 4, (d[1] + sj) % 4)
                        p.append(4 * d[0] + d[1])
                    perms.add(tuple(p))
    return list(perms)


W = grid_perms()
print("|W| =", len(W))
REPS = [(0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)]
C2I = [cell_to_input_index(s) for s in REPS]


def picture_bits(f, c2i):
    b = 0
    for k in range(16):
        b |= ((f >> c2i[k]) & 1) << k
    return b


def canon(b):
    best = None
    for p in W:
        r = 0
        for k in range(16):
            if (b >> k) & 1:
                r |= 1 << p[k]
        if best is None or r < best:
            best = r
    return best


cache = {}
dist = Counter()
example = {}
for f in range(1 << 16):
    cl = []
    for c2i in C2I:
        b = picture_bits(f, c2i)
        if b not in cache:
            cache[b] = canon(b)
        cl.append(cache[b])
    n = len(set(cl))
    dist[n] += 1
    if n not in example:
        example[n] = f
print("distinct picture-classes among the 3 reps -> number of functions:", sorted(dist.items()))
for n, f in sorted(example.items()):
    print("example with", n, "classes: f = 0x%04X" % f)
