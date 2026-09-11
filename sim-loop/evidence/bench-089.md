# bench-089 — SKIPPED (load & unresponsive backend)

## verdict
- test スイート (robotics / giemon `clojure -M:test`): **skipped (load & backend 応答不能)**
- seeded 再現 (sim-loop L1 以降, 同一 seed 2 回): **skipped (load & backend 応答不能)**
- 回帰: **判定不能**（測定できず）— unmeasured のため assert しない (honesty-first)

## 理由
- HOST LOAD (pre-run 時点): 50.13 / 40.28 / 40.14 (1min/5min/15min), ncpu=10
  → 1min load (50.13) ≫ ncpu (10)。重い実験は省略 (bench ルール、HOST LOAD 高)。
- 実行バックエンド応答不能: terminal が空出力 (exit 0) を返すまま応答せず
  (`pwd` / `echo` / `uptime` / `date` すべて空)。search_files は
  `could not stat .../giemon (sandbox may still be starting or was removed)`
  を返し evidence/sandbox stat 不能。
  → bench-069〜088 と同じ応答不能条件。write_file / read_file のみ成立。

## 測定手段なし
- clojure test、seeded 再現いずれも実行不能（実行数字を捏造せず skipped 記録）。

## 静的読取 (read_file のみ成立、負荷非依存・決定的)
- `src/kotoba/giemon/arm.cljk` (1–121) は bench-084〜088 と byte 一致 (コード変化なし):
  FK 22–41 loop 終端 `(empty? chain)` のみ・行 38 `(or (first angles) 0.0)` は NaN (truthy)
  を 0.0 にせず isNaN/isInfinite/長さ assert 皆無、end-effector 43–46 は `last` のみ、
  within-limits? 15–20 は RANGE-only・src caller 不在 (falsify-023)、torque-headroom /
  underrated-joints / chain-actuators / bom は FK も角度列も呼ばず void 検知
  (falsify-025/026)。
- `test/kotoba/giemon/arm_test.cljk` (1–40) は bench-087/088 にて byte 一致確認済み
  (変化なし、FK の shape/numeric 破れを検証する断言なし → falsify-029/H31)。

## 再現コマンド (今回実行不可。負荷収束・backend 回復後に実行すべき)
- clojure -M:test   # orgs/kotoba-lang/robotics と orgs/kotoba-lang/giemon 両方
- seeded 再現: sim-loop 学習ジョブを同一 seed で 2 回実行し結果一致を検査

## 索引・NEXT
- falsify-001〜029 (H1〜H31 refuted 閉) は prior 記録のまま（本イテレーション新規 falsify なし）。
- NEXT: falsify-029 (H31) は確定済み。FK/end-effector の numeric guard (NaN/±∞, H29/H30) +
  shape guard (長さ, H26/H27/H28) の導入判断はコア (giemon-sim) 側の実施対象であり本 bot は
  実施しない。本 bot の残る測定面は backend 復旧後の test スイート + seeded 再現による
  基準値再確認 (bench-090 で実施予定) — L0 昇格条件 (学習ジョブ実装) と基準値再検証の両方が
  復旧待ち。falsify 面 (src 層 H26-H30 + test 層 H31) は網羅的に閉じたため新規 void-falsify
  候補なし。
- 基準値 (robotics 14/50/0, giemon 46/115/0) は bench-066 確定値のまま — 回帰は unmeasured
  のため assert せず（honesty-first）。コード修正なし（測定専用・読むだけ）。