"""
단조 함수의 S4 Fix 값의 이론적 유도 검증 (표준 라이브러리만 사용)

주장: 순열 g 로 불변인 단조 함수의 개수 Fix(g) 는
      2^[4] 의 <g>-궤도들 위의 순서집합 P_g (궤도 O <= O' 는 어떤 a in O, a' in O' 에
      대해 a ⊆ a' 일 때) 의 상집합(up-set) 의 개수와 같다.
      특수한 경우:
        (123)   : P = 사슬 [4] x 사슬 [2]                  -> C(6,2) = 15
        (12)    : P = 사슬 [3] x 사슬 [2] x 사슬 [2]        -> 평면분할 PP(2,2,3) = 50
        (1234)  : P = 6원소 순서집합                        -> 8
        (12)(34): P = 10원소 순서집합                       -> 28
        id      : P = 2^[4]                                 -> Dedekind 수 168
"""
from math import comb

N = 4
SUBSETS = list(range(1 << N))


def apply_perm_to_set(perm, s):
    r = 0
    for i in range(N):
        if (s >> i) & 1:
            r |= 1 << perm[i]
    return r


def group_closure(gen):
    ident = tuple(range(N))
    g = {ident}
    cur = ident
    while True:
        cur = tuple(gen[cur[i]] for i in range(N))
        if cur in g:
            break
        g.add(cur)
    return g


def orbit_poset(gen):
    G = group_closure(gen)
    orbit_of = {}
    orbits = []
    for s in SUBSETS:
        if s in orbit_of:
            continue
        ob = frozenset(apply_perm_to_set(p, s) for p in G)
        for t in ob:
            orbit_of[t] = len(orbits)
        orbits.append(ob)
    k = len(orbits)
    leq = [[False] * k for _ in range(k)]
    for i, O in enumerate(orbits):
        for j, P in enumerate(orbits):
            leq[i][j] = any((a & b) == a for a in O for b in P)
    for m in range(k):
        for i in range(k):
            if leq[i][m]:
                for j in range(k):
                    if leq[m][j]:
                        leq[i][j] = True
    return orbits, leq


def count_upsets(k, leq):
    """상집합 개수: i in U, i <= j 이면 j in U"""
    cnt = 0
    for mask in range(1 << k):
        ok = True
        for i in range(k):
            if (mask >> i) & 1:
                for j in range(k):
                    if leq[i][j] and not (mask >> j) & 1:
                        ok = False
                        break
                if not ok:
                    break
        if ok:
            cnt += 1
    return cnt


def brute_fix(gen):
    """정의대로: 단조이면서 g 로 불변인 4변수 함수의 수 (2^16 전수)"""
    G = group_closure(gen)
    cnt = 0
    for f in range(1 << 16):
        mono = True
        for x in range(16):
            if (f >> x) & 1:
                for i in range(N):
                    if not (f >> (x | (1 << i))) & 1:
                        mono = False
                        break
            if not mono:
                break
        if not mono:
            continue
        if all(((f >> apply_perm_to_set(p, x)) & 1) == ((f >> x) & 1) for p in G for x in range(16)):
            cnt += 1
    return cnt


CLASSES = [("id", (0, 1, 2, 3), 1, 168), ("(12)", (1, 0, 2, 3), 6, 50), ("(12)(34)", (1, 0, 3, 2), 3, 28),
           ("(123)", (1, 2, 0, 3), 8, 15), ("(1234)", (1, 2, 3, 0), 6, 8)]

total = 0
print("순열      | 궤도 수 | 상집합 수 | 정의대로 센 Fix | 기대값")
for name, gen, size, want in CLASSES:
    orbits, leq = orbit_poset(gen)
    ups = count_upsets(len(orbits), leq)
    brute = brute_fix(gen)
    print("%-9s %7d %10d %14d %10d" % (name, len(orbits), ups, brute, want))
    assert ups == brute == want, name
    total += size * want
print("가중합 = %d, /24 = %d (단조 S4-궤도 수)" % (total, total // 24))
assert total == 720 and total // 24 == 30


def plane_partitions(a, b, c):
    """a x b 바닥, 높이 <= c 인 평면분할 수 (MacMahon 공식)"""
    num, den = 1, 1
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            num *= i + j + c - 1
            den *= i + j - 1
    return num // den


assert comb(6, 2) == 15 and plane_partitions(2, 2, 3) == 50
print("닫힌 형태: (123) -> C(6,2) = 15, (12) -> PP(2,2,3) = 50: 일치")
print("전체: 통과")
