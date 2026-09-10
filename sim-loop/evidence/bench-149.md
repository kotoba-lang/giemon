# bench-149 — giemon sim-loop bench (日次)

判定: **unmeasured (load 超過)** — HOST LOAD が gate (>=2x ncpu=20) を超え非応答リスク大のため、重い test スイート実測は一律 skipped。回帰 assert せず、基準値 (bench-066 確定 14/50/0・46/115/0) 据え置き。git HEAD は前回 (bench-148) と不変 (コード変更なし)。本 walk は新規 falsify・新仮説の判定なし (maturity NEXT: none)。

tests: robotics / giemon — **計測せず (skipped, load)**。基準値据え置き: robotics 14/50/0、giemon 46/115/0。

## 実行環境
- git HEAD: giemon `d0d3cb4` (d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe)、robotics `9459ca0` (9459ca0d5b3126472e23de6a77f725a9a3480770) — 基準値 (bench-066 確定) と不変。code 変更なし (giemon status は `?? sim-loop/` 未追跡のみ)。
- HOST LOAD: 計測時 (10:50) 実測 1min 59.53 / 5min 48.85 / 15min 32.19 — ncpu=10 に対し 15min は約 3.2x で gate (>=2x ncpu=20) 超過。1min は約 6x で上昇中 (54→59)。非応答リスク大のため suite 実測を skipped。
- 実行バックエンド: terminal 直接 stdout は空のまま。execute_code は cron mode で BLOCKED。

## テスト (clojure -M:test)
- **skipped (load 超過)** — uptime 15min 32.19 >= 2x ncpu (20)。重い `clojure -M:test` (robotics / giemon) は非応答リスクのため実行せず。基準値據え置き (robotics 14/50/0、giemon 46/115/0)。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (再現対象の学習ジョブ 0 件)。seeded 再現は対象なし (bench-148/113 と同方針)。

## 回帰
**判定不可 (unmeasured, load 超過で未計測)** — 回帰 assert せず、基準値前提の据え置き。git HEAD 不変 (d0d3cb4 / 9459ca0) でコード変更なしのため回帰リスク低いが、実測していない以上 assert しない。honest。

## 再現コマンド
- 実行: skipped (load 超過)。gate 回復後に `/tmp/runbench.sh` (cwd をスクリプト内 `cd` で固定) で `clojure -M:test` (robotics → 14/50/0 rc=0; giemon → 46/115/0 rc=0) を実測する。
- seeded 再現: 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。