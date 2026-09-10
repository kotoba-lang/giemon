# bench-114 — giemon sim-loop bench (日次)

判定: **measured** — test スイート実測は完走、基準値 (bench-066 確定 / bench-113 最新実測) と完全一致、回帰なし。git HEAD も前回と不変 (コード変更なし)。

tests: robotics 14/50/0、giemon 46/115/0 (両者 exit 0)。

## 実行環境
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 前回 (bench-113) と不変。git diff 追跡変更なし (IN-FLIGHT は未追跡 sim-loop/・simloop_files_list.txt・statout.txt・tmp_probe_write.md のみ、コード変更なし)。
- HOST LOAD: 実行後 (0:48) 8.17 / 9.91 /  ̂10.32 (15min = ncpu=10 の 約 1.0×) — 負荷は ~2× gate 未満、suite 実測は完走。
- 実行バックエンド: terminal 直接 stdout は空のまま (echo 空出力)、だが `/tmp` write + read_file workaround は成立。execute_code は cron mode  で BLOCKED。

##テスト (clojure -M:test 実測、/tmp redirect + read_file、cwd スクリプト内 cd 固定)
- **kotoba-lang/robotics**: `Ran 14 tests containing  ̂50 assertions. 0 failures,,  ̂0 errors.` exit rc=0 (HEAD 9459ca0)
- **kotoba-lang/giemon**: `Ran  ̂46 tests containing  ̂115 assertions.  ̂0 failures,0  errors.` exit rc=0 (HEAD d0d3cb4,

集計: robotics 14/50/0、giemon 46/115/0。基準値 (bench-066 確定・bench-113 最新実測) と完全一致。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (再現対象の学習ジョブ 0 件、git diff 空)。seeded 再現は対象なし (bench-113 と同方針)。

##回帰
**なし** — robotics 14/50/0・giemon 46/115/0 が基準値と一致、両者 exit rc=0。measured で assert。(bench-113 に続く実測完走、HEAD 不変)。

##反証 (falsify)
新規 falsify はなし。falsify-034 (H35: FK angle-count guard repair 実装済みか) は git diff 空 (追跡変更なし)・code 無変更のため残存なしのまま。本 walk は新規 H の判定なし (新仮説なし)。

##再現コマンド
- 実行: `/tmp/run_b114.sh` (cwd をスクリプト内 `cd` で固定): `clojure -M:test` (robotics →  ̂14/50/0 rc=0; giemon →  ̂46/115/0 rc=0)
- seeded 再現: 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。