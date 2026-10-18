"""
안정화군 격자 위의 뫼비우스/포함-배제로 계수를 유도하고 열거와 대조한다 (표준 라이브러리만 사용)

(A) 단조 함수의 S4-궤도 크기 분포: S4 의 부분군 30개 위에서 정확한 안정화군 개수를 뫼비우스 반전으로 구한다.
    Fix(H) = 단조 함수 중 H 로 불변인 것의 수 (168 개 단조 함수 목록으로 계산).
(B) 그림 종류별 함수 개수: B4 의 원소 집합 T 에 대해
        #{f : f 가 T 의 어떤 원소로 불변} = Σ_{S ⊆ 순환부분군(T), S≠∅} (-1)^{|S|+1} 2^{orb(<S>)}
    을 군의 폐포(생성된 군) 위의 동적계획법으로 계산한다. 함수는 세지 않고 군 <S> 의 점 궤도 수만 쓴다.
      - T = S4 성분이 3-순환인 원소 -> 3,220  (안정화군의 S3 상이 S3 인 함수)
      - T = S3 상이 호환인 원소 전부  -> 39,424 = 36,204 + 3,220
"""
import itertools
from collections import Counter

N = 4
PTS = list(itertools.product([0, 1], repeat=N))
IDX = {x: i for i, x in enumerate(PTS)}


def signed_perm(pi, c):
    return tuple(IDX[tuple(x[pi[i]] ^ c[i] for i in range(N))] for x in PTS)


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def orbits_count(gens, n=16):
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for g in gens:
        for i in range(n):
            ra, rb = find(i), find(g[i])
            if ra != rb:
                parent[ra] = rb
    return len({find(i) for i in range(n)})


ID16 = tuple(range(16))


def closure(gens):
    seen = {ID16}
    frontier = [ID16]
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                y = compose(g, x)
                if y not in seen:
                    seen.add(y)
                    nxt.append(y)
        frontier = nxt
    return frozenset(seen)


# ------------------------------------------------ (A) 단조 함수의 궤도 크기 분포
def monotone_list():
    out = []
    for f in range(1 << 16):
        ok = True
        for x in range(16):
            if (f >> x) & 1:
                for i in range(N):
                    if not (f >> (x | (1 << i))) & 1:
                        ok = False
                        break
            if not ok:
                break
        if ok:
            out.append(f)
    return out


MONO = monotone_list()
assert len(MONO) == 168
S4 = [signed_perm(pi, (0, 0, 0, 0)) for pi in itertools.permutations(range(N))]


def fixed_by(f, g):
    return all(((f >> g[x]) & 1) == ((f >> x) & 1) for x in range(16))


subgroups = {closure([])}
for a in S4:
    for b in S4:
        subgroups.add(closure([a, b]))
subgroups = sorted(subgroups, key=lambda H: -len(H))
print("[A] S4 의 부분군 수:", len(subgroups), "(30 이어야 함)")
assert len(subgroups) == 30

fix = {H: sum(1 for f in MONO if all(fixed_by(f, h) for h in H)) for H in subgroups}
exact = {}
for H in subgroups:                       # 위수 큰 것부터: 정확히 H 가 안정화군인 함수 수
    exact[H] = fix[H] - sum(exact[K] for K in exact if H < K)
assert all(v >= 0 for v in exact.values())
by_order = Counter()
for H, v in exact.items():
    by_order[len(H)] += v
print("   안정화군 위수별 단조 함수 수:", sorted(by_order.items(), reverse=True))
size_dist = {}
for k, cnt in by_order.items():
    size = 24 // k
    assert cnt % size == 0
    size_dist[size] = cnt // size
size_dist = {s: c for s, c in size_dist.items() if c}
print("   궤도 크기별 궤도 수:", sorted(size_dist.items()))
assert size_dist == {1: 6, 3: 2, 4: 9, 6: 6, 12: 7}
print("   (크기 24 궤도 없음 = 안정화군이 자명한 단조 함수가 없음)")

# ------------------------------------------------ (B) B4 위의 포함-배제 (함수를 세지 않음)
ELEMS = []
for pi in itertools.permutations(range(N)):
    for c in itertools.product([0, 1], repeat=N):
        ELEMS.append((pi, c, signed_perm(pi, c)))
assert len(ELEMS) == 384

PARTS = [frozenset({frozenset((0, 1)), frozenset((2, 3))}),
         frozenset({frozenset((0, 2)), frozenset((1, 3))}),
         frozenset({frozenset((0, 3)), frozenset((1, 2))})]


def s3_type(pi):
    p = tuple(PARTS.index(frozenset(frozenset(pi[i] for i in blk) for blk in P)) for P in PARTS)
    fixed = sum(1 for i in range(3) if p[i] == i)
    return {3: "id", 1: "transposition", 0: "3cycle"}[fixed]


def inclusion_exclusion(element_perms):
    """element_perms 의 어떤 원소로 불변인 함수의 수. 군 폐포 위의 동적계획."""
    cyc = {}
    for g in element_perms:
        C = closure([g])
        if len(C) > 1:
            cyc[C] = g
    cycs = list(cyc.items())
    print("   서로 다른 순환부분군 수:", len(cycs))
    state = {}                        # 생성된 군(원소 집합) -> [계수, 생성원 목록]
    join_cache = {}
    for C, g in cycs:
        new_state = {k: [v[0], v[1]] for k, v in state.items()}
        for G, (coef, gens) in state.items():
            key = (G, C)
            if key not in join_cache:
                if C <= G:
                    join_cache[key] = (G, gens)
                else:
                    ng = gens + [g]
                    join_cache[key] = (closure(ng), ng)
            J, jg = join_cache[key]
            if J in new_state:
                new_state[J][0] -= coef
            else:
                new_state[J] = [-coef, jg]
        if C in new_state:
            new_state[C][0] += 1
        else:
            new_state[C] = [1, [g]]
        state = {k: v for k, v in new_state.items() if v[0] != 0}
    return sum(coef * (1 << orbits_count(gens)) for G, (coef, gens) in state.items()), len(state)


three_cycle = [e[2] for e in ELEMS if s3_type(e[0]) == "3cycle"]
transp = [e[2] for e in ELEMS if s3_type(e[0]) == "transposition"]
print("\n[B] S3 상이 3-순환인 원소 %d개, 호환인 원소 %d개" % (len(three_cycle), len(transp)))
n3, st3 = inclusion_exclusion(three_cycle)
print("   S4 성분이 3-순환인 원소로 불변인 함수 수:", n3, "(DP 상태 %d개)" % st3)
assert n3 == 3220
nt, stt = inclusion_exclusion(transp)
print("   S3 상이 호환인 원소로 불변인 함수 수:", nt, "(DP 상태 %d개)" % stt)
assert nt == 36204 + 3220, nt
print("   => 상이 자명한 함수 수 = 65536 - %d = %d" % (nt, 65536 - nt))
assert 65536 - nt == 26112
print("\n전체: 통과")
