"""
images/ 의 그림이 논문 7의 캡션이 말하는 함수·배치·축 순서와 일치하는지 대조한다 (표준 라이브러리만 사용).

그림은 Word 문서에서 캡처한 PNG 이다. 격자의 0/1 값을 눈으로 옮겨 적은 상수(아래 GRIDS)를
7의 정의로 직접 만든 카르노맵 그림과 비교한다. 옮겨 적은 값이 계산과 같으면 캡션이 그림을 정확히 설명한다.
"""
import itertools

GRAY = [(0, 0), (0, 1), (1, 1), (1, 0)]
BINARY = [(0, 0), (0, 1), (1, 0), (1, 1)]
VARS = "ABCD"


def minterm(assign):
    """assign: {'A':0/1,...} -> 인덱스 (A 가 최상위 비트)"""
    return assign["A"] * 8 + assign["B"] * 4 + assign["C"] * 2 + assign["D"]


def picture(on, rows, cols, order=GRAY):
    """on: 1 인 민텀 집합. rows=(X,Y), cols=(Z,W). 반환: 4x4 튜플"""
    g = []
    for i in range(4):
        row = []
        for j in range(4):
            a = dict(zip(rows, order[i]))
            a.update(dict(zip(cols, order[j])))
            row.append(1 if minterm(a) in on else 0)
        g.append(tuple(row))
    return tuple(g)


# ---------------------------------------------------------------- 격자 대칭군 W (위치 인덱스 위의 D4(Z4) wr Z2)
def w_maps():
    maps = []
    for sr, a in itertools.product((1, -1), range(4)):
        for sc, b in itertools.product((1, -1), range(4)):
            for tr in (False, True):
                maps.append((sr, a, sc, b, tr))
    return maps


def apply_w(grid, m):
    sr, a, sc, b, tr = m
    out = [[0] * 4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            r2, c2 = (sr * r + a) % 4, (sc * c + b) % 4
            if tr:
                r2, c2 = c2, r2
            out[r2][c2] = grid[r][c]
    return tuple(tuple(x) for x in out)


W = w_maps()
assert len(W) == 128


def w_equivalent(g1, g2):
    return any(apply_w(g1, m) == g2 for m in W)


def stab_w(grid):
    return sum(1 for m in W if apply_w(grid, m) == grid)


def classes(grids):
    reps = []
    for g in grids:
        if not any(w_equivalent(g, r) for r in reps):
            reps.append(g)
    return len(reps)


def S(*rows):
    return tuple(tuple(r) for r in rows)


# ---------------------------------------------------------------- 그림에서 옮겨 적은 격자 (행/열 모두 위에서 아래, 왼쪽에서 오른쪽)
GRIDS = {
    # 파일: (격자, 설명)
    "fig01_kmap_exactly0": S((1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)),
    "fig07_xorplane_ab_cd": S((0, 0, 0, 0), (0, 1, 0, 1), (0, 0, 0, 0), (0, 1, 0, 1)),
    "fig08_xorplane_ac_bd": S((0, 0, 1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0)),
    "fig09_xorplane_ad_bc": S((0, 0, 1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0)),
    "fig10_xnorplane_ab_cd": S((1, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0)),
    "fig11_xnorplane_ac_bd": S((1, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0)),
    "fig12_xnorplane_ad_bc": S((1, 0, 1, 0), (0, 0, 0, 0), (1, 0, 1, 0), (0, 0, 0, 0)),
    "fig13_parity_xor_gray": S((0, 1, 0, 1), (1, 0, 1, 0), (0, 1, 0, 1), (1, 0, 1, 0)),
    "fig14_parity_xor_binary": S((0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 0, 1), (0, 1, 1, 0)),
    "fig15_parity_xnor_gray": S((1, 0, 1, 0), (0, 1, 0, 1), (1, 0, 1, 0), (0, 1, 0, 1)),
    "fig16_parity_xnor_binary": S((1, 0, 0, 1), (0, 1, 1, 0), (0, 1, 1, 0), (1, 0, 0, 1)),
    "fig17_layers": S((1, 2, 3, 2), (2, 3, 4, 3), (3, 4, 5, 4), (2, 3, 4, 3)),   # 라벨 L1..L5 = 해밍 무게 0..4
    "fig18_exactly1": S((0, 1, 0, 1), (1, 0, 0, 0), (0, 0, 0, 0), (1, 0, 0, 0)),
    "fig19_exactly2": S((0, 0, 1, 0), (0, 1, 0, 1), (1, 0, 0, 0), (0, 1, 0, 1)),
    "fig20_exactly3": S((0, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, 1), (0, 0, 1, 0)),
    "fig21_exactly4": S((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 0)),
}

ok_all = True


def check(name, cond, note=""):
    global ok_all
    print("  [%s] %s %s" % ("OK " if cond else "불일치", name, note))
    ok_all = ok_all and cond


weight = lambda m: bin(m).count("1")

print("[1] 완전 대칭 함수 그림 (Exactly-k): 계산과 같고, 24개 배치에서 모두 같은가 (명제 1)")
for name, k in (("fig01_kmap_exactly0", 0), ("fig18_exactly1", 1), ("fig19_exactly2", 2),
                ("fig20_exactly3", 3), ("fig21_exactly4", 4)):
    on = {m for m in range(16) if weight(m) == k}
    pics = {picture(on, p[:2], p[2:]) for p in itertools.permutations(VARS)}
    check(name, len(pics) == 1 and GRIDS[name] in pics, "(Exactly-%d, 배치 24개에서 그림 %d종)" % (k, len(pics)))

print("[2] 레이어 그림: 칸의 라벨 L(k+1) = 해밍 무게 k")
exp =tuple(tuple(weight(minterm({**dict(zip("AB", GRAY[i])), **dict(zip("CD", GRAY[j]))})) + 1 for j in range(4))
            for i in range(4))
check("fig17_layers", exp == GRIDS["fig17_layers"], "(그림의 L1..L5 = 무게 0..4, 논문 7의 $L_0..L_4$ 보다 지수가 1 크다)")

print("[3] 패리티 그림 (명제 2): 축 순서 Gray / 이진 x XOR / XNOR")
xor = {m for m in range(16) if weight(m) % 2 == 1}
xnor = set(range(16)) - xor
check("fig13_parity_xor_gray", picture(xor, "AB", "CD", GRAY) == GRIDS["fig13_parity_xor_gray"], "(체커보드)")
check("fig14_parity_xor_binary", picture(xor, "AB", "CD", BINARY) == GRIDS["fig14_parity_xor_binary"], "(0110/1001/1001/0110)")
check("fig15_parity_xnor_gray", picture(xnor, "AB", "CD", GRAY) == GRIDS["fig15_parity_xnor_gray"])
check("fig16_parity_xnor_binary", picture(xnor, "AB", "CD", BINARY) == GRIDS["fig16_parity_xnor_binary"])
# 그림 파일 09, 11 에 붙어 있던 옛 캡션은 '09 = XOR 이중대각, 11 = XNOR 이중대각' 이었다. 그림 자체와 비교해 라벨이 뒤바뀐 것을 확인한다.
check("옛 캡션이 'XOR 이중대각'이라 한 그림 09 는 XNOR 의 이진 축 그림이다",
      GRIDS["fig16_parity_xnor_binary"] == picture(xnor, "AB", "CD", BINARY))
check("옛 캡션이 'XNOR 이중대각'이라 한 그림 11 은 XOR 의 이진 축 그림이다",
      GRIDS["fig14_parity_xor_binary"] == picture(xor, "AB", "CD", BINARY))

print("[4] 정리 4 의 예: XOR 평면 f = m(5,6,9,10) 와 XNOR 평면 f = m(0,6,9,15), 세 대표 배치")
XORP, XNORP = {5, 6, 9, 10}, {0, 6, 9, 15}
for tag, on, names in (("xorplane", XORP, ("fig07_xorplane_ab_cd", "fig08_xorplane_ac_bd", "fig09_xorplane_ad_bc")),
                       ("xnorplane", XNORP, ("fig10_xnorplane_ab_cd", "fig11_xnorplane_ac_bd", "fig12_xnorplane_ad_bc"))):
    pics = []
    for nm, (rows, cols) in zip(names, (("AB", "CD"), ("AC", "BD"), ("AD", "BC"))):
        g = picture(on, rows, cols)
        check(nm, g == GRIDS[nm], "(%s/%s)" % (rows, cols))
        pics.append(g)
    print("      %s: 세 대표 배치의 그림이 W 아래 서로 구별되는 종류 = %d" % (tag, classes(pics)))
    print("      %s: |Stab_W| (AB/CD 그림) = %d" % (tag, stab_w(pics[0])))
check("정리 4(1)의 예 m(5,6,9,10): |Stab_W| = 32", stab_w(picture(XORP, "AB", "CD")) == 32)

print("[5] 보조정리 1 의 설명 그림 (변수 쌍 맞교환): 라벨 01 과 10 이 맞바뀌고 위치 1, 3 의 줄이 서로 바뀐다")
pos = {lab: i for i, lab in enumerate(GRAY)}
perm = [pos[(b, a)] for (a, b) in GRAY]          # 위치 i 의 라벨 (a,b) 를 (b,a) 로 읽으면 위치가 perm[i]
check("라벨 (a,b) -> (b,a) 로 바뀌는 위치", perm == [0, 3, 2, 1], "(위치 0,2 는 고정, 1 <-> 3: 보조정리 1 의 i -> -i)")
check("Gray 표(fig03/fig04)의 'index' = 라벨의 이진수 값",
      [int("%d%d" % l, 2) for l in GRAY] == [0, 1, 3, 2] and [int("%d%d" % (b, a), 2) for (a, b) in GRAY] == [0, 2, 3, 1])

print("\n전체:", "통과" if ok_all else "불일치 있음")
assert ok_all
