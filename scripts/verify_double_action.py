"""
verify_double_action.py
=======================
논문 7의 6.1절 "(D4 x S4) 이중 작용"을 명시적 모델로 계산한다.

모델:
  - 카르노맵 셀 (i, j) <-> 입력 x = (gray(i), gray(j)), gray = (00,01,11,10)
  - S4  : 변수 순열이 입력점 16개를 치환 -> 함수 f에 작용
  - D4  : 4x4 격자의 회전/반사 8개가 셀(=입력점) 16개를 치환 -> 함수 f에 작용
  - T   : 토러스 순환 이동 Z4 x Z4 (16개)
  - 합성군 G = <S4, D4> 의 크기와 F4 위의 궤도 수를 열거로 계산

사용법: python scripts/verify_double_action.py
의존성: Python 3.8+, 표준 라이브러리만 사용.
"""
import itertools

N = 4
INPUTS = list(itertools.product([0, 1], repeat=N))
IDX = {x: i for i, x in enumerate(INPUTS)}
GRAY = [(0, 0), (0, 1), (1, 1), (1, 0)]
GRAY_INV = {g: i for i, g in enumerate(GRAY)}


def cell_of(x):
    return GRAY_INV[(x[0], x[1])], GRAY_INV[(x[2], x[3])]


def input_of(i, j):
    return GRAY[i % 4] + GRAY[j % 4]


def compose(p, q):
    """(p o q)[k] = p[q[k]]"""
    return tuple(p[q[k]] for k in range(16))


def closure(gens):
    ident = tuple(range(16))
    group = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                c = compose(h, g)
                if c not in group:
                    group.add(c)
                    nxt.append(c)
        frontier = nxt
    return group


def s4_perm(p):
    return tuple(IDX[tuple(x[p[i]] for i in range(N))] for x in INPUTS)


def grid_perm(fn):
    perm = []
    for x in INPUTS:
        i, j = cell_of(x)
        a, b = fn(i, j)
        perm.append(IDX[input_of(a, b)])
    return tuple(perm)


S4_GENS = [s4_perm((1, 0, 2, 3)), s4_perm((1, 2, 3, 0))]
D4_GENS = [grid_perm(lambda i, j: (j, 3 - i)), grid_perm(lambda i, j: (i, 3 - j))]
T_GENS = [grid_perm(lambda i, j: (i + 1, j)), grid_perm(lambda i, j: (i, j + 1))]


def act(f, pp):
    r = 0
    for i in range(16):
        if (f >> pp[i]) & 1:
            r |= 1 << i
    return r


def count_orbits(space, group):
    space = set(space)
    seen, orbs = set(), 0
    for f in sorted(space):
        if f in seen:
            continue
        orbs += 1
        seen.update(act(f, pp) for pp in group)
    return orbs


def closed(space, group):
    space = set(space)
    return all(act(f, pp) in space for f in space for pp in group)


def tbl(fn):
    return sum(fn(x) << i for i, x in enumerate(INPUTS))


def main():
    S4 = closure(S4_GENS)
    D4 = closure(D4_GENS)
    D4T = closure(D4_GENS + T_GENS)
    G = closure(S4_GENS + D4_GENS)
    GT = closure(S4_GENS + D4_GENS + T_GENS)

    print("군 크기: S4=%d  D4(격자)=%d  D4+토러스이동=%d  <S4,D4>=%d  <S4,D4,T>=%d"
          % (len(S4), len(D4), len(D4T), len(G), len(GT)))
    print("D4 와 S4 의 교집합 크기:", len(S4 & D4), "(D4 가 S4 의 부분군이면 8)")
    comm = all(compose(a, b) == compose(b, a) for a in S4_GENS for b in D4_GENS)
    print("S4 생성원과 D4 생성원이 모두 가환:", comm, "(False 이면 직접곱 작용이 아님)")

    full = range(1 << 16)
    print("\n전체 공간 F4(65536) 궤도 수:")
    for name, grp in [("S4", S4), ("D4(격자)", D4), ("D4+토러스", D4T), ("<S4,D4>", G), ("<S4,D4,T>", GT)]:
        print("  %-10s 군크기 %3d  궤도 %5d" % (name, len(grp), count_orbits(full, grp)))

    affine = {tbl(lambda x, c=c: c[0] ^ (c[1] & x[0]) ^ (c[2] & x[1]) ^ (c[3] & x[2]) ^ (c[4] & x[3]))
              for c in itertools.product([0, 1], repeat=5)}
    selfdual = {f for f in full
                if all(((f >> i) & 1) != ((f >> IDX[tuple(1 - v for v in x)]) & 1) for i, x in enumerate(INPUTS))}
    print("\n<S4,D4> 하에서 부분공간의 닫힘과 궤도 수:")
    for name, sp in [("아핀(32)", affine), ("자기쌍대(256)", selfdual)]:
        print("  %-14s 닫힘=%s  궤도 %d" % (name, closed(sp, G), count_orbits(sp, G)))

    # 변수 배치 24개 -> 동치류: 배치 sigma 의 "셀 -> 입력점" 사상이 격자 대칭 g 로 서로 옮겨지는지
    arrs = list(itertools.permutations(range(4)))

    def arrangement_map(sigma):
        return {cell_of(tuple(x[sigma[k]] for k in range(4))): x for x in INPUTS}

    maps = [arrangement_map(s) for s in arrs]

    def classes(grid_gens):
        grid_group = closure(grid_gens)
        parent = list(range(len(arrs)))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        for a in range(len(arrs)):
            for gp in grid_group:
                img = {c: INPUTS[gp[IDX[x]]] for c, x in maps[a].items()}
                for b in range(len(arrs)):
                    if maps[b] == img:
                        parent[find(a)] = find(b)
        return len({find(a) for a in range(len(arrs))})

    print("\n변수 배치 24개의 동치류 수:")
    print("  D4(격자 8개)만      :", classes(D4_GENS))
    print("  D4 + 토러스 이동    :", classes(D4_GENS + T_GENS))


if __name__ == "__main__":
    main()
