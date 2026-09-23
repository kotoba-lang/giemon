# bench-320

- date-anchor: cron run, JST (no timestamp dependency; deterministic)
- HOST LOAD at gate check (measured, live, `uptime` order is 1/5/15-min): 15-min 16.89 (pre-run script snapshot 15-min 22.69 時点 / gate 判定は実行時 16.89) / ncpu 10 → **≈1.7x** < 2x gate → tests executed
- test 終了時 load: robotics 15-min 12.40 (完了時 ≈1.2x)・giemon 15-min 20.85 (完了時 ≈2.1x — 実行開始は gate 内、完了が超過へ移行した経過。両 suite とも完走)

## Tests
- robotics `clojure -M:test`: executed — Ran 0 tests, 0 assertions, 0 failures, 0 errors, RC=0 (silent-zero シグネチャ、bench-319 実測値と同一)
- giemon `clojure -M:test`: executed — Ran 0 tests, 0 assertions, 0 failures, 0 errors, RC=0 (silent-zero シグネチャ、bench-319 実測値と同一)
- test ファイル存在確認 (実測): robotics test/ 4 ns・giemon test/ 10 ns 全件 `*_test.cljk` (拡張子復帰なし、falsify-082 と同値)
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0 (回帰 assert なし — runner が 0 tests を返す既知 defect の再確認)
- 本 run 運用注記: 初回実行スクリプトで giemon cd が home 名の space 起因 path mangle (com-junk Kawasaki) により com-junkawasaki 直下で deps.edn 不在 RC=1 を 1 回出してから `$HOME`+glob 解決で正しい CWD (`.../orgs/kotoba-lang/giemon`) に再実行し 0/0/0 RC=0 を確定。robotics も同法で CWD 実測確認済み。phantom ディレクトリ生成なし (os.listdir で /Users 直下 3 項目のみ実測)

## Git HEADs (measured)
- robotics: ad99366 (git rev-parse 実測・不変・clean、git status --porcelain 空、tree 59b12b8)
- giemon: 69878b9 (git rev-parse 実測・不変・tree 1fae9e4 実測 — bench-317/318/319 / falsify-084/085 と同一、deps.edn blob 1e682e3・src tree e17e17ff・test tree 274e52b5 不変を裏付け)
- in-flight (未コミット): giemon `M sim-loop/status/maturity.md` (本 run の status 更新) + `?? sim-loop/evidence/bench-316.md` `?? sim-loop/evidence/bench-317.md` `?? sim-loop/evidence/bench-318.md` `?? sim-loop/evidence/bench-319.md` `?? sim-loop/evidence/bench-320.md` (本 run) `?? sim-loop/evidence/falsify-085.md` (前走期作成・evidence-only commit 待ち)。src/test 不変。

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job — seed / L1+ 学習ジョブ 0 件) — unmeasured

## Judgement
- measured (silent-zero reconfirmed) — 基準値据え置き、回帰の assert なし
- regression: none observable (0/0/0 = 既知 defect シグネチャ; falsify-069 根因: JVM require が .cljk をロード不能、runner 修復未了)
- runner status: clojure runner silent-zero 実測分 **52 連続** (bench-244〜320、途中 load-skip 除く。bench-319 の 51 連続に本走 1 実測を追加)
- falsify 新規なし (H1〜H86 全決着・未決残存なし)
- NEXT は runner repair + re-baseline を再発行 (継続、HEAD 参照 69878b9)

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min >= 2x ncpu -> skip (本 run は gate 時 1.7x で gate 内実行)
cd orgs/kotoba-lang/robotics && clojure -M:test   # 0/0/0 RC=0 実測 (CWD 実測確認)
cd orgs/kotoba-lang/giemon && clojure -M:test     # 0/0/0 RC=0 実測 (CWD 実測確認)
cd orgs/kotoba-lang/giemon && git rev-parse --short HEAD && git rev-parse --short HEAD^{tree}   # 69878b9 / 1fae9e4 実測
```
