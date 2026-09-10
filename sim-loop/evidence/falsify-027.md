# falsify-027 — H29: 角度列の NaN / ±Infinity（数値破れ）を FK に渡すと、例外なしで silent に NaN pose 化されるか

## 仮説 (1 iteration = 1 hypothesis)
H29: 「角度列に長さ不一致 (H26/H27/H28) とは別次元の**数値破れ** — NaN / ±Infinity 等の
非数値 — を渡したとき、FK (`forward-kinematics`) は H26/H27 の型混在 (string → CCE loud)
と異なり**例外なしで silent に pose 化してしまう**か」。すなわち
「FK/kinematics/end-effector 経路のどこかに数値検査があり NaN/±∞ 角を拒否・loud 化する」
という代替仮説は成立しない、という予測。

## 実測 (source-deterministic; 行レベル静的読取・負荷非依存・決定的)
バックエンド (terminal / search / sandbox stat) が応答不能 (HOST LOAD 29.90 / 45.61 / 70.65、
ncpu=10; bench-069〜082 同型条件) のため REPL 実行は honesty-first で skipped — 本仮説は
NEXT が明示する通り IEEE-754 の決定的性質 + 行レベル静的読取のみで完全に確定できる
「NaN 検知面の有無」判定であり、決定的 (REPL 実行) 数字を捏造しない。

### 数値破れの伝播経路 (IEEE-754 決定的性質の適用)
- **(a) `normalize` (`kinematics.cljc` 22–27)**: `(zero? n)` の零ベクトル例外のみ。
  角度そのものは正規化しない。axis (ベクトル) には影響しない。
- **(b) `axis-angle->rot` (`kinematics.cljc` 42–50)**: `c (Math/cos angle) s (Math/sin angle)
  t (- 1.0 c)` — **`angle` を `Math/cos` / `Math/sin` に直接渡すのみ**。IEEE-754 では
  `Math/cos` / `Math/sin` は NaN・±Infinity を受けても例外を投げず **NaN** を返す。
  → angle=NaN なら c=NaN, s=NaN, t=NaN。angle=+Inf なら c=NaN (cos ∞ は undefined → NaN)、
  s=NaN、t=NaN。**数値検査 (isNaN / isInfinite / NaN 比較・assert) は皆無**。
  Rodrigues 行列 (48–50) はこれらを直接使うため全成分が NaN。
- **(c) `joint-transform` (`kinematics.cljc` 63–67)**: `(axis-angle->rot axis angle)` —
  angle をそのまま渡すのみ、検査なし。
- **(d) `combine` (`kinematics.cljc` 56–61)**: `mat3-mul` + `v+` で NaN 成分を照合 —
  `:xf/rot` も `:xf/pos` も NaN に汚染される。検査なし。
- **(e) `forward-kinematics` (`arm.cljc` 22–41)**: `angle (or (first angles) 0.0)` (行 38)。
  Clojure で NaN は truthy (nil/false ではない) ため `(or NaN 0.0)` は **NaN を返す** (0.0 充填
  されない)。これを `k/joint-transform` に渡し、loop 終端 `(empty? chain)` (行 35) のみで
  **数値検査・assert・throw なし**で NaN pose を `:xf/pos` に受理して返す。
- **(f) `end-effector` (`arm.cljc` 43–46)**: FK 結果の `last` のみ — NaN pose をそのまま返す。
  検査なし。

### NaN 検知面の有無 (fk / kinematics / end-effector)
`arm.cljc` (1–121) と `kinematics.cljc` (1–67) の全体を行レベルで通読した結果、
`isNaN` / `Double/isNaN` / `isInfinite` / `Double/isInfinite` / NaN 比較 / `assert` / `throw`
の **いずれも 0 件**。数値破れを検知・拒否・loud 化する面は **皆無**。
→ 判定規則 (NEXT 明示: FK/kinematics/end-effector に数値検査が 1 箇所でもあれば survived、
皆無なら refuted) により **refuted**。

### 型混在 (string) との対比 (H26/H27 同型で独立)
string 角度は `(Math/cos "abc")` で `ClassCastException` loud (H26/H27 確定)。
**NaN/±∞ は real double であり例外を投げず**、型混在 (CCE loud) とは独立した
数値破れの silent false-pass 面。torque-headroom / underrated-joints / export / giemon /
governor は FK も角度列も呼ばず (falsify-025/026) のため NaN pose を検知する面も 0 件。

## verdict: **refuted**
H29 は破れた (成立): NaN/±∞ 角を FK に渡すと `Math/cos`/`Math/sin` が例外を投げず NaN を
返し、`axis-angle->rot` → `combine` → `forward-kinematics` → `end-effector` と例外なしで
silent に NaN の `:xf/pos` が生成される。`or`/`Math` 系のどの面にも数値検査がなく
(arm.cljc/kinematics.cljc 全体で isNaN/isInfinite/NaN 比較/assert/throw 皆無)、NaN pose を
検知できる既存面も 0 件。型混在 (string → CCE loud) とは独立の**数値破れ silent false-pass
面の不在**が確定。現 API に DOF 実行入力面がないため現 fixture では非発火、将来の
kinematics 消費経路の numeric contract。

## コア (giemon-sim) への 1 行 message
falsify-027: H29 refuted — FK/kinematics/end-effector に数値検査が皆無で、NaN/±∞ 角は
`Math/cos`/`Math/sin` が例外を投げず NaN を返し、silent に NaN `:xf/pos` を生成する
(型混在は CCE loud と一切独立)。NaN/±∞ 角の guard (isNaN/isInfinite 検証 or FK 入口で
assert) の導入判断はコア側。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
# 本イテレーションは実行バックエンド (terminal/search/sandbox stat) が応答不能
# (bench-069〜082 同型条件、HOST LOAD 29.90 / 45.61 / 70.65、ncpu=10) のため REPL 実行は
# honesty-first で skipped。H29 は IEEE-754 の決定的性質 + 行レベル静的読取のみで確定 —
# 実行数字を捏造せず「静的読取」として記録。
# 環境回復後に以下を読めば各面の確定内容を byte 一致で再確認できる:
#   src/kotoba/giemon/kinematics.cljc 22–27 (normalize: zero? のみ),
#     42–50 (axis-angle->rot: Math/cos+Math/sin 直接・検査なし → NaN),
#     56–61 (combine: NaN 汚染), 63–67 (joint-transform: 通過のみ)
#   src/kotoba/giemon/arm.cljc 22–41 (FK: (or (first angles) 0.0) は NaN を返す,
#     loop 終端 (empty? chain) のみ・検査なし), 43–46 (end-effector: last のみ)
```

## 補足
- コード修正なし (測定専用、実装は読むだけ)。
- 決定的・タイムスタンプなしで記載。
- HOST LOAD 高 (pre-run 1min 29.90 / 5min 45.61 / 15min 70.65、ncpu=10)。
  read_file (実在 src) のみ成立したため静的読取は盤に実施。test スイート / seeded 再現は
  一律 skipped (honesty-first、決定的数字を捏造せず、基準値保持の判定は bench-066 確定値:
  robotics 14/50/0、giemon 46/115/0)。
- NEXT: H29 の確定 (falsify-027) をもって next を進めて可。次候補は
  FK/end-effector のナンバーガード (NaN/±∞) と長さ guard (H26/H27/H28) の導入判断
  (現 API に DOF 実行入力面なしのため非発火、将来径路の shape+numeric contract) と、
  backend 復旧後の test スイート + seeded 再現の本測定 (bench-084 以降で実施予定)。