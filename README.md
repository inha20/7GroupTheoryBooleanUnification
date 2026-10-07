# 7GroupTheoryBooleanUnification

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-blue?style=flat-square&logo=github)](https://inha20.github.io/7GroupTheoryBooleanUnification/)
[![Field](https://img.shields.io/badge/Field-Group%20Theory%20%7C%20Boolean%20Algebra-purple?style=flat-square)](https://inha20.github.io/7GroupTheoryBooleanUnification/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**논문 제목:** 카르노맵 위의 4변수 부울 함수 공간의 군론적 분류  
**Title:** Group-Theoretic Classification of 4-Variable Boolean Function Spaces on Karnaugh Maps  
**저자:** 최종훈 (Jonghun Choi) — 인하공업전문대학 졸업 · 독립 연구자  
**GitHub Pages:** [웹 논문 및 대화형 분석 포털 보기](https://inha20.github.io/7GroupTheoryBooleanUnification/)  

> 이 저장소의 논문은 자기완결적입니다. 같은 저자의 다른 저장소를 읽지 않아도 모든 정의와 증명을 본문에서 따라갈 수 있습니다. 필요한 배경은 군과 Burnside 보조정리의 기초뿐입니다.

---

## 📌 Keywords
Karnaugh map, Boolean function space, variable arrangement equivalence, symmetric group $S_4$, signed permutation group (hyperoctahedral group) $B_4$, Burnside's Lemma, Hamming weight layer, orbit classification, affine / monotone / self-dual functions, Post's lattice.

---

## 📖 Abstract (초록)

4변수 부울 함수 공간 $\mathcal{F}_4$ ($2^{16} = 65{,}536$개)에는 변수 순열군 $S_4$, 입력 반전군 $\mathbb{Z}_2^4$, 카르노맵 평면의 격자 대칭이 작용한다. 본 논문은 이 대칭들의 관계를 정리하고 궤도(동치류)를 모두 계산한다.

---

## 🔬 핵심 결과 (Main Results)

| # | 결과 |
|:---:|:---|
| 1 | 4변수 카르노맵의 변수 배치 $4! = 24$가지는 토러스 대칭군 $W$ (위수 128) 아래 **정확히 3개**의 동치류 $\{AB\|CD\}, \{AC\|BD\}, \{AD\|BC\}$로 나뉜다. $W$는 입력 반전과 변수 순열이 이루는 군 $B_4 = \mathbb{Z}_2^4 \rtimes S_4$ (위수 384)에서 변수 쌍 분할 하나의 안정화군이며 지표가 3이다. 격자의 회전·반사 8개만으로는 12개이다. |
| 2 | **정정:** 완전 대칭 함수(XOR, 다수결 등 32개)의 카르노맵 그림은 24개 배치 모두에서 같다. 배치에 따라 그림이 달라지는 것은 비대칭 함수이며, 65,536개 중 26,112개가 세 동치류에서 서로 다른 그림이 된다. |
| 3 | $S_4$ 아래의 궤도 수: 전체 **3,984**, 아핀(32개) **10**, 단조(168개) **30**, 자기쌍대(256개) **32**. 모든 Burnside Fix 표를 본문에 제시한다. |
| 4 | $S_4$와 격자 대칭이 생성하는 군은 직접곱이 아니라 $B_4$ (위수 384)이다. 이 군 아래에서 전체 공간은 **402**, 아핀은 **6**, 자기쌍대는 **7**개의 궤도이다. 402는 문헌의 4변수 NP 동치류 수와 일치한다. |

---

## 📂 저장소 구조 (Repository Structure)

```
7GroupTheoryBooleanUnification/
├─ README.md                               ← 저장소 안내 (본 문서)
├─ index.html                              ← 대화형 웹 논문 포털 (KaTeX)
├─ paper/
│  └─ GroupTheoryBooleanUnification.md     ← 논문 전문
└─ scripts/                                ← 본문 수치를 검증하는 Python 스크립트 (표준 라이브러리만 사용)
   ├─ verify_orbits.py                     ← S4 궤도 수 (열거 + Burnside)
   ├─ verify_tables.py                     ← Fix 표, 궤도 크기 분포, 안정화군 위수, 그림 비교
   ├─ verify_double_action.py              ← S4와 격자 대칭의 합성군 크기·궤도 수
   ├─ verify_b4_table.py                   ← B4 켤레류 표와 전수 열거 대조
   ├─ verify_pictures.py                   ← 세 배치의 카르노맵 그림 전수 비교
   └─ verify_extras.py                     ← 패리티 체커보드, 단조 30궤도 목록, B4-궤도의 W-분할, L∩M, n=5 예비 결과
```

각 스크립트는 `python scripts/<이름>.py`로 실행한다.

---

## 🌐 관련 저장소 (선택 사항, 읽지 않아도 됨)

이 논문은 저자의 **초기 연구 노트**(저장소 1~6)에서 출발했지만 그 내용을 전제로 하지 않으며, 읽지 않아도 됩니다.

| 저장소 | 내용 |
|:---|:---|
| [Research-Portfolio](https://github.com/inha20/Research-Portfolio) | 전체 연구 프로그램 포털 |
| [8StructuralThinkingInAIEra](https://github.com/inha20/8StructuralThinkingInAIEra) | 구조적 사고와 인간-AI 연구 협력 (별도 주제) |

---

## 📜 인용 정보 (Citation)

```bibtex
@article{choi2026grouptheory,
  author    = {Choi, Jonghun},
  title     = {Group-Theoretic Classification of 4-Variable Boolean Function Spaces on Karnaugh Maps},
  journal   = {Independent Mathematics Research Program Preprint},
  year      = {2026},
  url       = {https://github.com/inha20/7GroupTheoryBooleanUnification}
}
```

---
© 2026 Jonghun Choi (최종훈). Released under the MIT License.
