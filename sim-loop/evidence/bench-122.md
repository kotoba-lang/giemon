# bench-122 — giemon sim-loop bench (日次)

判定: **measured** — test スイート実測は完走、基準値 (bench-066 確定 / bench-111 最新実測) と完全一致、回帰なし。



tests: robotics 14/50/0、giemon 46/115/0 (両者 exit 0)。



## 実行環境

- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-066 確定) と不変。
- git diff: robotics status 空 (追跡変更なし)。giemon porcelain = 4 未追跡のみ: sim-loop/・simloop_files_list.txt・statout.txt・tmp_probe_write.md (tracked 変更なし) — コード変更なし。
- HOST LOAD: 実行中 (3:33) 20.38 /探 18.21 /走 18.95 (15min = ncpu=10 の 約 1.9×) — Load gate (15min ≥ 2×ncpu≈20) 未満の負荷帯で suite 実測は完走 (bench-102～111 と同方針)。
- 実行バックエンド: terminal 直接 stdout は空のまま (/tmp redirect workaround)。execute_code は cron mode で BLOCKED。本 walk も `/tmp` redirect + read_file で test 出力・git HEAD・uptime を実測取得。



## テスト (kbb -M:test 実測、/tmp redirect + read_file)

- **kotoba-lang/robotics**: `Ran 14 tests containing 50 assertions. 0 failures,  ̂0 errors.` exit rc=0
- **kotoba-lang/giemon**:    `Ran 46 tests containing  ̂115 assertions. 0 failures,,  ̂0 errors.` exit rc=0

集計: robotics 14/50/0、giemon 46/115/0。基準値 (bench-066 確定・bench-111 最新実測) と完全一致。



## Seeded 再現 verdict

**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (seed/L1+ 学習ジョブ 0 件,git diff 空)。再現対象の学習ジョブが存在しないため、本測定は行わない (bench-105〜121 と同方針)。



##回帰

**なし** — robotics 14/50/0・giemon 46/115/0 が基準値と一致、両者 exit rc=0。measured で assert。(bench-111 に続く実測完走。)



##反証 (falsify)

新規 falsify はなし。最新 falsify-040、maturity.md の NEXT は none で新規 H の判定なし (code 無変更のため)。未決 falsify 残存なし。





##再現コマンド

- 実行: `kbb -M:test` (workdir: orgs/kotoba-lang/robotics → 14/50/0 rc=0; orgs/kotoba-lang/giemon →  46/115/0 rc=0)
- seeded 再現: 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。