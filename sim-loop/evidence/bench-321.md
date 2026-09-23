# bench-321

- date-anchor: cron run, JST (no timestamp dependency; deterministic)
- HOST LOAD at gate check (measured, live, `uptime` order is 1/5/15-min): 15-min 13.28 / ncpu 10 → **≈1.3x** < 2x gate → tests executed (test 終了時 15-min 14.00 ≈1.4x、gate 内完走)

## Tests
- robotics `clojure -M:test`: executed — Ran 0 tests, 0 assertions, 0 failures, 0 errors, RC=0 (silent-zero シグネチャ、bench-320 実測値と同一)
- giemon `clojure -M:test`: executed — Ran 0 tests, 0 assertions, 0 failures, 0 errors, RC=0 (silent-zero シグネチャ、bench-320 実測値と同一)
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0 (回帰 assert なし — runner が 0 tests を返す既知 defect の再確認)
- 本 run 運用注記: terminal stdout 直接取得は空 (既知 env 問題) → /tmp redirect + read_file 経路で完走。CWD は絶対 path 直指定 (home 名 space 起因 mangle 回避、bench-320 の教訓を先取り)、phantom dir 生成なし (python os.path.isdir 実測)

## Git HEADs (measured)
- robotics: ad99366 (git rev-parse 実測・不変・clean、tree 59b12b8 実測 — bench-320 と同一)
- giemon: 69878b9 (git rev-parse 実測・不変・tree 1fae9e4 実測 — bench-317〜320 / falsify-084/085 と同一)
- in-flight (未コミット): giemon `M sim-loop/status/maturity.md` (本 run の status 更新) + `?? sim-loop/evidence/bench-316〜321.md` (bench-321 は本 run) + `?? falsify-085.md / falsify-086.md` (evidence-only commit 待ち)。src/test 不変。

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job — seed / L1+ 学習ジョブ 0 件) — unmeasured

## Judgement
- measured (silent-zero reconfirmed) — 基準値据え置き、回帰の assert なし
- regression: none observable (0/0/0 = 既知 defect シグネチャ; falsify-069 根因: JVM require が .cljk をロード不能、runner 修復未了)
- runner status: clojure runner silent-zero 実測分 **53 連続** (bench-244〜321、途中 load-skip 除く。bench-320 の 52 連続に本走 1 実測を追加)
- falsify 新規なし (H1〜H86 全決着・未決残存なし)
- NEXT は runner repair + re-baseline を再発行 (継続、HEAD 参照 69878b9)

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min >= 2x ncpu -> skip (本 run は gate 時 1.3x で gate 内実行)
cd orgs/kotoba-lang/robotics && clojure -M:test   # 0/0/0 RC=0 実測
cd orgs/kotoba-lang/giemon && clojure -M:test     # 0/0/0 RC=0 実測
cd orgs/kotoba-lang/giemon && git rev-parse --short HEAD^{tree}   # 69878b9 / 1fae9e4 実測
```
