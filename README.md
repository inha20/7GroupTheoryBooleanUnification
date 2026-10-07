# 7GroupTheoryBooleanUnification

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-blue?style=flat-square&logo=github)](https://inha20.github.io/7GroupTheoryBooleanUnification/)
[![Field](https://img.shields.io/badge/Field-Group%20Theory%20%7C%20Boolean%20Algebra-purple?style=flat-square)](https://inha20.github.io/7GroupTheoryBooleanUnification/)
[![Track](https://img.shields.io/badge/Track-A%3A%20Mathematical%20Synthesis-success?style=flat-square)](https://inha20.github.io/7GroupTheoryBooleanUnification/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**논문 제목:** 카르노맵 위의 부울 함수 공간에 대한 군론적 통합 분류  
**Title:** A Group-Theoretic Unified Classification of Boolean Function Spaces on Karnaugh Maps  
**저자:** 최종훈 (Jonghun Choi) — 인하공업전문대학 졸업 · 독립 연구자  
**GitHub Pages:** [웹 논문 및 대화형 분석 포털 보기](https://inha20.github.io/7GroupTheoryBooleanUnification/)  

---

## 📌 Keywords
Karnaugh map, Boolean function space, Dihedral group $D_4$, Symmetric group $S_4$, Burnside's Lemma, Hamming weight layer, orbit classification, variable arrangement invariance, affine functions, Post's lattice, gate-generated spaces.

---

## 📖 Abstract (초록)

본 연구는 4변수 카르노맵을 기하학적 평면 격자로 모델링하고, 그 위의 부울 함수 공간 $\mathcal{F}_4$ ($|\mathcal{F}_4| = 2^{16} = 65,536$)을 **$D_4$ 이면체군** 및 **$S_4$ 대칭군**의 군론적 작용(Group Action)을 통해 단일한 수학적 프레임워크로 통합 분류한다.

선행 연구들(P1, P2, P3, P6)에서 개별적으로 다루어진:
1. 카르노맵 변수 배치의 $D_4$ 기하학적 불변성 ($24 \to 6 \to 3$ 독립 동치류 축약)
2. 대칭 부울 함수의 Hamming Weight 레이어 분할 구조 ($L_0 \sim L_4$)
3. 변수 재배열 $S_4$ 작용에 대한 번사이드 보조정리(Burnside's Lemma) 궤도 계산
4. 단일 기본 게이트(NAND, NOR, XOR 등)가 생성하는 부분함수 공간의 기하학적 분포

이들을 단일 대수 구조인 **$(S_4 \times D_4)$ 변환 작용 하의 궤도 분해(Orbit Decomposition)**로 포섭하여, 부울 함수 공간의 대칭성과 시각적 표현 사이의 필연적 연결 고리를 엄밀하게 증명한다.

---

## 🔬 핵심 수학적 정리 (Core Theorems)

### 1. 정리 1: 변수 배치 동치류 ($24 \to 6 \to 3$ 축약)
4변수 카르노맵의 가능한 $4! = 24$가지 변수 배치 $\sigma \in S_4$에 대하여, 카르노맵 평면의 기하학적 대칭군 $D_4$에 의한 합동 작용을 적용하면:
$$\text{배치 수 } 24 \xrightarrow{\text{행/열 반전}} 6 \xrightarrow{\text{전치(Transpose)}} 3$$
정확히 3개의 독립 동치류 대표원 $\{ (AB, CD), (AC, BD), (AD, BC) \}$만이 존재하며, XOR 및 XNOR 체커보드 패턴은 이 세 배치에서 각각 위상적으로 서로 다른 기하학적 형태로 발현된다.

### 2. 정리 2: 대칭 함수의 Hamming Layer 분할
모든 변수 순열 $\pi \in S_4$에 대해 불변인 대칭 부울 함수 $f \in \mathcal{S}_4$는 Hamming Weight $w(\mathbf{x}) \in \{0, 1, 2, 3, 4\}$에 의해서만 함수값이 결정된다:
$$|\mathcal{S}_4| = 2^{4+1} = 2^5 = 32$$
각 레이어의 카르노맵 셀 수는 이항계수 $\binom{4}{k} \in \{1, 4, 6, 4, 1\}$를 따르며, 카르노맵 상에서 동심(concentric) 및 교차 대칭 격자를 형성한다.

### 3. 정리 3: 변수 재배열 불변성과 Burnside 보조정리
$S_4$ 작용 하의 4변수 부울 함수 궤도(동치류) 개수 $N$은 번사이드 보조정리에 의해 엄밀하게 계산된다:
$$N = \frac{1}{|S_4|} \sum_{g \in S_4} |\text{Fix}(g)| = 4,016$$
즉, 변수 이름의 치환에 의해 본질적으로 같은 구조를 지닌 4변수 함수는 전체 65,536개 중 4,016개의 고유한 대칭 궤도로 축약된다.

### 4. 정리 4: 게이트 생성 공간의 계층 구조
임의의 기본 게이트 $G$에 의해 생성되는 폐포 공간 $\langle G \rangle$은 Post 격자(Post's Lattice)의 부분 대수를 형성하며, affine 함수, 단조 함수, 자가쌍대 함수의 궤도 크기와 카르노맵 대칭 밀도가 완벽히 대응함을 규명하였다.

---

## 📂 저장소 구조 (Repository Structure)

```
7GroupTheoryBooleanUnification/
├─ README.md                               ← 저장소 안내 및 학술 요약 (본 문서)
├─ index.html                              ← 대화형 시각화 및 웹 논문 포털 (KaTeX 지원)
├─ paper/
│  └─ GroupTheoryBooleanUnification.md     ← 완성된 통합 수학 학술 논문 전문
└─ images/                                 ← 수학 다이어그램 및 카르노맵 격자 구조도
```

---

## 🌐 상호 연결 연구 생태계 (Research Ecosystem)

| ID | 저장소 | 핵심 내용 |
|:---:|:---|:---|
| **P1** | [1KMapStructureInvariance](https://github.com/inha20/1KMapStructureInvariance) | 카르노맵 변수 배치 불변성과 체커보드 패턴 분석 |
| **P2** | [2SymmetricBooleanFunctionMinorThesis](https://github.com/inha20/2SymmetricBooleanFunctionMinorThesis) | 대칭 부울 함수의 Hamming Layer 구조 연구 |
| **P3** | [3VariableRearrangementInvarianceMinorThesis](https://github.com/inha20/3VariableRearrangementInvarianceMinorThesis) | $S_4$ 변수 재배열 불변성과 궤도 분석 |
| **P6** | [6BooleanFunctionSpaceTheory](https://github.com/inha20/6BooleanFunctionSpaceTheory) | 게이트 생성 공간 및 Post 격자 기하학 |
| **P7** | **7GroupTheoryBooleanUnification (본 저장소)** | **P1+P2+P3+P6 군론적 통합 수학 논문** |
| **P8** | [8StructuralThinkingInAIEra](https://github.com/inha20/8StructuralThinkingInAIEra) | 생성형 AI 시대 구조적 사고와 인간-AI 연구 협력 |
| **Hub** | [Research-Portfolio](https://github.com/inha20/Research-Portfolio) | 전체 연구 프로그램 통합 포털 |

---

## 📜 인용 정보 (Citation)

```bibtex
@article{choi2026grouptheory,
  author    = {Choi, Jonghun},
  title     = {A Group-Theoretic Unified Classification of Boolean Function Spaces on Karnaugh Maps},
  journal   = {Independent Mathematics Research Program Preprint},
  year      = {2026},
  url       = {https://github.com/inha20/7GroupTheoryBooleanUnification}
}
```

---
© 2026 Jonghun Choi (최종훈). Released under the MIT License.
