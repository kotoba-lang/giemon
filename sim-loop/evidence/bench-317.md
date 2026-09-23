# bench-317

- date-anchor: cron run, JST (no timestamp dependency; deterministic)
- HOST LOAD at gate check (measured, live, `uptime` order is 1/5/15-min): 15-min 11.94 (1-min 11.15, 5-min 19.13) / ncpu 10 → **≈1.2x** < 2x gate → tests executed
- pre-run script snapshot (earlier same window): 15-min 12.31 ≈1.2x (gate 未満)
- test 終了時 load: 15-min 19.13 ≈1.9x (実行中 rise・gate 内完走)

## Tests
- robotics `clojure -M:test`: executed — Ran 0 tests, 0 assertions, 0 failures, 0 errors, RC=0 (silent-zero シグネチャ、bench-316 実測値と同一)
- giemon `clojure -M:test`: executed — Ran 0 tests, 0 assertions, 0 failures, 0 errors, RC=0 (silent-zero シグネチャ、bench-316 実測値と同一)
- test ファイル存在確認 (実測): robotics test/ 4 ns・giemon test/ 10 ns 全件 `*_test.cljk` (拡張子復帰なし、falsify-082 と同値)
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0 (回帰 assert なし — runner が 0 tests を返す既知 defect の再確認)

## Git HEADs (measured)
- robotics: ad99366 (git rev-parse 実測・不変・clean、git status --porcelain 空)
- giemon: 69878b9 (git rev-parse 実測・不変。tree hash 実測: HEAD tree 1fae9e4・deps.edn blob 1e682e3・src tree e17e17ff・test tree 274e52b5 — falsify-084/085 と同一の 3 ハッシュで src/test/deps.edn 不変を裏付け)
- in-flight (未コミット): giemon `M sim-loop/status/maturity.md` (本 run の status 更新) + `?? sim-loop/evidence/bench-316.md` `?? sim-loop/evidence/falsify-085.md` (bench-316 期に作成・本 run で evidence-only commit されるもの)。src/test 不変。

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job — seed / L1+ 学習ジョブ 0 件) — unmeasured

## Judgement
- measured (silent-zero reconfirmed) — 基準値据え置き、回帰の assert なし
- regression: none observable (0/0/0 = 既知 defect シグネチャ; falsify-069 根因: JVM require が .cljk をロード不能、runner 修復未了)
- runner status: clojure runner silent-zero 実測分 **49 連続** (bench-244〜317、途中 load-skip 除く。bench-316 の 48 連続に本走 1 実測を追加)
- falsify 新規なし (H1〜H86 全決着・未決残存なし)
- NEXT は runner repair + re-baseline を再発行 (継続、HEAD 参照 69878b9)

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min >= 2x ncpu -> skip (本 run は 1.2x で gate 内実行)
cd orgs/kotoba-lang/robotics && clojure -M:test   # 0/0/0 RC=0 実測
cd orgs/kotoba-lang/giemon && clojure -M:test     # 0/0/0 RC=0 実測
cd orgs/kotoba-lang/giemon && git rev-parse HEAD && git rev-parse HEAD^{tree}   # 69878b9 / 1fae9e4 実測
```
