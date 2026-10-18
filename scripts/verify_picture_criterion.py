"""
정리 4(2) 의 판정 기준 검증 (표준 라이브러리만 사용)

주장: 함수 f 의 B4-궤도 안의 W-궤도 수 (= 그림 종류 수) 는
      f 의 B4-안정화군 H_f 의 S4 성분들이 세 변수 쌍 분할
      {01|23}, {02|13}, {03|12} 위에 일으키는 치환군의 궤도 수와 같다.
      (S4 -> S3 의 상이 자명하면 3, 위수 2 이면 2, 3-순환을 포함하면 1)

추가로 (A) 부호 순환의 점 순환 수 공식 (정리 3 의 보조정리) 을 brute force 와 대조한다.
"""
import itertools
import math
from collections import Counter

N = 4
PTS = list(itertools.product([0, 1], repeat=N))
IDX = {x: i for i, x in enumerate(PTS)}


def signed_perm(pi, c):
    return [IDX[tuple(x[pi[i]] ^ c[i] for i in range(N))] for x in PTS]


def tables_for(point_perm, nbits=16):
    out = []
    for b in range(nbits // 8):
        t = []
        for v in range(256):
            r = 0
            for k in range(8):
                if (v >> k) & 1:
                    r |= 1 << point_perm[8 * b + k]
            t.append(r)
        out.append(t)
    return out


def act(f, tabs):
    r = 0
    for b, t in enumerate(tabs):
        r |= t[(f >> (8 * b)) & 255]
    return r


# ------------------------------------------------ 군 B4, W, 분할 위의 작용
PARTS = [frozenset({frozenset((0, 1)), frozenset((2, 3))}),
         frozenset({frozenset((0, 2)), frozenset((1, 3))}),
         frozenset({frozenset((0, 3)), frozenset((1, 2))})]


def part_perm(pi):
    img = []
    for P in PARTS:
        Q = frozenset(frozenset(pi[i] for i in blk) for blk in P)
        img.append(PARTS.index(Q))
    return tuple(img)


ELEMS = []   # (pi, c, 점치환, 조회표, 분할치환)
for pi in itertools.permutations(range(N)):
    for c in itertools.product([0, 1], repeat=N):
        pp = signed_perm(pi, c)
        ELEMS.append((pi, c, pp, tables_for(pp), part_perm(pi)))
assert len(ELEMS) == 384
W_IDX = [k for k, e in enumerate(ELEMS) if e[4][0] == 0]   # 분할 0 의 안정화군
assert len(W_IDX) == 128


def orbit_under(f, idxs):
    return {act(f, ELEMS[k][3]) for k in idxs}


def orbits_of_group_on_parts(perms):
    """분할 3개 위에서 치환들이 만드는 군의 궤도 수 (합집합-찾기)"""
    parent = list(range(3))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for p in perms:
        for a in range(3):
            ra, rb = find(a), find(p[a])
            if ra != rb:
                parent[ra] = rb
    return len({find(a) for a in range(3)})


def generated_group_size(perms):
    grp = {tuple(range(3))}
    changed = True
    while changed:
        changed = False
        for a in list(grp):
            for b in perms:
                c = tuple(b[a[i]] for i in range(3))
                if c not in grp:
                    grp.add(c)
                    changed = True
    return len(grp)


# ------------------------------------------------ 전수 대조 (402 개 B4-궤도)
seen = set()
by_criterion = Counter()
by_bruteforce = Counter()
image_sizes = Counter()
mismatch = 0
for f in range(1 << 16):
    if f in seen:
        continue
    ob = orbit_under(f, range(384))
    seen |= ob
    rem, k_brute = set(ob), 0            # (i) 정의대로: B4-궤도 안의 W-궤도 수
    while rem:
        g = next(iter(rem))
        rem -= orbit_under(g, W_IDX)
        k_brute += 1
    stab = {e[4] for e in ELEMS if act(f, e[3]) == f}   # (ii) 안정화군의 분할 치환상
    k_crit = orbits_of_group_on_parts(stab)
    image_sizes[generated_group_size(stab)] += len(ob)
    by_bruteforce[k_brute] += len(ob)
    by_criterion[k_crit] += len(ob)
    if k_brute != k_crit:
        mismatch += 1
        print("불일치:", f, k_brute, k_crit)

print("[기준 검증] B4-궤도 불일치 개수:", mismatch)
print("  정의대로 센 그림 종류별 함수 수  :", sorted(by_bruteforce.items()))
print("  S3-상 궤도 수 기준으로 센 함수 수:", sorted(by_criterion.items()))
print("  안정화군의 S3 상 크기별 함수 수 (1=자명, 2=위수 2, 3 또는 6=3-순환 포함):", sorted(image_sizes.items()))
assert mismatch == 0
assert (by_bruteforce[1], by_bruteforce[2], by_bruteforce[3]) == (3220, 36204, 26112)
assert image_sizes[1] == by_criterion[3] and image_sizes[2] == by_criterion[2]
assert image_sizes[3] + image_sizes[6] == by_criterion[1]


# ------------------------------------------------ (A) 부호 순환의 점 순환 수 공식
def fix_formula(l, sign, k):
    """부호 l-순환 g 의 g^k 의 고정점 수. g^k = (g^l)^q 와 이동 r 의 합성.
    이동 r 은 d = gcd(l, r) (r=0 이면 d=l) 개의 순환으로 좌표를 나누고,
    각 순환을 한 바퀴 돌 때 반전 횟수는 (r/d)*s + q*s*(l/d) (s=1 이면 음의 순환)."""
    s = 1 if sign < 0 else 0
    q, r = divmod(k, l)
    d = l if r == 0 else math.gcd(l, r)
    flips = (0 if r == 0 else (r // d) * s) + q * s * (l // d)
    return (1 << d) if flips % 2 == 0 else 0


def brute_cycles(l, sign):
    pts = list(itertools.product([0, 1], repeat=l))

    def g(x):
        y = [x[(i - 1) % l] for i in range(l)]
        if sign < 0:
            y[0] ^= 1                 # 이동하며 한 좌표를 반전
        return tuple(y)
    seen, dist = set(), Counter()
    for x in pts:
        if x in seen:
            continue
        length, y = 0, x
        while y not in seen:
            seen.add(y)
            y = g(y)
            length += 1
        dist[length] += 1
    return dist


print("\n[A] 부호 순환의 점 순환 길이 분포 (brute force) 와 Burnside 공식 대조")
EXPECT = {(1, 1): {1: 2}, (2, 1): {1: 2, 2: 1}, (3, 1): {1: 2, 3: 2}, (4, 1): {1: 2, 2: 1, 4: 3},
          (1, -1): {2: 1}, (2, -1): {4: 1}, (3, -1): {2: 1, 6: 1}, (4, -1): {8: 2}}
for (l, sg), want in sorted(EXPECT.items()):
    got = brute_cycles(l, sg)
    order = l if sg > 0 else 2 * l
    burn = sum(fix_formula(l, sg, k) for k in range(order)) // order
    ok = dict(got) == want and burn == sum(got.values())
    print("  l=%d %s: 분포 %s, 순환 수 %d, Burnside 공식 %d -> %s"
          % (l, "+" if sg > 0 else "-", dict(sorted(got.items())), sum(got.values()), burn, "OK" if ok else "불일치"))
    assert ok
print("\n전체: 통과")


# ------------------------------------------------ (B) 위수 3인 상이 나타나지 않는 이유 (정리 5 의 따름정리)
def comp(a, b):
    return [a[b[i]] for i in range(16)]


def inv(a):
    r = [0] * 16
    for i, v in enumerate(a):
        r[v] = i
    return r


def order_of(a):
    ident = list(range(16))
    cur, k = a, 1
    while cur != ident:
        cur = comp(a, cur)
        k += 1
    return k


def is_three_cycle(pi):
    moved = [i for i in range(N) if pi[i] != i]
    return len(moved) == 3


PURE = {}   # pi -> 순수 순열의 점치환
SIGN_ONLY = []
for e in ELEMS:
    pi, c, pp = e[0], e[1], e[2]
    if all(ci == 0 for ci in c):
        PURE[pi] = pp
    if pi == tuple(range(N)):
        SIGN_ONLY.append(pp)

orders = Counter()
for pi, c, pp, _, _ in ELEMS:
    if not is_three_cycle(pi):
        continue
    o = order_of(pp)
    orders[o] += 1
    if o == 3:   # 위수 3 인 원소는 부호 벡터 공액으로 순수 3-순환이 된다
        ok = any(comp(comp(u, pp), inv(u)) == PURE[pi] for u in SIGN_ONLY)
        assert ok, (pi, c)
print("\n[B] S4 성분이 3-순환인 B4 원소의 위수 분포:", sorted(orders.items()), "(3 또는 6 뿐)")
assert set(orders) <= {3, 6}

# C3 불변 => (12) 불변 (순수 순열에서)
c3, t12 = PURE[(1, 2, 0, 3)], PURE[(1, 0, 2, 3)]
bad = 0
for f in range(1 << 16):
    if act(f, tables_for(c3)) == f and act(f, tables_for(t12)) != f:
        bad += 1
print("    (123) 로 불변이지만 (12) 로 불변이 아닌 함수의 개수:", bad)
assert bad == 0
print("전체(B 포함): 통과")
