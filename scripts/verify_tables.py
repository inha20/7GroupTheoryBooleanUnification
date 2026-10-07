import itertools
from collections import Counter

N = 4
PTS = list(itertools.product([0, 1], repeat=N))
IDX = {x: i for i, x in enumerate(PTS)}
GRAY = [(0, 0), (0, 1), (1, 1), (1, 0)]
S4 = list(itertools.permutations(range(N)))


def pperm(p):
    return [IDX[tuple(x[p[i]] for i in range(N))] for x in PTS]


PP = {p: pperm(p) for p in S4}


def act(f, pp):
    r = 0
    for i in range(16):
        if (f >> pp[i]) & 1:
            r |= 1 << i
    return r


def ctype(p):
    seen, out = set(), []
    for s in range(N):
        if s in seen:
            continue
        k, l = s, 0
        while k not in seen:
            seen.add(k)
            k = p[k]
            l += 1
        out.append(l)
    return tuple(sorted(out, reverse=True))


NAME = {(1, 1, 1, 1): "C1 id", (2, 1, 1): "C2 (12)", (2, 2): "C3 (12)(34)", (3, 1): "C4 (123)", (4,): "C5 (1234)"}
REP = {}
for p in S4:
    REP.setdefault(ctype(p), p)


def tbl(fn):
    return sum(fn(x) << i for i, x in enumerate(PTS))


full = range(1 << 16)


def mono(f):
    return all(not (all(a <= b for a, b in zip(x, y)) and (f >> i) & 1 and not (f >> j) & 1)
               for i, x in enumerate(PTS) for j, y in enumerate(PTS))


monotone = {f for f in full if mono(f)}
selfdual = {f for f in full if all(((f >> i) & 1) != ((f >> IDX[tuple(1 - v for v in x)]) & 1) for i, x in enumerate(PTS))}
affine = {tbl(lambda x, c=c: c[0] ^ (c[1] & x[0]) ^ (c[2] & x[1]) ^ (c[3] & x[2]) ^ (c[4] & x[3]))
          for c in itertools.product([0, 1], repeat=5)}


def report(name, space):
    space = set(space)
    print("==", name, len(space))
    tot = 0
    for ct, rep in REP.items():
        n = sum(1 for p in S4 if ctype(p) == ct)
        fx = sum(1 for f in space if act(f, PP[rep]) == f)
        tot += n * fx
        print(f"  {NAME[ct]:<12} |C|={n}  Fix={fx}")
    print("  orbits =", tot / 24)
    seen, sizes = set(), []
    for f in sorted(space):
        if f in seen:
            continue
        orb = {act(f, PP[p]) for p in S4}
        seen |= orb
        sizes.append(len(orb))
    print("  orbit sizes:", sorted(Counter(sizes).items()))


report("full", full)
report("affine", affine)
report("monotone", monotone)
report("selfdual", selfdual)

print("\n== stabilizer orders for affine reps")
for name, fn in [("x1", lambda x: x[0]), ("x1^x2", lambda x: x[0] ^ x[1]), ("x1^x2^x3", lambda x: x[0] ^ x[1] ^ x[2]), ("x1^x2^x3^x4", lambda x: x[0] ^ x[1] ^ x[2] ^ x[3])]:
    f = tbl(fn)
    st = [p for p in S4 if act(f, PP[p]) == f]
    print(name, "stab order", len(st), "orbit size", 24 // len(st))


def picture(f, sigma):
    rows = []
    for gi in GRAY:
        row = []
        for gj in GRAY:
            x = [0] * 4
            x[sigma[0]], x[sigma[1]] = gi
            x[sigma[2]], x[sigma[3]] = gj
            row.append((f >> IDX[tuple(x)]) & 1)
        rows.append(tuple(row))
    return tuple(rows)


def rot(a):
    return tuple(tuple(a[3 - j][i] for j in range(4)) for i in range(4))


def refl(a):
    return tuple(tuple(a[i][3 - j] for j in range(4)) for i in range(4))


def grid_sym(m):
    out = set()
    cands = []
    a = m
    for _ in range(4):
        cands.append(a)
        cands.append(refl(a))
        a = rot(a)
    for a in cands:
        for si in range(4):
            for sj in range(4):
                out.add(tuple(tuple(a[(i + si) % 4][(j + sj) % 4] for j in range(4)) for i in range(4)))
    return out


def show(m):
    return ["".join(str(v) for v in r) for r in m]


reps = {"AB/CD": (0, 1, 2, 3), "AC/BD": (0, 2, 1, 3), "AD/BC": (0, 3, 1, 2)}
for fname, fn in [("A^B^C^D (full xor)", lambda x: x[0] ^ x[1] ^ x[2] ^ x[3]), ("A^B", lambda x: x[0] ^ x[1]),
                  ("A&B", lambda x: x[0] & x[1]), ("A^B^C", lambda x: x[0] ^ x[1] ^ x[2])]:
    f = tbl(fn)
    print("\n--", fname)
    for k, s in reps.items():
        print(k, show(picture(f, s)))
    allpics = {picture(f, s) for s in S4}
    classes = {frozenset(grid_sym(p)) for p in allpics}
    print("distinct pictures over 24 arrangements:", len(allpics), " distinct up to grid symmetry W:", len(classes))
