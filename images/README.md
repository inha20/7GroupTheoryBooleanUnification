# images/ — 그림 출처와 검증

이 폴더의 그림 21장은 저자의 이전 연구 저장소 세 곳(아래 표의 저장소 번호 1~3)의 `images/`에서 가져온 것이다. 논문은 그 저장소를 읽지 않아도 이해되도록 쓰였고, 그림은 본문의 설명을 보조할 뿐이다. 저장소 번호 1, 2, 3은 각각 `inha20/1KMapStructureInvariance`, `inha20/2SymmetricBooleanFunctionMinorThesis`, `inha20/3VariableRearrangementInvarianceMinorThesis`이다. 아래의 "구 1~3"도 이 저장소들을 뜻한다.

- 파일은 원본과 **바이트 단위로 동일**하다(아래 MD5). 원본은 수정하지 않았고, 설명은 이 논문의 캡션에서 새로 썼다.
- 각 그림의 0/1 값과 라벨은 `scripts/verify_figures.py`가 논문의 정의로 직접 만든 카르노맵 그림과 대조한다 (통과).
- 파일 이름은 GitHub Pages(대소문자 구분)를 위해 소문자 ASCII로 바꿨다.

## 사용한 그림

| 파일 | 논문 위치 | 내용 | 원본(저장소 번호 / 파일) | MD5 |
|:---|:---|:---|:---|:---|
| `fig01_kmap_exactly0.png` | 2.2절 그림 2, 4.3절 | 표준 배치 $AB/CD$의 카르노맵, 민텀 0만 1 ($E_0$) | 2 / `03.png` (1·3에도 동일 파일) | `10a5cb5e5387bcec5a5b7a90002b8c22` |
| `fig02_gray_cycle.png` | 2.2절 그림 1 | Gray 순서 $00 \to 01 \to 11 \to 10 \to 00$의 순환 | 2 / `01.png` | `743b0ae2e95ec909922de4b2e2fb6556` |
| `fig03_swap_xy_index_table.png` | 3.2절 그림 3 | $XY$와 $YX$ 라벨 대응표 | 1 / `greycode_index_conversion_xy_to_yx.png` | `d5ba78b0b042a49c8d3538c82bd5f328` |
| `fig04_swap_zw_index_table.png` | 3.2절 그림 4 | $ZW$와 $WZ$ 라벨 대응표 | 1 / `greycode_index_conversion_zw_to_wz.png` | `1fd64ac0f8b79da72037f28c38df6fb2` |
| `fig05_swap_row_variables.png` | 3.2절 그림 3 | 행 변수 맞교환: 위치 1, 3의 행이 바뀜 | 1 / `row_variable_swap_kmap_comparison.png` | `a106ec603b3b107d46506f86b5fd4caf` |
| `fig06_swap_col_variables.png` | 3.2절 그림 4 | 열 변수 맞교환: 위치 1, 3의 열이 바뀜 | 1 / `column_variable_swap_kmap_comparison.png` | `39ac4d7e9ffa89adaffd2b3ee78ab647` |
| `fig07_xorplane_ab_cd.png` | 6.5절 그림 8 | $f = m(5,6,9,10)$, 배치 $AB/CD$ | 1 / `ABCDXOR.png` | `9f31bcb2df119a156aa24224a7def48f` |
| `fig08_xorplane_ac_bd.png` | 6.5절 그림 8 | 같은 $f$, 배치 $AC/BD$ | 1 / `ACBDXOR.png` | `5e79579000c0610e8b5194d2389c5cc7` |
| `fig09_xorplane_ad_bc.png` | 6.5절 그림 8 | 같은 $f$, 배치 $AD/BC$ | 1 / `ADBCXOR.png` | `f7be2ab02f3d68c197390f6f875f8e01` |
| `fig10_xnorplane_ab_cd.png` | 6.5절 그림 9 | $f = m(0,6,9,15)$, 배치 $AB/CD$ | 1 / `ABCDXNOR.png` | `3ba03188e8d517434849ae85ef6c7d08` |
| `fig11_xnorplane_ac_bd.png` | 6.5절 그림 9 | 같은 $f$, 배치 $AC/BD$ | 1 / `ACBDXNOR.png` | `d368cd523cb7d59240f1024ff1d20579` |
| `fig12_xnorplane_ad_bc.png` | 6.5절 그림 9 | 같은 $f$, 배치 $AD/BC$ | 1 / `ADBCXNOR.png` | `917925e5b24018c81358dea1bfcdf8bf` |
| `fig13_parity_xor_gray.png` | 3.5절 그림 5 | XOR, Gray 축 순서(체커보드) | 2 / `08.png` | `0bd7dc33e412f25ed4ab38108969ed31` |
| `fig14_parity_xor_binary.png` | 3.5절 그림 5 | XOR, 이진 축 순서(이중대각) | 2 / `11.png` | `0e8725af18b9dbc1fe76cb4a48562f66` |
| `fig15_parity_xnor_gray.png` | 3.5절 그림 5 | XNOR, Gray 축 순서 | 2 / `10.png` | `1750c6522893be7972283b0a698f1a11` |
| `fig16_parity_xnor_binary.png` | 3.5절 그림 5 | XNOR, 이진 축 순서 | 2 / `09.png` | `7d2036a01d3571f513a5e946a6fdcfa2` |
| `fig17_layers.png` | 4.2절 그림 6 | 칸별 레이어(라벨 $L1 \dots L5$) | 2 / `02.png` | `ad963d38e9702b395c85a2777c61eb1e` |
| `fig18_exactly1.png` | 4.3절 그림 7 | $E_1$ (Exactly-1) | 2 / `04.png` (3에도 동일) | `f759b33816915aea2cc7bc91024af64b` |
| `fig19_exactly2.png` | 4.3절 그림 7 | $E_2$ (Exactly-2) | 2 / `05.png` | `d1ec8b4d1e5fbd26a679b90db7a70a50` |
| `fig20_exactly3.png` | 4.3절 그림 7 | $E_3$ (Exactly-3) | 2 / `06.png` | `6a270ff05a5fde9da58dd81e3fca2938` |
| `fig21_exactly4.png` | 4.3절 그림 7 | $E_4$ (Exactly-4) | 2 / `07.png` | `4db366f1ce482b1cff060b4343e46aab` |

## 원본의 캡션과 달라진 점 (계산으로 확인)

- **XOR / XNOR의 이진 축 그림이 서로 바뀌어 있었다.** 구 2의 `09.png`는 "XOR의 이중대각 패턴"이라고 적혀 있었으나 그림은 `1001/0110/0110/1001`, 곧 XNOR이다. `11.png`는 반대로 XOR(`0110/1001/1001/0110`)이다. 위 표는 그림의 실제 내용으로 이름을 붙였다.
- **레이어 라벨의 지수.** 구 2의 `02.png`는 $L1 \dots L5$로 적었고, 이 논문은 $L_0 \dots L_4$(해밍 무게)를 쓴다. 한 칸 어긋나므로 캡션에서 밝혔다.
- **"재배열에 따른 변화" 서술.** 구 3은 `figure05`, `07`, `12`, `13`의 이진 축 그림을 "변수 재배열 후 패턴의 변화"로 설명했으나, 이는 변수 배치가 아니라 축 라벨 순서의 차이이다(이 논문의 명제 2). 이 그림들은 같은 파일로 `fig13`~`fig16`에 들어 있고 설명은 새로 썼다.
- 구 1의 `ABCDXOR` 등 6장은 이 논문의 정리 4 예시 $f = m(5,6,9,10)$와 $m(0,6,9,15)$의 세 대표 배치 그림이다.

## 쓰지 않은 그림

| 원본 | 이유 |
|:---|:---|
| 구 1 `aa.png` | 시험용 그림("테스트 문구") |
| 구 1 `dihedral_group_d4_symmetry_operations.png` | 라벨 상자가 비어 있는 미완성 그림 |
| 구 3 `figure03-2_…png` 계열(`figure15-1`, `figure18-2` 포함) | 위쪽에 검은 막대가 있다 |
| 구 2 `12.png`, `13.png` | 이 프로젝트 고유 용어(0132 배열 등)를 쓰는 순서도 |
| 구 1 `kmap_equivalence_transformation_generators.png` | 한글 순서도, 본문이 증명을 직접 싣는다 |
| 구 1 `alphabet_array_diagonal_symmetry.png`, `greycode_array_diagonal_symmetry.png`, `coordinate_transformation_rows_column_swap.png`, `xor/xnor_plane_checkerboard_example_1_and_2.png` | 선택 사항. 위 그림들과 내용이 겹친다 |
| 구 1 `kmap_variable_arrangement_equivalence_class.png`(구 3의 `figure02`, `16`, `17`과 동일) | 3.4절의 표와 같은 내용이다 |
| 구 3 `figure03-3_…png`(`figure15-2`, `figure18-3`과 동일) | 선택 사항. 두 배치의 비교 예시이며 6.5절의 그림 8, 9와 내용이 겹친다 |
| 구 3의 나머지 파일 | 위에서 쓴 파일들과 내용이 같은 복사본(같은 MD5) |
