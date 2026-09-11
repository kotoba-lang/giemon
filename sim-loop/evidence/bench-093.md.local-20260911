# bench-093 — SKIPPED (load & unresponsive backend)

## verdict
- test スイート (robotics / giemon `clojure -M:test`): **skipped (load & backend 応答不能)**
- seeded 再現 (sim-loop L1 以降, 同一 seed 2 回): **skipped (load & backend 応答不能)**
- 回帰: **判定不能**（測定できず）— unmeasured のため assert しない (honesty-first)

## 理由
- HOST LOAD (本 iteration 実測): 21.35 / 24.47 / 26.73 (1min/5min/15min), ncpu=10
  → 実行バックエンド応答不能のため重い実験 (test スイート・学習再現) は実行不能。
- 実行バックエンド応答不能: 本 iteration の fresh probe (`date` / `echo MARKER` /
  `true` / `uptime`) がすべて空出力 (exit 0) のまま応答せず。shell は通過するが
  stdout が戻らない (redirect+read_file でのみ成立しており、`uptime` の数値は
  /tmp 経由で読取確認)。search_files は `could not stat .../giemon
  (sandbox may still be starting or was removed)` を返し sandbox stat 不能。
  execute_code は cron モード blocked。
  → bench-069〜092 と同じ応答不能条件。write_file / read_file のみ成立。

## 測定手段なし
- clojure test、seeded 再現いずれも実行不能（実行数字を捏造せず skipped 記録）。
- uptime 数値は stdout 直行が空のため /tmp/load_probe.txt への redirect 読戻しで取得
  (21.35/24.47/26.73) — これは実測値であり捏造ではない。

## 静的読取 (read_file のみ成立、負荷非依存・決定的)
- `src/kotoba/giemon/arm.cljc` (1–50 読取, 全 121 行) は bench-091/092 と内容一致
  (コード変化なし): FK 22–41 loop 終端 `(empty? chain)` のみ (行 35)・行 38
  `(or (first angles) 0.0)` は NaN (truthy) を 0.0 にせず isNaN/isInfinite/長さ
  assert 皆無、end-effector 43–46 は `last` のみ、within-limits? 15–20 は
  RANGE-only (`<=` 比較)。	falsify 対象面 は偽のまま変化なし。

## 再現コマンド (今回実行不可。負荷収束・backend 回復後に実行すべき)
- clojure -M:test   # orgs/kotoba-lang/robotics と orgs/kotoba-lang/giemon 両方
- seeded 再現: sim-loop 学習ジョブを同一 seed で 2 回実行し結果一致を検査

## 索引・NEXT
- bench-092 の「基準値再確認 (bench-093 で実施予定)」は本 iteration も backend
  応答不能 (load 21.35 1min / ncpu=10) のため再確認できず、繰り越し。決定的数字は捏造しない。
- 基準値 (robotics 14/50/0, giemon 46/115/0) は bench-066 確定値のまま — 回帰は
  unmeasured のため assert せず (honesty-first)。コード修正なし (測定専用・読むだけ)。
- NEXT: backend 復旧後の test スイート + seeded 再現による基準値再確認 (bench-094)。