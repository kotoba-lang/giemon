# bench-152 — giemon sim-loop bench (日次)

判定: **measured** — HOST LOAD (15min 17.74, ncpu=10 の約 1.77x) は gate (>=2x ncpu=20) 未満で、重い test スイートを問題なく完走できた。robotics 14/50/0、giemon 46/115/0 を実測で再確認、基準値 (bench-066 確定) と完全一致。回帰なし (measured)。

tests: robotics **14 / 50 / 0** (rc=0)、giemon **46 / 115 / 0** (rc=0) — 実測。

## 実行環境
- git HEAD: giemon `d0d3cb4` (d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe)、robotics `9459ca0` (9459ca0d5b3126472e23de6a77f725a9a3480770) — 基準値 (bench-066 確定) と不変。code 変更なし (giemon status は `?? sim-loop/` 未追跡のみ)。
- HOST LOAD: 計測時 実測 1min 18.80 / 5min 16.24 / 15min 17.74 — ncpu=10 に対し 15min は約 1.77x で gate (>=2x ncpu=20) 未満。スイート完走に十分安定。
- 実行バックエンド: terminal 直接 stdout は空のまま (スキル既知)。`/tmp` redirect + read_file workaround を使用。

## テスト (clojure -M:test)
- kotoba-lang/robotics: **14 test / 50 assertion / 0 failure / 0 errors** (exit 0)
- kotoba-lang/giemon: **46 test / 115 assertion / 0 failure / 0 errors** (exit 0)
- 基準値 (bench-066 確定 14/50/0・46/115/0) と完全一致。**回帰なし (measured)**。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (再現対象の学習ジョブ 0 件)。seeded 再現は対象なし (bench-151/113 と同方針)。

## 回帰
**なし (measured)** — 実測で robotics 14/50/0・giemon 46/115/0、基準値と完全一致。git HEAD 不変 (d0d3cb4 / 9459ca0)。

## 再現コマンド
- 実行: `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test` → 14/50/0 rc=0; `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M:test` → 46/115/0 rc=0。
- seeded 再現: 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。