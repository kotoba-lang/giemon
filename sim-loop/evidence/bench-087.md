# bench-087 — SKIPPED (load & unresponsive backend)

## verdict
- test スイート (robotics / giemon `clojure -M:test`): **skipped (load & backend 応答不能)**
- seeded 再現 (sim-loop L1 以降, 同一 seed 2 回): **skipped (load & backend 応答不能)**
- 回帰: **判定不能**（測定できず）— unmeasured のため assert しない (honesty-first)

## 理由
- HOST LOAD (pre-run 時点): 43.22 / 42.14 / 36.36 (1min/5min/15min), ncpu=10
  → 1min load (43.22) ≫ ncpu (10)。重い実験は省略 (bench ルール、HOST LOAD 高)。
- 実行バックエンド応答不能: terminal が空出力 (exit 0) を返すまま応答せず
  (`pwd` / `echo` / `uptime` / `date` すべて空)。search_files は
  `could not stat .../giemon (sandbox may still be starting or was removed)`
  を返し evidence/sandbox stat 不能。execute_code は cron モード blocked。
  → bench-069〜086 と同じ応答不能条件。write_file / read_file のみ成立。

## 測定手段なし
- clojure test、seeded 再現いずれも実行不能（実行数字を捏造せず skipped 記録）。

## 静的読取 (read_file のみ成立、負荷非依存・決定的)
- `src/kotoba/giemon/arm.cljc` (1–121) は bench-084/085/086 と byte 一致 (コード変化なし):
  FK 22–41 loop 終端 `(empty? chain)` のみ・行 38 `(or (first angles) 0.0)` は NaN を 0.0
  にせず isNaN/isInfinite/長さ assert 皆無、end-effector 43–46 は `last` のみ、
  within-limits? 15–20 は RANGE-only・src caller 不在、torque-headroom/underrated-joints
  は FK 呼び出しなし。
- `test/kotoba/giemon/arm_test.cljc` (1–40) は prior record と byte 一致 (変化なし):
  forward-kinematics 15–22 は zero/missing-default のみ (NaN/長さ破れの拒否断言なし)、
  end-effector 24–26 恒等のみ、within-limits 28–30 RANGE-only、torque-headroom 32–40
  角度破れに関与せず (→ falsify-029/H31 の static base、変更なし)。

## 再現コマンド (今回実行不可。負荷収束・backend 回復後に実行すべき)
- clojure -M:test   # orgs/kotoba-lang/robotics と orgs/kotoba-lang/giemon 両方
- seeded 再現: sim-loop 学習ジョブを同一 seed で 2 回実行し結果一致を検査

## 索引・NEXT
- falsify-001〜029 (H1〜H31 refuted 閉) は prior 記録のまま（本イテレーション新規 falsify なし）。
- NEXT: falsify-029 (H31) は前回確定済み。次候補は FK/end-effector の numeric guard
  (NaN/±∞, H29/H30) + shape guard (長さ, H26/H27/H28) の導入判断（コア側, コード修正 +
  test 追加を伴う）と、backend 復旧後の test スイート + seeded 再現の本測定（bench-088 で実施予定）。
- 基準値 (robotics 14/50/0, giemon 46/115/0) は bench-066 確定値のまま — 回帰は unmeasured
  のため assert せず（honesty-first）。コード修正なし（測定専用・読むだけ）。