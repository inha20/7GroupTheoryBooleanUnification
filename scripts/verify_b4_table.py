import itertools
from math import factorial
from collections import Counter

N = 4
PTS = list(itertools.product([0, 1], repeat=N))
IDX = {x: i for i, x in enumerate(PTS)}


def partitions(n, maxp=None):
    maxp = maxp or n
    if n == 0:
        yield ()
        return
    for k in range(min(n, maxp), 0, -1):
        for r in partitions(n - k, k):
            yield (k,) + r


def build(lam, mu):
    """대표원: g(x)_i = x_{pi(i)} xor c_i"""
    pi = list(range(N))
    c = [0] * N
    pos = 0
    for sign, part in ((0, lam), (1, mu)):
        for l in part:
            for k in range(l):
                pi[pos + k] = pos + (k + 1) % l
            c[pos] = sign
            pos += l
    return pi, c


def point_perm(pi, c):
    return [IDX[tuple(x[pi[i]] ^ c[i] for i in range(N))] for x in PTS]


def cycles(perm):
    seen, out = set(), []
    for s in range(len(perm)):
        if s in seen:
            continue
        cyc, k = [], s
        while k not in seen:
            seen.add(k)
            cyc.append(k)
            k = perm[k]
        out.append(cyc)
    return out


def fix_sd(perm):
    comp = [IDX[tuple(1 - v for v in x)] for x in PTS]
    cyc = cycles(perm)
    where = {p: i for i, cy in enumerate(cyc) for p in cy}
    for i, cy in enumerate(cyc):
        if where[comp[cy[0]]] == i:
            return 0, len(cyc)
    return 2 ** (len(cyc) // 2), len(cyc)


def centralizer(lam, mu):
    r = 1
    for part in (lam, mu):
        for l, m in Counter(part).items():
            r *= (2 * l) ** m * factorial(m)
    return r


rows = []
for a in range(N + 1):
    for lam in partitions(a):
        for mu in partitions(N - a):
            pi, c = build(lam, mu)
            pp = point_perm(pi, c)
            size = 384 // centralizer(lam, mu)
            f, cc = fix_sd(pp)
            rows.append((lam, mu, size, cc, 2 ** cc, f))

print("classes:", len(rows))
print("sum size:", sum(r[2] for r in rows))
for lam, mu, size, cc, fa, fs in rows:
    print(f"({','.join(map(str, lam)) or '-'} | {','.join(map(str, mu)) or '-'})  size={size:>3}  c={cc:>2}  2^c={fa:>6}  FixSD={fs:>4}")
print("orbits all:", sum(r[2] * r[4] for r in rows) / 384)
print("orbits selfdual:", sum(r[2] * r[5] for r in rows) / 384)

cnt = 0
sumall = 0
sumsd = 0
cls = Counter()
for pi in itertools.permutations(range(N)):
    for c in itertools.product([0, 1], repeat=N):
        pp = point_perm(pi, c)
        cnt += 1
        sumall += 2 ** len(cycles(pp))
        sumsd += fix_sd(pp)[0]
        seen = set()
        lam, mu = [], []
        for s in range(N):
            if s in seen:
                continue
            k, l, par = s, 0, 0
            while k not in seen:
                seen.add(k)
                par ^= c[k]
                k = pi[k]
                l += 1
            (mu if par else lam).append(l)
        cls[(tuple(sorted(lam, reverse=True)), tuple(sorted(mu, reverse=True)))] += 1
print("brute: |B4|=", cnt, " all orbits", sumall / cnt, " selfdual orbits", sumsd / cnt)
print("class sizes match:", all(cls[(r[0], r[1])] == r[2] for r in rows))
