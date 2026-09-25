# bench-327

- date-anchor: cron run, JST (no timestamp dependency; deterministic)
- HOST: main-2.local, user junkawasaki (terminal backend 実測 whoami/hostname — full checkout 側、clojure/kbb/java 揃い)
- HOST LOAD (live `uptime`, 1/5/15-min 順): gate 確認時 (pre-run snapshot) 15-min 42.91 / ncpu 10 → ≈4.3x ≥ 2x gate; 実行時 START 15-min 38.44 ≈3.8x / END 15-min 33.04 ≈3.3x — gate 超過持続
- gate verdict: load 超過だが robotics test ツリーの前進を確認 (下記) したため測定実行を選択。全経路 /tmp redirect + read_file で決定的取得

## Tests (measured, live)
- robotics `clojure -M:test` @ f5efd49: **0/0/0 RC=0** — "Testing user / Ran 0 tests containing 0 assertions" silent-zero 持続 (bench-244〜326 の実測分と続く、実測分 55 連続・runner 修復未了)。clojure JVM runner が .cljk をロード不能 (falsify-069 根因) は現 HEAD でも不変
- robotics `kbb -M:test` @ f5efd49: **23 tests / 558 assertions / 0 failures / 0 errors, RC=0** — 基準値 robotics 23/558/0 と一致。4 ns (export-test / safety-invariants-test / ui-test / robotics-test) 全 run。falsify-074 が指摘した deps floor 未接続は 8c9ac97 (clojure-test-to-kotoba-test, nbb.edn +6/-1) で接続済みと実測で裏付け — RC=1 hard-fail から緑化
- kbb robotics 決定性検査 (同一 seed / 同一環境 2 連続実行): RUN1 = RUN2 = 23/558/0 RC=0 — **一致 (deterministic)**
- giemon `clojure -M:test` @ fe217f0: **0/0/0 RC=0** — silent-zero 持続 (同上)
- giemon `kbb -M:test` @ fe217f0: **RC=1** — 2 dep(s) not on classpath (org.clojure/tools.namespace, org.clojure/tools.cli) + 10 ns cljs.test 置換経路で `Could not find namespace: clojure.java.io` — falsify-074 (H75) 既知未接続と同値、新規回帰なし。暫定 sci 経路 (27/67/0) の再実測は本走 budget 切れで未実施

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job — seed / L1+ 学習ジョブ 0 件)。kbb 経路の 2 連続同一実行による決定性検査のみ実施 (上記・一致)

## Git HEADs (measured, live rev-parse)
- robotics: **f5efd49b12745362e387440197965e53d0ba2fab** — 前進 (bench-326 時点 ad99366 → f5efd49)。8c9ac97 "test: clojure.test -> kotoba.test (6 file(s))" (deps.edn/nbb.edn/test/*.cljk 4 件) + 22ba64f "edn: clojure.edn -> kotoba.lang.edn" (deps.edn/nbb.edn/scripts 2 件) の 2 merge。tree 実測: src 不変 1351a5a8 / **test 64f357ca → e59c3875 (test ツリー変更)** / deps.edn 14e0f934 → 2aeca2bc / nbb.edn a0f82a3f → f9fee9c8
- giemon: **fe217f0955422f5039b1a9c676169410ed858d66** — 69878b9 → fe217f0 前進 (0be2046 "sim-loop: land in-flight evidence bench-316..326 / falsify-085,086,088 + maturity.md" + merge)。tree 実測: src/test/deps.edn 全て 69878b9 と同一 (src e17e17ff / test 274e52b5 / deps.edn 1e682e34) — **evidence-only 前進・src/test 不変**
- in-flight (git status 実測): giemon `M sim-loop/status/maturity.md` (本走の更新) + `?? sim-loop/evidence/.hermes-tmp.Ytfzs4` (2595B・Sep 23 13:07・参照確認前の本走では不変更)。robotics clean。本走の bench-327.md は新規着地

## Judgement
- **measured** (load 超過 notwithstanding — robotics test ツリー前進による実測意義あり)
- regression: **none observable** — robotics 23/558/0 (kbb 緑・基準値一致・決定性 2 回一致)、giemon は clojure silent-zero + kbb 既知 RC=1 のみで新規破れなし。基準値 23/558/0・46/115/0 (clojure)・27/67/0 (giemon kbb 暫定) の据え置き
- runner status: clojure runner silent-zero 実測分 55 連続 (本走両 suite 再実測)。robotics kbb 経路は test ツリー前進 (8c9ac97) で緑化 — NEXT の runner 修復は robotics 側で kbb 経路が先行着地、clojure runner と giemon kbb 経路の修復が未了のまま
- falsify 新規なし (H1〜H88 全決着・falsify-087 欠番のままで変更なし)
- NEXT: (1) clojure runner silent-zero (falsify-069: .cljk ロード不能 — test 拡張子復旧 or loader 登録) + giemon kbb RC=1 (deps floor / clojure.java.io 代償) の修復。 (2) 修復後の再基準化 (clojure 経路 23/558/0・46/115/0 実測緑の再確立)。 (3) giemon kbb 暫定経路 27/67/0 の再実測 (本走 budget 切れ)。 (4) governor rejected レコード化 + 負テスト (falsify-076/077/078 系)。 (5) FK guard repair (falsify-034 起 refuted 継続)。 HEAD 参照: robotics f5efd49 / giemon fe217f0 (evidence-only・src/test 不変)

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min >= 2x ncpu -> load gate (本 run 15-min 33.04-42.91 / 10 = 3.3-4.3x 超過で実行)
cd orgs/kotoba-lang/robotics && kbb -M:test   # 23/558/0 RC=0 (緑・f5efd49 で 2 連続一致)
cd orgs/kotoba-lang/robotics && clojure -M:test   # 0/0/0 RC=0 (silent-zero 持続)
cd orgs/kotoba-lang/giemon && clojure -M:test     # 0/0/0 RC=0 (silent-zero 持続)
cd orgs/kotoba-lang/giemon && kbb -M:test         # RC=1 (deps 2 件未接続 + clojure.java.io 未解決・falsify-074 同値)
git -C orgs/kotoba-lang/robotics rev-parse HEAD    # f5efd49 実測
git -C orgs/kotoba-lang/giemon rev-parse HEAD      # fe217f0 実測
```

No code change.
