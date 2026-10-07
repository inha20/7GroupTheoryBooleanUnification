"""
verify_extras.py
================
논문 7의 보강 항목을 전수 계산으로 검증한다 (표준 라이브러리만 사용).

  A. 패리티 함수의 카르노맵 그림: Gray 축 순서에서는 체커보드, 이진 축 순서에서는 아님
  B. 시각적 대칭 = W 안정화군 원소 (1장 §5.8의 예시 함수 검증)
  C. B4-궤도가 W-궤도로 쪼개지는 개수(1, 2, 3)와 "세 배치 그림 종류" 개수의 대응
  D. 단조 함수 30개 S4-궤도의 대표 함수 목록 (크기와 서로 다름, 168개 전부 포괄)
  E. L ∩ M 의 3개 궤도
  F. n=5: 아핀 64개의 S5-궤도 12개, 단조 7,581개의 S5-궤도 210개

사용법: python scripts/verify_extras.py
"""
import itertools
from collections import Counter

# ---------------------------------------------------------------- 공통 (n=4)
N = 4
PTS = list(itertools.product([0, 1], repeat=N))
IDX = {x: i for i, x in enumerate(PTS)}
GRAY = [(0, 0), (0, 1), (1, 1), (1, 0)]


def tables_for(point_perm, nbits):
    """점 치환 -> 함수 작용을 바이트 단위 조회표로 구현 (궤도 구조는 작용 규약과 무관)"""
    nbytes = nbits // 8   # nbits = 입력점의 개수 (= 함수 진리표의 비트 수)
    out = []
    for b in range(nbytes):
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


def signed_perm(pi, c, pts, idx, n):
    return [idx[tuple(x[pi[i]] ^ c[i] for i in range(n))] for x in pts]


# B4 전체와 W (좌표쌍 분할 {{0,1},{2,3}} 의 안정화군)
TARGET = {frozenset((0, 1)), frozenset((2, 3))}
B4 = []
W = []
for pi in itertools.permutations(range(N)):
    for c in itertools.product([0, 1], repeat=N):
        pp = signed_perm(pi, c, PTS, IDX, N)
        B4.append(pp)
        if {frozenset((pi[0], pi[1])), frozenset((pi[2], pi[3]))} == TARGET:
            W.append(pp)
assert len(B4) == 384 and len(W) == 128, (len(B4), len(W))

# 격자 대칭(회전·반사·이동·전치)으로부터 만든 군이 위 W 와 같은지 확인
cell_in = lambda i, j: IDX[GRAY[i % 4] + GRAY[j % 4]]
cell_of = {IDX[GRAY[i] + GRAY[j]]: (i, j) for i in range(4) for j in range(4)}


def grid_perm(fn):
    return tuple(cell_in(*fn(*cell_of[k])) for k in range(16))


def closure(gens):
    ident = tuple(range(16))
    seen, frontier = {ident}, [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                c = tuple(h[g[k]] for k in range(16))
                if c not in seen:
                    seen.add(c)
                    nxt.append(c)
        frontier = nxt
    return seen


gens = [grid_perm(lambda i, j: (j, 3 - i)), grid_perm(lambda i, j: (i, 3 - j)),
        grid_perm(lambda i, j: (i + 1, j)), grid_perm(lambda i, j: (i, j + 1))]
grid_group = closure(gens)
assert grid_group == {tuple(p) for p in W}, "격자 대칭군 != 좌표쌍 안정화군"
print("[기본] |B4| = %d, |W| = %d, 격자 대칭군 = 좌표쌍 안정화군: 일치" % (len(B4), len(W)))

TB4 = [tables_for(p, 16) for p in B4]
TW = [tables_for(p, 16) for p in W]


# ---------------------------------------------------------------- A. 패리티 체커보드
def picture(f, row_order, col_order):
    return [[(f >> IDX[ri + ci]) & 1 for ci in col_order] for ri in row_order]


parity = sum(((sum(x)) & 1) << i for i, x in enumerate(PTS))
gray_pic = picture(parity, GRAY, GRAY)
bin_order = [(0, 0), (0, 1), (1, 0), (1, 1)]
bin_pic = picture(parity, bin_order, bin_order)
adj_ok = all(gray_pic[i][j] != gray_pic[(i + 1) % 4][j] and gray_pic[i][j] != gray_pic[i][(j + 1) % 4]
             for i in range(4) for j in range(4))
print("\n[A] 패리티(XOR) 그림, Gray 축 순서 (토러스 인접 포함 모든 인접 셀 값이 반대):", adj_ok)
for r in gray_pic:
    print("    ", "".join(map(str, r)))
print("    이진 축 순서(00,01,10,11):")
for r in bin_pic:
    print("    ", "".join(map(str, r)))
assert adj_ok


# ---------------------------------------------------------------- B. 시각적 대칭 = W 안정화군
def minterms_to_f(ms):
    return sum(1 << m for m in ms)  # 입력 인덱스 = ABCD 이진수 (A 가 최상위)


def stab_W(f):
    return sum(1 for t in TW if act(f, t) == f)


print("\n[B] 1장 §5.8 예시 함수의 W 안정화군 크기 (>1 이면 시각적 대칭 존재)")
tau = signed_perm((2, 3, 0, 1), (0, 0, 0, 0), PTS, IDX, 4)          # F(A,B,C,D)=F(C,D,A,B)
tau_neg = signed_perm((2, 3, 0, 1), (1, 0, 1, 0), PTS, IDX, 4)      # F(A,B,C,D)=F(~C,D,~A,B)
t1, t2 = tables_for(tau, 16), tables_for(tau_neg, 16)
for name, ms in [("m(5,6,9,10)", [5, 6, 9, 10]), ("m(0,6,9,15)", [0, 6, 9, 15]), ("m(1,4,7,11,13,14)", [1, 4, 7, 11, 13, 14])]:
    f = minterms_to_f(ms)
    print("    %-20s |Stab_W| = %3d   F=F(C,D,A,B): %-5s  F=F(~C,D,~A,B): %-5s"
          % (name, stab_W(f), act(f, t1) == f, act(f, t2) == f))
assert tuple(tau) in {tuple(p) for p in W} and tuple(tau_neg) in {tuple(p) for p in W}


# ---------------------------------------------------------------- C. B4-궤도의 W-궤도 분할
def orbit(f, tabs):
    return {act(f, t) for t in tabs}


seen = set()
split = Counter()      # k -> 함수 개수
b4_orbits = 0
w_orbits_total = 0
for f in range(1 << 16):
    if f in seen:
        continue
    ob = orbit(f, TB4)
    seen |= ob
    b4_orbits += 1
    rem = set(ob)
    k = 0
    while rem:
        g = next(iter(rem))
        rem -= orbit(g, TW)
        k += 1
    w_orbits_total += k
    split[k] += len(ob)
print("\n[C] B4-궤도 %d개, W-궤도 합계 %d개" % (b4_orbits, w_orbits_total))
print("    B4-궤도가 W-궤도 k개로 쪼개질 때 그 함수 개수:", sorted(split.items()))
print("    (3.5절의 '세 배치 그림 종류 1/2/3종' 함수 개수 3,220 / 36,204 / 26,112 와 일치해야 함)")
assert (split[1], split[2], split[3]) == (3220, 36204, 26112) and w_orbits_total == 805 and b4_orbits == 402

# ---------------------------------------------------------------- D. 단조 30궤도 대표 목록
LET = {"A": 0, "B": 1, "C": 2, "D": 3}


def terms_to_f(terms):
    f = 0
    for i, x in enumerate(PTS):
        sup = {k for k in range(4) if x[k]}
        if any({LET[ch] for ch in t} <= sup for t in terms):
            f |= 1 << i
    return f


ONE = [""]          # 빈 항 = 상수 1
REPS = [
    ("O01", "0", []), ("O02", "ABCD", ["ABCD"]), ("O03", "Maj3", ["ABC", "ABD", "ACD", "BCD"]),
    ("O04", "Maj2", ["AB", "AC", "AD", "BC", "BD", "CD"]), ("O05", "A∨B∨C∨D", ["A", "B", "C", "D"]), ("O06", "1", ONE),
    ("O07", "AB∨CD", ["AB", "CD"]), ("O08", "(A∨B)(C∨D)", ["AC", "AD", "BC", "BD"]),
    ("O09", "BCD", ["BCD"]), ("O10", "BCD∨ACD∨ABD", ["BCD", "ACD", "ABD"]), ("O11", "CD∨BD∨AD", ["CD", "BD", "AD"]),
    ("O12", "D", ["D"]), ("O13", "CD∨BD∨BC", ["CD", "BD", "BC"]), ("O14", "CD∨BD∨AD∨ABC", ["CD", "BD", "AD", "ABC"]),
    ("O15", "D∨ABC", ["D", "ABC"]), ("O16", "D∨BC∨AC∨AB", ["D", "BC", "AC", "AB"]), ("O17", "D∨C∨B", ["D", "C", "B"]),
    ("O18", "BCD∨ACD", ["BCD", "ACD"]), ("O19", "CD", ["CD"]), ("O20", "CD∨ABD∨ABC", ["CD", "ABD", "ABC"]),
    ("O21", "CD∨BD∨BC∨AD∨AC", ["CD", "BD", "BC", "AD", "AC"]), ("O22", "D∨C", ["D", "C"]), ("O23", "D∨C∨AB", ["D", "C", "AB"]),
    ("O24", "CD∨ABD", ["CD", "ABD"]), ("O25", "CD∨BD", ["CD", "BD"]), ("O26", "CD∨BD∨ABC", ["CD", "BD", "ABC"]),
    ("O27", "CD∨BC∨AD", ["CD", "BC", "AD"]), ("O28", "CD∨BD∨BC∨AD", ["CD", "BD", "BC", "AD"]),
    ("O29", "D∨BC", ["D", "BC"]), ("O30", "D∨BC∨AC", ["D", "BC", "AC"]),
]
S4P = [signed_perm(pi, (0, 0, 0, 0), PTS, IDX, N) for pi in itertools.permutations(range(N))]
TS4 = [tables_for(p, 16) for p in S4P]


def is_monotone(f):
    return all(not ((f >> i) & 1 and not (f >> j) & 1 and all(a <= b for a, b in zip(PTS[i], PTS[j])))
               for i in range(16) for j in range(16))


allm = set()
orbit_ids = {}
ok = True
print("\n[D] 단조 30궤도 대표 검증")
exp_sizes = [1, 1, 1, 1, 1, 1, 3, 3] + [4] * 9 + [6] * 6 + [12] * 7
for (oid, label, terms), es in zip(REPS, exp_sizes):
    f = terms_to_f(terms)
    ob = orbit(f, TS4)
    key = min(ob)
    good = len(ob) == es and is_monotone(f) and key not in orbit_ids
    ok &= good
    orbit_ids[key] = oid
    allm |= ob
    if not good:
        print("    불일치:", oid, label, "크기", len(ob), "기대", es)
print("    30개 대표 모두 (단조, 기대 크기, 서로 다른 궤도):", ok, "/ 합집합 크기:", len(allm), "(168 이어야 함)")
assert ok and len(allm) == 168
wrong = terms_to_f(["A", "BC", "AC"])
print("    6 paper.md 의 O10 표기 'A∨B∧C∨A∧C' 의 궤도 크기:", len(orbit(wrong, TS4)), "(4 가 아니라 12)")

# ---------------------------------------------------------------- E. L ∩ M
affine = set()
for c in itertools.product([0, 1], repeat=5):
    affine.add(sum((c[0] ^ (c[1] & x[0]) ^ (c[2] & x[1]) ^ (c[3] & x[2]) ^ (c[4] & x[3])) << i for i, x in enumerate(PTS)))
mono_all = {f for f in range(1 << 16) if is_monotone(f)}
lm = affine & mono_all
lm_orbits = {min(orbit(f, TS4)) for f in lm}
print("\n[E] |L ∩ M| = %d, S4-궤도 %d개" % (len(lm), len(lm_orbits)))
assert len(lm) == 6 and len(lm_orbits) == 3 and len(mono_all) == 168

# ---------------------------------------------------------------- F. n=5
N5 = 5
PTS5 = list(itertools.product([0, 1], repeat=N5))
IDX5 = {x: i for i, x in enumerate(PTS5)}
S5 = [tables_for(signed_perm(pi, (0,) * 5, PTS5, IDX5, 5), 32) for pi in itertools.permutations(range(5))]
aff5 = set()
for c in itertools.product([0, 1], repeat=6):
    aff5.add(sum((c[0] ^ (sum(c[k + 1] & x[k] for k in range(5)) & 1)) << i for i, x in enumerate(PTS5)))
mono4 = sorted(mono_all)
mono5 = {f0 | (f1 << 16) for f0 in mono4 for f1 in mono4 if f0 & ~f1 == 0}


def count_orbits(space):
    space, seen, n = set(space), set(), 0
    for f in sorted(space):
        if f not in seen:
            n += 1
            seen |= {act(f, t) for t in S5}
    return n


print("\n[F] n=5: 아핀 %d개 -> S5-궤도 %d개, 단조 %d개 -> S5-궤도 %d개"
      % (len(aff5), count_orbits(aff5), len(mono5), count_orbits(mono5)))
assert len(aff5) == 64 and count_orbits(aff5) == 12 and len(mono5) == 7581 and count_orbits(mono5) == 210
print("\n전체: 통과")
