# bench-094 — SKIPPED (load & unresponsive backend)

## verdict
- test スイート (robotics / giemon `kbb -M:test`): **skipped (load & backend 応答不能)**
- seeded 再現 (sim-loop L1 以降, 同一 seed 2 回): **skipped (load & backend 応答不能)**
- 回帰: **判定不能**(測定できず — unmeasured のため assert しない (honesty-first)

## 理由
- HOST LOAD (本 iteration 実測、redirect+read_file で読取): 41.32 / 31.97 / 27.35 (1min/5min/15min, ncpu=10)
  — pre-run 時点 18.90 / 19.71 / 22.91 から上昇し、実行バックエンド応答不能閾値を超過。

- 実行バックエンド応答不能: fresh probe (`echo` / `uptime` / `date` / `pwd` / `ls`) がすべて
  空出力 (exit 0) のまま応答せず。shell は通過するが stdout が戻らない
  (redirect+read_file でのみ成立、`date`/`uptime` の数値は /tmp 経由で読取確認)。search_files
   read_file は relative path で `could not stat .../giemon` (sandbox 未起動/除去) を返し、
   absolute path のみ成立。execute_code は cron モード blocked。
- → bench-069〜093 と同じ応答不能条件。。write_file / absolute read_file のみ成立拡


## 測定手段なし
- clojure test、seeded 再現いずれも実行不能 (実行数字を捏造せず skipped 記録)。
- falsify 本測定も skip (行レベル静的読取による falsify-024/025 既存記録を参照;M NEXT は none)。

## 再現手順
1. uptime で load 1min が ncpu=10 を超える / terminal が空出力 exit 0 を返す
2. 重い実験 (test スイート・seeded 再現) を実行せず skipped と記録