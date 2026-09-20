# bench-304

## Judgement: measured — silent-zero 持続 (回帰 assert なし、既知 runner 未修復)

- Date anchor: 2026-09-20 (JST), uptime `19:05 up 2 days, 3:16`
- Load: 1/5/15-min = 16.86 / 19.49 / 17.20 (run 開始時) → 18.99 / 18.11 / 17.20 (run 完了時), hw.ncpu = 10
  → 15-min ≈ 1.7–1.8x、gate (~2x ncpu) 未満で test スイート実行。
- HEADs (変更なし): robotics `ad99366` / giemon `41ac173` (git rev-parse 実測)
- In-flight: giemon working tree に ` M sim-loop/status/maturity.md` + untracked bench-270〜 evidence
  群のみ (bench 反復作業物、コード変更なし)。

## Measurements

- `clojure -M:test` robotics: **0 tests / 0 assertions / 0 failures, RC=0**
  (output: `Running tests in #{"test"}` → `Ran 0 tests containing 0 assertions.`)
- `clojure -M:test` giemon:   **0 tests / 0 assertions / 0 failures, RC=0** (同上)
- → silent-zero 持続は bench-244〜304 実測分で **45 連続** (runner 修復未了、falsify-069 根因確定:
  JVM require が .cljk をロード不能)。RC=0 の緑と読んではならない。
- seeded reproduction: not-applicable (sim-loop L0, no job)。

## Reference values (据え置き)

- robotics: 23/558/0 @ ad99366 (HEAD 不変)
- giemon: 46/115/0 @ 41ac173 (HEAD 不変)

## Regression

- New regression assertion: none — silent-zero は既知の runner 未修復 (falsify-069/082 で
  根因・未着手 45 連続まで確定済み) で、新規回帰ではない。基準値据え置き。
- kbb -M:test 第2経路: 本走は未実行 (clojure 経路の計数で事足りた・cron 予算)。既知状態:
  giemon 5 dep 未解決 + nbb.edn 不在 (falsify-074/080 同値)、robotics 3 dep + html.core 未解決。

## Falsify status

- FK guard repair (falsify-034 起) 残存なし変化 — 未着手のまま。
- test-runner 修復 (falsify-082) — HEAD 41ac173 に修復 commit 無しを本走の clojure 実測
  (0/0/0) と静的既知で補強。拡張子戻し / loader 登録 / nbb.edn 接続のいずれも未着地。

## Repro commands

```
bash /tmp/b304.sh    # (script: cd robotics; clojure -M:test > /tmp/b304_rob.txt; cd giemon; clojure -M:test > /tmp/b304_gie.txt)
cat /tmp/b304_rob.txt /tmp/b304_gie.txt   # -> 両 suite "Ran 0 tests containing 0 assertions." RC=0
uptime; sysctl -n hw.ncpu
git -C <proj> rev-parse --short HEAD  # ad99366 / 41ac173
```

No code change.
