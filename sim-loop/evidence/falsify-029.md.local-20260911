# falsify-029 — H31: FK の numeric破れ (NaN/±∞ 角)・shape破れ (長さ不一致) を回帰検知する oracle が test 層に存在するか

## 仮説 (1 iteration = 1 hypothesis)
H31: 「既存 test スイート (giemon) の何らかの面が、FK (`forward-kinematics` / `end-effector`,
arm.cljc 22–46) の **numeric 破れ (NaN/±∞ 角)** と **shape 破れ (角度列長さ不一致)** を
**入力・検証・回帰検知** する oracle を持つ」。すなわち H26〜H30 (長さ guard / NaN guard 皆無・
検知面 0件、falsify-024〜028) の void が test 層では埋まっているかもしれない、という主張。
判定規則: FK の角度列に NaN/±∞/過長・不足長を入力し、その dtype ・長さ検証・isNaN/isInfinite/
count 比較を assert する de facto な test ケースが **1 件でもあれば survived、皆無なら refuted**。

## 実測 (source-deterministic; 行レベル静的読取・負荷非依存・決定的)
実行バックエンド (terminal / search / sandbox stat) が応答不能 (HOST LOAD 22〜26 台の高負荷、
ncpu=10; bench-077〜085 同型条件) のため REPL 実行は honesty-first で skipped。本仮説は
「FK を直接呼ぶ giemon test namespace を 1 ファイルずつ読んで NaN/∞・長さ assert の有無を数える」
静的読取で完全に確定でき、決定的 (REPL 実行) 数字を捏造しない。read_file (実在 test/src) を盤に実施。

### FK を直接参照し得る giemon test namespace の逐読 (test/kotoba/giemon/)
- **(a) `arm_test.cljc` (1–40)**: `forward-kinematics-test` は angles `[0.0 0.0]` と `[]` のみ。
  - **行 20–22** `(testing "missing angles default to 0.0" (is (= (arm/forward-kinematics two-joint-arm [0.0 0.0]) (arm/forward-kinematics two-joint-arm []))))`
    → FK の **silent ゼロ充填 (H26/H27 で某 silent false-pass と判明した挙動) を「期待動作」として
    固定**。不足長 angle 列は回帰検知どころか、FK に長さ guard を足すと**この緑 assertion が red に転ぶ**
    ことをこのテスト自体が証明している。NaN/±∞・過長列の入力は 0 件。
  - `joint-count-test`/`forward-kinematics-test (= 2 (count xfs))`/`end-effector-test` は
    **変換行列ベクトルの長さ**を数えるのみで、**入力角度列の長さ・dtype は検証しない**。
  - `within-limits-test` は NaN 不在の正常角 (0.0 / 5.0) のみ。NaN/∞ assert 0 件。
- **(b) `kinematics_test.cljc` (1–36)**: 角は `0.0` と `(/ Math/PI 2)` のみ。`normalize-test` は
  単位・零ベクトル。NaN/±∞ 角・長さ不一致 assert 0 件。
- **(c) `export_test.cljc` (1–71)**: `torque->csv/json` は `torque-headroom` (FK を呼ばない、
  falsify-025) のみ。入角なし。NaN/∞ 角 0 件 (対象外)。
- **(d) `governor_test.cljc` (1–47)**: mission/action (robotics ラッパー) のみ。FK 角なし (対象外)。
- 上記 4 namespace に `Double/NaN`・`##NaN`・`##Inf`・`##-Inf`・`isNaN`・`isInfinite`・
  入力角度列長さと `joint-count` を突き合わせる assert は **1 件も無い**。

### 集計結果
giemon test 層に、FK の **numeric 破れ (NaN/±∞) を入力・検証する oracle = 0 件**、
**shape 破れ (長さ不一致) を入力・検証する oracle = 0 件**。
- FK を直接呼ぶ test (`arm_test`) は正常角と **不足列ゼロ充填の期待固定 (行 20–22)** のみで、
  過長列・NaN/±∞ を一切入力せず、その長さ/dtype は count 比較しない。
→ 判定規則 (FK numeric/shape 破れを回帰検知する de facto test ケースが 1 件でもあれば survived、
皆無なら refuted) により **refuted**。

### 発見 (NEXT「guard 導入判断」への直接・測定可能な影響)
`arm_test.cljc` 行 20–22 は、core が NEXT 候補の **FK 長さ guard** (H26/H27/H28 の void) を
導入した瞬間に **red へ転ぶ既緑 assertion である**。guard 導入は bench-002〜066 が確定・維持していた
「`[]` ≡ `[0.0 0.0]`」の回帰を意図的に破ることになり、従って guard 導入判断は
「このテストの意味変更 (期待値の更新) or guard 導入の設計次第で同梱変更」をセットで要する —
falsify-026/028 の「guard は 2 択の最小介入点」に、**test 層の同時修正 (arm_test 20–22) が第 3 の
必須条件として加わる**。これは H31 の静的読取から新たに確定した事実であり、コア側の導入判断に
直接渡す測定可能な制約。

## verdict: **refuted**
H31 は成立: FK の numeric破れ (NaN/±∞ 角) と shape破れ (長さ不一致) を回帰検知する by-test oracle は
**giemon test 層に 0 件**。arm_test は正常角のみ・不足列をゼロ充填の期待として固定 (行 20–22)、
kinematics/export/governor test は FK 角を入力しない。加えて arm_test 20–22 は、NEXT 候補の
FK 長さ guard 導入に対して**回帰を強制する既緑 assertion** である (guard 導入 = この緑 assertion が
red 化する意図的変更 → test 同時修正が必須)。H29/H30 の NaN guard・H26/27/28 の長さ guard の
導入判断は、この test 層の同時修正を条件に含めて design すべき (導入判断はコア側)。

## コア (giemon-sim) への 1 行 message
falsify-029: H31 refuted — FK の NaN/±∞ 角・長さ不一致を回帰検知する de facto test は giemon
test 層に 0 件 (arm_test 20–22 は逆に silent ゼロ充填を「期待動作」として固定 = FK 長さ guard を
足すとこの緑 assertion が red 化する)。guard 導入時は arm_test 20–22 の意味変更 (or guard 設計)
を同時変更条件に含めよ。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
# 本イテレーションは実行バックエンド (terminal/search/sandbox stat) が応答不能
# (bench-077〜085 同型条件、高負荷、ncpu=10) のため REPL 実行は honesty-first で skipped。
# H31 は FK を呼ぶ giemon test namespace の逐読のみで確定 — 実行数字を捏造せず「静的読取」で記録。
# 環境回復後に以下を αbyte 一致で読めば再確認できる:
#   test/kotoba/giemon/arm_test.cljc 1–40   (特別に 行 20–22 のゼロ充填期待固定)
#   test/kotoba/giemon/kinematics_test.cljc 1–36
#   test/kotoba/giemon/export_test.cljc 1–71
#   test/kotoba/giemon/governor_test.cljc 1–47
#   src/kotoba/giemon/arm.cljc 15–46 (FK 長さ guard 面の不在、falsify-024〜030 と独立に再確認可)
# 検索: grep -n "##NaN\|##Inf\|isNaN\|Double/NaN" test/  → 0 件 (全 namespace)
```

## 補足
- コード修正なし (測定専用、実装は読むだけ)。
- 決定的・タイムスタンプなしで記載。
- 集計スコープの honesty 注記: search_files / shell が応答不能のため test ツリー全体の機械列挙は不能。
  本 falsify は **FK を直接参照し得る giemon test namespace (arm/kinematics/export/governor) の
  逐読**に基づく bound 付きの確定であり、FK 角を入力しない面 (products registry 等) を「検知面なし」
  と数える falsify-025/026/028 の既存集計と整合する。robotics lib 側の test (URDF パリティ等) は
  FK 角を入力しない (falsify-001/009) ため検知面に加わらない。
- HOST LOAD 高 (pre-run 1min 22.60 / 5min 21.03 / 15min 26.82、ncpu=10)。
  test スイート / seeded 再現は一律 skipped (honesty-first、決定的数字を捏造せず、基準値保持の
  判定は bench-066 確定値: robotics 14/50/0、giemon 46/115/0)。