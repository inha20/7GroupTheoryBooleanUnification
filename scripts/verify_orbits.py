"""
verify_orbits.py
================
4변수 부울 함수 공간에 대한 S4(변수 순열) 작용의 궤도 수를
전수 열거와 Burnside 보조정리 두 방식으로 독립 검증한다.

검증 대상 (논문 7의 주장값):
    전체 공간 F4     : 65,536개 함수 -> 3,984 궤도
    Space(XOR) 아핀  :     32개 함수 ->    10 궤도
    Space(AND) 단조  :    168개 함수 ->    30 궤도
    Space(NOT) 자기쌍대:  256개 함수 ->    32 궤도

사용법:
    python scripts/verify_orbits.py

의존성: Python 3.8+, 표준 라이브러리만 사용. 불일치가 있으면 종료 코드 1.
"""
import itertools
import sys

N = 4
INPUTS = list(itertools.product([0, 1], repeat=N))
IDX = {x: i for i, x in enumerate(INPUTS)}
PERMS = list(itertools.permutations(range(N)))

EXPECTED = {"full": 3984, "affine": 10, "monotone": 30, "selfdual": 32}


def point_perm(p):
    return [IDX[tuple(x[p[i]] for i in range(N))] for x in INPUTS]


PP = [point_perm(p) for p in PERMS]


def act(f, pp):
    r = 0
    for i in range(16):
        if (f >> pp[i]) & 1:
            r |= 1 << i
    return r


def orbits_and_burnside(space):
    space = set(space)
    seen, orbs = set(), 0
    for f in sorted(space):
        if f in seen:
            continue
        orbs += 1
        seen.update(act(f, pp) for pp in PP)
    fix = sum(1 for pp in PP for f in space if act(f, pp) == f)
    assert fix % len(PP) == 0
    return orbs, fix // len(PP)


def tbl(fn):
    return sum(fn(x) << i for i, x in enumerate(INPUTS))


def is_monotone(f):
    return all(
        not (all(a <= b for a, b in zip(x, y)) and (f >> i) & 1 and not (f >> j) & 1)
        for i, x in enumerate(INPUTS)
        for j, y in enumerate(INPUTS)
    )


def is_self_dual(f):
    return all(
        ((f >> i) & 1) != ((f >> IDX[tuple(1 - v for v in x)]) & 1)
        for i, x in enumerate(INPUTS)
    )


def main():
    full = range(1 << 16)
    affine = {
        tbl(lambda x, c=c: c[0] ^ (c[1] & x[0]) ^ (c[2] & x[1]) ^ (c[3] & x[2]) ^ (c[4] & x[3]))
        for c in itertools.product([0, 1], repeat=5)
    }
    monotone = {f for f in full if is_monotone(f)}
    selfdual = {f for f in full if is_self_dual(f)}

    ok = True
    for name, sp in [("full", full), ("affine", affine), ("monotone", monotone), ("selfdual", selfdual)]:
        sp = list(sp)
        enum, burn = orbits_and_burnside(sp)
        good = enum == burn == EXPECTED[name]
        ok = ok and good
        print(f"{name:<9} 함수 {len(sp):>6}  열거 {enum:>5}  Burnside {burn:>5}  기대 {EXPECTED[name]:>5}  {'OK' if good else 'MISMATCH'}")

    print("\n켤레류 대표원별 Fix (전체 공간):")
    for p, pp in zip(PERMS, PP):
        if p in [(0, 1, 2, 3), (1, 0, 2, 3), (1, 0, 3, 2), (1, 2, 0, 3), (1, 2, 3, 0)]:
            print(f"  {p}  Fix = {sum(1 for f in range(1 << 16) if act(f, pp) == f)}")

    print("\n전체:", "통과" if ok else "실패")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
