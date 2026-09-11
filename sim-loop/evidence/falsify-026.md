# falsify-026 — H28: H26/H27 の長さ不一致 silent false-pass を将来 down-stream consumer（カメラ等）が引き回すとき、それを検知できる唯一の面は何か（25 件集計の収斂）

## 仮説 (1 iteration = 1 hypothesis)
H28: 「カメラ等の追加 down-stream 消費者が将来 FK の角度列長さ形状を、`end-effector`
以外にも引き回す時、H26/H27 (falsify-024/025 で確定 refuted) の長さ不一致 silent
false-pass を検知できる面は、既存 25 件の falsify から集計すると (1) FK 自体の長さ
guard か (2) FK を呼ぶ唯一の面 (`end-effector`) の count 検証の 2 択に収斂する」、
すなわち「既存の任意の consumer 面が欠落/過剰角度を検知できる」という代替仮説は
成立しない。

## 実測 (source-deterministic aggregate; 既存 falsify-001〜025 の静的集計・負荷非依存・決定的)
バックエンド (terminal / search / sandbox stat) が応答不能 (HOST LOAD 112.15 /
196.90 / 185.22、ncpu=10; bench-077〜080 同型条件) のため REPL 実行は honesty-first
で skipped — 本仮説は既存 evidence の行レベル静的読取のみで完全に決定的に確定できる集計
であり、決定的 (REPL 実行) 数字を捏造しない。

### 角度列長さ shape を参照し得る全面の列挙 (既存 falsify から)
- **(a) FK 自体 (`arm.cljc` 22–41)**: loop 終端 `(empty? chain)` のみ (行 35)。
  長さ比較 `(= (count chain) (count angles))`・`assert`・`throw` いずれも不在
  (falsify-024/H26 で確定)。短い角度列は `(or (first angles) 0.0)` (行 38) で
  0.0 充填、長過剰は chain 空で末尾を静かに捨てる。**形状検証面は不在**。
  唯一の「長さを知る」面だが、検証・abort を行わない。
- **(b) `end-effector` (`arm.cljc` 43–46)**: FK 結果の `last` のみ (行 46)。
  個数 (shape) を検査しない (falsify-025/H27 で確定)。FK を呼ぶ唯一の consumer。
- **(c) `within-limits?` (`arm.cljc` 15–20)**: `:joint/limit` lower/upper の
  RANGE 検証のみ。長さ (count) とは無関係、かつ全 src .cljc に実行 caller 不在
  (falsify-023/H25 で確定)。角度列 shape の検出面なし。
- **(d) `torque-headroom` (95–113) / `underrated-joints` (115–121)**: FK も
  角度列も引数に取らず `:arm/chain` の `:joint/limit :effort` と actuator
  `:cont-nm` のみ読む — 角度 shape void (falsify-025/H27 で確定)。
- **(e) `chain-actuators` (48–64) / `bom` (66–93)**: actuator BOM 生成のみで
  FK・角度列に無依存。
- **(f) `export.cljc` / `giemon.cljc` / `governor.cljc`**: FK / end-effector への
  呼び出し参照 0 (falsify-025/H27 で確定)。角度 shape は一切観測しない。

### 集計の収斂
角度列長さ shape を「参照し得る」面は (a) FK 自身 (長さ比較なし) と
(b) `end-effector` (`last` のみ) の 2 面のみ。そのいずれも検証・abort 面を提供せず、
(c)(d)(e)(f) は角度 shape を void 検知のまま。
→ **H26/H27 の長さ不一致 silent false-pass を検知し得る唯一の面**は、現実装の
consumer 集合では **皆無**。その void を閉じる最小介入点は
(1) FK 自体に長さ guard (assert / caller pre-check、`(empty? chain)` 終端の前に
`(= (count chain) (count angles))` 検証) か
(2) FK を呼ぶ唯一の面 (`end-effector`) への count 検証
の **2 択に収斂**する。カメラ等の将来 consumer が `end-effector` 以外にも FK を
呼ぶなら、その新 consumer は (b) と同じ `last`-only / count-void の構造を踏襲しない
限り検知できるが、既存実装には**検知できる面が存在しない**。

## verdict: **refuted**
H28 は破れた (成立): 既存 25 件の falsify を集計すると、角度列長さ shape を参照する
面は FK 自身と `end-effector` の 2 面のみで、いずれも長さ検証・abort 面がない。
`within-limits?` は RANGE のみ・caller 不在、torque-headroom / underrated-joints /
chain-actuators / bom / export / giemon / governor は FK も角度列も呼ばず void 検知。
つまり「長さ不一致を検知できる既存面」は **0 件**であり、void を閉じる最小介入点は
(1) FK 自体の長さ guard か (2) 唯一の FK consumer (`end-effector`) の count 検証の
2 択に収斂する。カメラ等の将来 down-stream が FK/end-effector を引き回しても、
その構造を踏襲しない限り最初から検知面を持たない — 本 void (形状強制面の不在) は
falsify-023/024/025 と同型の潜在赤で、現 API に DOF 実行入力面がないため現 fixture
では非発火、将来の kinematics 消費経路の shape contract。型混在 (string) 角のみ
(kinematics.cljc 42–50 の `Math/cos`) で CCE loud (H26/H27 と同型、長さ破れとは独立)。

## コア (giemon-sim) への 1 行 message
falsify-026: H28 refuted — H26/H27 の長さ不一致 silent false-pass を現実装で検知
できる面は 0 件 (FK 自身も `end-effector` も長さ検証なし、他 consumer は FK/角度列
void)。void を閉じる最小介入点は FK 自体の長さ guard か FK を呼ぶ唯一の面
(`end-effector`, arm.cljc 43–46) の count 検証の 2 択に収斂。guard 導入判断はコア側。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
# 本イテレーションは実行バックエンド (terminal/search/sandbox stat) が応答不能
# (bench-077〜080 同型条件、HOST LOAD 112.15 / 196.90 / 185.22、ncpu=10) のため
# REPL 実行は honesty-first で skipped。H28 は既存 falsify-001〜025 の行レベル静的
# 読取のみで完全に決定的な集計であり、実行数字を捏造せず「静的集計」として記録。
# 環境回復後に以下を読めば各面の確定内容を byte 一致で再確認できる:
#   sim-loop/evidence/falsify-023 (H25: within-limits? RANGE-only・caller 不在)
#   sim-loop/evidence/falsify-024 (H26: FK loop 終端 (empty? chain) のみ・0.0 充填)
#   sim-loop/evidence/falsify-025 (H27: end-effector last-only・他 consumer FK void)
#   src/kotoba/giemon/arm.cljk 22–46, 95–121 (上記 face の実体)
```

## 補足
- コード修正なし (測定専用、実装は読むだけ)。
- 決定的・タイムスタンプなしで記載。
- HOST LOAD 高 (pre-run 1min 112.15 / 5min 196.90 / 15min 185.22、ncpu=10)。
  read_file (キャッシュ内 src + 既存 evidence) のみ成立したため静的集計は盤に実施。
  test スイート / seeded 再現は一律 skipped (honesty-first、決定的数字を捏造せず、
  基準値保持の判定は bench-066 確定値: robotics 14/50/0、giemon 46/115/0)。
- NEXT: H28 の集計確定 (falsify-026) をもって next を進めて可。次候補は
  FK/`end-effector` の長さ一致 guard のコア側導入判断 (現 API に DOF 実行入力面なしの
  ため非発火、将来径路の shape contract) と、backend 復旧後の test スイート +
  seeded 再現の本測定 (bench-081 以降で実施予定)。