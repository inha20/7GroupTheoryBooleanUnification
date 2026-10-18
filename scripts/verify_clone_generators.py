"""5.3절: 세 클론의 생성 연산을 4변수 함수 위에서 직접 닫아 확인한다.

사영 함수 4개에서 출발하여 생성 연산을 반복 적용해 얻는 4변수 함수의 집합(클론의 4항 부분)을 계산한다.
  - 아핀 함수 L: XOR(2항)과 상수 1  -> 32개
  - 단조 함수 M: AND, OR와 상수 0, 1 -> 168개
  - 자기쌍대 함수 D: NOT과 3입력 다수결 MAJ3 -> 256개
또한 연산 하나만으로 얻는 함수의 수를 확인한다 (AND만 + 상수: 17개, NOT만 + 상수: 10개).
함수는 16비트 정수(진리표)로 표현한다. 표준 라이브러리만 사용한다.

실행: python verify_clone_generators.py
"""
import itertools

N = 4
POINTS = list(itertools.product((0, 1), repeat=N))
INDEX = {p: i for i, p in enumerate(POINTS)}
FULL = (1 << 16) - 1


def table(fn):
    return sum(fn(p) << i for i, p in enumerate(POINTS))


PROJ = [table(lambda p, k=k: p[k]) for k in range(N)]
ZERO, ONE = 0, FULL


def NOT(a):
    return FULL ^ a


def AND(a, b):
    return a & b


def OR(a, b):
    return a | b


def XOR(a, b):
    return a ^ b


def MAJ3(a, b, c):
    return (a & b) | (a & c) | (b & c)


def closure(start, unary=(), binary=(), ternary=()):
    """start에서 출발하여 주어진 연산으로 닫은 함수 집합."""
    s = set(start)
    while True:
        cur = list(s)
        new = set(s)
        for f in unary:
            for a in cur:
                new.add(f(a))
        for f in binary:
            for a in cur:
                for b in cur:
                    new.add(f(a, b))
        for f in ternary:
            for a in cur:
                for b in cur:
                    for c in cur:
                        new.add(f(a, b, c))
        if new == s:
            return s
        s = new


def is_self_dual(f):
    for i, p in enumerate(POINTS):
        q = tuple(1 - v for v in p)
        if ((f >> INDEX[q]) & 1) == ((f >> i) & 1):
            return False
    return True


def is_monotone(f):
    for i, p in enumerate(POINTS):
        if (f >> i) & 1:
            for j, q in enumerate(POINTS):
                if all(a <= b for a, b in zip(p, q)) and not (f >> j) & 1:
                    return False
    return True


def is_affine(f):
    """f = c0 xor (c . x) 꼴인지: 계수를 진리표에서 읽어 같은 함수를 다시 만들어 본다."""
    c0 = f & 1
    coef = [((f >> INDEX[tuple(1 if k == j else 0 for k in range(N))]) & 1) ^ c0 for j in range(N)]
    g = table(lambda p: c0 ^ (sum(c * x for c, x in zip(coef, p)) & 1))
    return g == f


def main():
    ok = True

    L = closure(PROJ + [ONE], binary=(XOR,))
    want = {f for f in range(1 << 16) if is_affine(f)}
    print('아핀: XOR + 상수 1 의 닫힘 = %d개, 아핀 함수 = %d개, 일치 = %s' % (len(L), len(want), L == want))
    ok &= L == want and len(L) == 32

    M = closure(PROJ + [ZERO, ONE], binary=(AND, OR))
    want = {f for f in range(1 << 16) if is_monotone(f)}
    print('단조: AND, OR + 상수 0, 1 의 닫힘 = %d개, 단조 함수 = %d개, 일치 = %s' % (len(M), len(want), M == want))
    ok &= M == want and len(M) == 168

    D = closure(PROJ, unary=(NOT,), ternary=(MAJ3,))
    want = {f for f in range(1 << 16) if is_self_dual(f)}
    print('자기쌍대: NOT, MAJ3 의 닫힘 = %d개, 자기쌍대 함수 = %d개, 일치 = %s' % (len(D), len(want), D == want))
    ok &= D == want and len(D) == 256

    a = closure(PROJ + [ZERO, ONE], binary=(AND,))
    n = closure(PROJ + [ZERO, ONE], unary=(NOT,))
    print('AND만(상수 포함): %d개, NOT만(상수 포함): %d개' % (len(a), len(n)))
    ok &= len(a) == 17 and len(n) == 10

    print('전체: %s' % ('통과' if ok else '실패'))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
