# bench-148 — giemon sim-loop bench (日次)

判定: **measured** — test スイート実測は完走、基準値 (bench-066 確定 / bench-147 実測・HEAD 不変) と完全一致、回帰なし。git HEAD も前回と不変 (コード変更なし)。本 walk は新規 falsify・新仮説の判定なし (maturity NEXT: none)。

tests: robotics 14/50/0、giemon 46/115/0 (両者 exit 0)。

## 実行環境
- git HEAD: giemon `d0d3cb4` (d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe)、robotics `9459ca0` (9459ca0d5b3126472e23de6a77f725a9a3480770) — 基準値 (bench-066 確定) と不変。code 変更なし (giemon status は `?? sim-loop/` 未追跡のみ、robotics status 空)。
- HOST LOAD: 実行時 (10:35) 実測 1min 17.52 / 5min 16.74 / 15min 16.47 — ncpu=10 に対し 15min は約 1.65x で gate (>=2x ncpu=20) 未満。応答不能リスク低、suite 実測は完走。
- 実行バックエンド: terminal 直接 stdout は空のまま (echo 空出力)、だが `/tmp` write + read_file workaround は成立。execute_code は cron mode で BLOCKED。

## テスト (clojure -M:test 実測、/tmp redirect + read_file、cwd スクリプト内 cd 固定)
- **kotoba-lang/robotics**: `Ran 14 tests containing 50 assertions. 0 failures, 0 errors.` exit rc=0 (HEAD 9459ca0d5b3)
- **kotoba-lang/giemon**: `Ran 46 tests containing 115 assertions. 0 failures, 0 errors.` exit rc=0 (HEAD d0d3cb45fcc)

集計: robotics 14/50/0、giemon 46/115/0。基準値 (bench-066 確定・bench-147 最新実測完走) と完全一致。両者 exit rc=0。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (再現対象の学習ジョブ 0 件、git diff 空)。seeded 再現は対象なし (bench-147/113 と同方針)。

## 回帰
**なし** — robotics 14/50/0・giemon 46/115/0 が基準値と一致、両者 exit rc=0。measured で assert (bench-147 から連続実測、HEAD 不変)。新規 falsify なし。

## 再現コマンド
- 実行: `/tmp/runbench.sh` (cwd をスクリプト内 `cd` で固定): `clojure -M:test` (robotics → 14/50/0 rc=0; giemon → 46/115/0 rc=0)
- seeded 再現: 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。