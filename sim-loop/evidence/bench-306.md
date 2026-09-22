# bench-306

## Judgement: measured — silent-zero 持続 (回帰 assert なし、既知 runner 未修復)

- Date anchor: 2026-09-21 (JST), uptime `07:10 up 2 days, 15:21`
- Load: 1/5/15-min = 10.86 / 10.73 / 14.75 (記録時), hw.ncpu = 10 → 15-min ≈ 1.48x。
  前回ゲート 17.48 (1.75x) / 実行開始 15.09 (1.51x) / 実行完了 15.03 (1.50x) →
  全ポイントで gate (~2x ncpu) 未満で test スイート実行。負荷は下降帯。
- HEADs: robotics `ad99366` (不変) / **giemon `8c3c3e6` (41ac173 から前進)** (git rev-parse 実測)

## HEAD 前進 (giemon 41ac173 → 8c3c3e6) — 判定: evidence-only、src/test 不変

- 前進分 `git diff --stat 41ac173..8c3c3e6` = 48 files, +2059/−4、全て
  `sim-loop/evidence/` (bench-270〜305 / falsify-074〜083) + `sim-loop/status/maturity.md`
  + `sim-loop/status/probe.txt`。**src/ と test/ は不変** (landed WIP のみ:
  ffaf91b「sim-loop: land bench-303〜305 / falsify-083」、8c3c3e6 merge)。
- → 基準値 46/115/0 は src/test 不変でそのまま適用。giemon 基準値の参照 HEAD を
  41ac173 → 8c3c3e6 に更新 (実測値は不変)。
- In-flight: HEAD 前進で未コミット evidence が landed、両 repo の
  `git status --porcelain` は空 (robotics / giemon とも clean)。コード変更なし。

## Measurements

- `clojure -M:test` robotics: **0 tests / 0 assertions / 0 failures, RC=0**
  (output: `Running tests in #{"test"}` → `Ran 0 tests containing 0 assertions.`)
- `clojure -M:test` giemon:   **0 tests / 0 assertions / 0 failures, RC=0** (同上)
- → silent-zero 持続は bench-244〜306 実測分で **46 連続** (bench-305 は load skip 計上外。
  runner 修復未了、falsify-069 根因確定: JVM require が .cljk をロード不能)。RC=0 の緑と読んではならない。
- seeded reproduction: not-applicable (sim-loop L0, no job)。

## Reference values (据え置き・HEAD 参照更新)

- robotics: 23/558/0 @ ad99366 (HEAD 不変)
- giemon: 46/115/0 @ **8c3c3e6** (HEAD 前進・src/test 不変で実測値不変)

## Regression

- New regression assertion: none — silent-zero は既知の runner 未修復 (falsify-069/082 で
  根因・未着手確定済み) で、新規回帰ではない。giemon HEAD 前進も evidence-only で
  src/test 不変、基準値据え置き。
- kbb -M:test 第2経路: 本走は未実行 (clojure 経路の計数で事足りた・cron 予算)。
  既知状態: giemon 5 dep 未解決 + nbb.edn 不在 (falsify-074/080 同値)、
  robotics 3 dep + html.core 未解決。HEAD 前進は evidence-only なので状態不変。

## Falsify status

- FK guard repair (falsify-034 起) 残存なし変化 — 未着手のまま。
- test-runner 修復 (falsify-082) — 本走の clojure 実測 (0/0/0) が拡張子戻し /
  loader 登録 / nbb.edn 接続のいずれも未着地を補強。HEAD 前進 (8c3c3e6) には
  修復 commit 無し (evidence-only)。

## Repro commands

```
bash /tmp/b306.sh    # (script: cd robotics; clojure -M:test; cd giemon; clojure -M:test; uptime at start/end)
cat /tmp/b306_out.txt    # -> 両 suite "Ran 0 tests containing 0 assertions." RC=0
uptime; sysctl -n hw.ncpu
git -C orgs/kotoba-lang/robotics rev-parse --short HEAD   # ad99366
git -C orgs/kotoba-lang/giemon   rev-parse --short HEAD   # 8c3c3e6
git -C orgs/kotoba-lang/giemon diff --stat 41ac173..8c3c3e6   # -> evidence-only, src/test 不変
```

No code change.
