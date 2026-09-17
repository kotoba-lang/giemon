# bench-270

## judgement: measured — clojure runner silent-zero 継続 (27 連続) / kbb runner 新規 hard-fail RC=1 へ悪化

## load
- 10:06 up 11 days, 2:49, load averages: 11.12 12.26 14.75 (15min) / ncpu=10 → ~1.1x、2x gate 未満で test 実行実施。

## commands (再現)
```
cd orgs/kotoba-lang/robotics && clojure -M:test   # > /tmp/b_rob2.txt → 0/0/0, RC=0
cd orgs/kotoba-lang/robotics && kbb -M:test       # > /tmp/b_rob.txt  → RC=1
cd orgs/kotoba-lang/giemon   && clojure -M:test   # > /tmp/b_gie2.txt → 0/0/0, RC=0
cd orgs/kotoba-lang/giemon   && kbb -M:test       # > /tmp/b_gie.txt  → RC=1
```

## results
### clojure -M:test (JVM runner)
- robotics: Ran **0 tests / 0 assertions / 0 failures**, RC=0, HEAD ad99366 — silent-zero 継続 (bench-244〜269 から **27 連続**)。
- giemon: Ran **0 tests / 0 assertions / 0 failures**, RC=0, HEAD 41ac173 — 同様に silent-zero。

### kbb -M:test (第2経路)
- robotics: **テスト開始前にクラッシュ, RC=1** — `Could not find namespace: html.core`。kbb banner: 3 dep(s) not :local/root and NOT on classpath (io.github.kotoba-lang/html, css, io.github.cognitect-labs/test-runner)、Node.js v26.0.0。
- giemon: **同様に RC=1** — `Could not find namespace: clojure.java.io`。kbb banner: 5 dep(s) not on classpath (io.github.kotoba-lang/text, html, css, robotics, cognitect-labs/test-runner)。
- 注: giemon HEAD は bench-269 記録の 00fd23f から **41ac173 へ変移** (robotics は ad99366 不変)。

## 比較 (基準: robotics 23/558/0, giemon 46/115/0)
- clojure runner: silent-zero (0/0/0 RC=0) は既知状態の継続で変化なし。根因確定済み (falsify-069: JVM require が .cljk をロード不能、falsify-073 静的再確定)。修復未着手 → 回帰 assert はしない (honest unmeasured)。
- kbb runner: bench-262 で 21/52/0 緑だった第2経路が本日 **起動時に dep 解決失敗でクラッシュ (RC=1)**。テスト数比較不能だが exit-code / 起動可否の観点で **新規 failure (regression: NEW FAILURE)**。
- 基準値 23/558/0 / 46/115/0 の実測緑再確立は不能。

## seeded reproduction
- sim-loop は L0、学習ジョブ無し → not-applicable。

## regression
- clojure runner: silent-zero 継続は測定不能であり回帰 assert 対象外 (honest unmeasured)。
- **kbb runner: YES — NEW FAILURE** (bench-262 実績 21/52/0 → 本日 RC=1 クラッシュ)。evidence 赤記録。

## falsify status
- FK guard repair (falsify-034 起) 未着手・残存。
- governor silent-nil 負テスト (falsify-071/072 起) 未着手・残存。
- test-runner 修復 (NEXT) は silent-zero (.cljk loader) 修復に加え、kbb の Maven/git coordinate 依存 (kotoba-lang/html, css, text, robotics, cognitect-labs/test-runner) を classpath 解決可能にする対応も含む必要あり。

### 再現性 (kbb RC=1 は race でなく確定)
- 並行実行 (/tmp/b_rob.txt, /tmp/b_gie.txt) と直列再実行 (/tmp/b_rob3.txt, /tmp/b_gie3.txt) の
  両方で同一エラーを再現 — 並行 dep download の race ではない。
- kbb 第2経路 (--backend sci --classpath src:test + 明示 require, falsify-070 手順) は
  本走未再実行 (予算切れ)。bench-262 の 21/52/0 緑が最終実測。
