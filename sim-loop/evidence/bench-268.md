# bench-268

## judgement: measured — silent-zero 継続 (runner 未修復)

## load
- 4:05 up 10 days, 20:48, load averages: 22.65 18.48 **15.39** (15min) / ncpu=10 → ~1.54x、2x gate 未満で test 実行実施。

## commands (再現)
```
cd orgs/kotoba-lang/robotics && kbb -M:test   # > /tmp/b_rob.txt
cd orgs/kotoba-lang/giemon   && kbb -M:test   # > /tmp/b_gie.txt
```

## results
- robotics: Ran **0 tests / 0 assertions / 0 failures**, RC=0, HEAD ad99366
- giemon: Ran **0 tests / 0 assertions / 0 failures**, RC=0, HEAD 00fd23f

## 比較 (基準: robotics 23/558/0, giemon 46/115/0)
- 両 suite とも silent-zero (0/0/0 RC=0)。bench-244〜267 から **24 連継**の既知状態。
- 根因確定済み (falsify-069: JVM require が .cljk をロード不能、falsify-073 静的再確定)。
  修復未着手。基準値実測緑の再確立はできていない → **回帰 assert はしない (honest unmeasured)**。

## seeded reproduction
- sim-loop は L0、学習ジョブ無し → not-applicable。

## regression
- silent-zero 継続は「測定不能」であり回帰 assert 対象外。テスト数自体の新規回帰は検出不能 (runner 破損中)。

## falsify status
- FK guard repair (falsify-034 起) 未着手・残存。
- governor silent-nil 負テスト (falsify-071/072 起) 未着手・残存。
- **最優先は NEXT (test-runner 修復): .cljk を戻すか loader 登録で clojure / kbb 両 runner を緑化。**
