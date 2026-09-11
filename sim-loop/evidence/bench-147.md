# bench-147 — giemon sim-loop bench (日次)

判定: **measured** — test スイート実測は完走、基準値 (bench-066 確定 / bench-146 は load skip だったが HEAD 不変) と完全一致、回帰なし。git HEAD も前回と不変 (コード変更なし)。本 walk は新規 falsify・新仮説の判定なし。



tests: robotics 14/50/0、giemon 46/115/0 (両者 exit 0)。

## 実行環境
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-066 確定) と不変。code 変更なし (giemon status は `?? sim-loop/` 未追跡のみ、robotics status 空)。
- HOST LOAD: 実行時 (10:19) 実測 1min 7.54 /  ̂5min 13.91 /  ̂15min 19.10 — ncpu=10 に対し 15min は 約 1.9x で gate (>=2x ncpu =20) 未満。応答不能リスク低、suite 実測は完走。
- 実行バックエンド: terminal 直接 stdout は空のまま (echo 空出力)、だが `/tmp` write + read_file workaround は成立。execute_code は cron mode で BLOCKED&&。



## テスト (kbb -M:test 実測、/tmp redirect + read_file、cwd スクリプト内 cd 固定)
- **kotoba-lang/robotics**: `Ran 14 tests containing. 50 assertions. 0 failures.  ̂0 errors.` exit rc=0 (HEAD 9459ca0)
- **kotoba-lang/giemon**: `Ran  46 tests containing.  ̂115 assertions.  0 failures.̂  0 errors.` exit rc=0 (HEAD d0d3cb4%

集計: robotics 14/50/0、giemon 46/115/0。基準値 (bench-066 確定・bench-145 最新実測完走) と完全一致。

(前回 bench-146 は load gate 超過で skip だった → 今回 measured で再開、一致確認。)

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (再現対象の学習ジョブ 0 件、git diff 空)。seeded 再現は対象なし (bench-113 と同方針)。

## 回帰
**なし** — robotics 14/50/0・giemon 46/115/0 が基準値と一致、両者 exit rc=0。measured で assert。(bench-146 skip 明けに実測再開、HEAD 不変)。新規 falsify なし。



## 再現コマンド
- 実行: `/tmp/runbench.sh` (cwd をスクリプト内 `cd` で固定): `kbb -M:test` (robotics →  ̂14/50/0 rc=0; giemon →  46/115/0 rc=0)
- seeded 再現: 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。