# bench-282

## Judgement: measured (load gate pass)

## Load
ncpu=10, load avg (start) 11.56/12.49/13.75 ≈ 1.2× → 2× 以下、gate pass。
終了時 12.41/12.62/13.70 ≈ 1.2–1.4×。

## clojure -M:test (両 suite)
- robotics @ ad99366bc7bef949e86ee33b7e04d12525dffe46: `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0
- giemon @ 41ac173f8e9dc599e8b9ab340a51f4135d5ade98: `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0
- **silent-zero 30 連続目 (bench-244〜282。bench-271〜274/277/278 は skip のため実測換算では
  bench-275/276/278 の 28/29 連続実測に本走が 1 加算)**。cljk rename 起・falsify-069 確定
  (JVM require が .cljk をロード不能)。テスト数は基準値 (robotics 23/558/0・giemon 46/115/0)
  と比較不能 → regression 判定は assert せず基準値据え置き、honest。
- HEAD 両者 bench-275/276/277 記録値から不変。

## 暫定測定経路 (kbb --backend sci --classpath src:test + 明示 require 4 ns)
- arm-test / chassis-test / kinematics-test / viewer-test: **21 tests / 52 assertions /
  0 failures, 0 errors, RC=0** — bench-262/270/276 実績 21/52/0 と一致。HEAD 41ac173 生存。
- 拡張試行は本走では未実施 (bench-276 測定のまま: 全 10 ns は sci 下 `catch Exception` 未解決、
  8 ns は kotoba.lang.text 未解決・deps floor 未接続)。

## seeded 再現
not-applicable (sim-loop は L0、学習ジョブ無し)。

## Regression
- 回帰差分は計測不能 (clojure runner silent-zero のためテスト数が 0)。基準値据え置き。
- 暫定経路 21/52/0 は前回同値 → 暫定経路上の回帰なし。

## falsify status
- falsify-034 (H35, FK guard repair 未実装) 残存: 33 連続 refuted・未着手。runner 修復後の再検証待ち。
- 変更なし。falsify-076 までの記録は現状維持。

## 再現コマンド
```
cd orgs/kotoba-lang/robotics && clojure -M:test   # → 0/0/0 RC=0 (silent-zero)
cd orgs/kotoba-lang/giemon && clojure -M:test     # → 0/0/0 RC=0 (silent-zero)
kbb --backend sci --classpath src:test -e "(require '[clojure.test :as t] 'kotoba.giemon.arm-test 'kotoba.giemon.chassis-test 'kotoba.giemon.kinematics-test 'kotoba.giemon.viewer-test)(apply t/run-tests (map find-ns '[kotoba.giemon.arm-test kotoba.giemon.chassis-test kotoba.giemon.kinematics-test kotoba.giemon.viewer-test]))"   # → 21/52/0 RC=0
```

## NEXT (変わらず最優先)
test-runner 修復: clojure / kbb 両 runner 緑化 (.cljk loader 登録 or 拡張子復帰)。kbb -M:test
復活には nbb.edn へ deps floor 接続。暫定経路は 4 ns のみ (21/52 は 46/115 の部分集合)。
コード変更: なし。
