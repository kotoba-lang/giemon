# bench-289

## Judgement: measured — silent-zero 持続 (36 連続)。runner 修復未着手につき回帰の有無は測定不能 (既知状態の再実測)。

## Load
ncpu=10, load avg (start 19:11 JST) 11.90/13.55/15.19 ≈ 1.2–1.5× → 15分平均 < 2×、gate pass。両 suite 実行。

## clojure -M:test (両 suite)
- robotics: Ran 0 tests / 0 assertions / 0 failures, 0 errors, RC=0。
- giemon: Ran 0 tests / 0 assertions / 0 failures, 0 errors, RC=0。
- bench-287 の 0/0/0 RC=0 と同値 → silent-zero 36 連続 (falsify-069 根因: JVM require が .cljk をロード不能、確定済み)。実測緑 (robotics 23/558/0・giemon 46/115/0) は依然再確立できず。

## 暫定測定経路 (kbb --backend sci)
- 本走は未実施 (clojure runner 同値確認を優先)。直近実測は falsify-070/074/075: kbb sci 経路 21/52/0 緑 (governor_test 追加なら 6 tests 増)。kbb -M:test 第2経路は bench-270 以降 RC=1 hard-fail (5 dep 未解決)。

## seeded 再現
not-applicable (sim-loop は L0、学習ジョブ無し — jobs/ runs/ 不在、bench-287 確認のまま)。

## Regression
- 両 suite 0/0/0 RC=0 の既知状態を 36 連続で再実測。基準値 (robotics 23/558/0・giemon 46/115/0) 据え置き。負の断定はしない (regression assert せず)。

## HEAD
- robotics ad99366 / giemon 41ac173 (git rev-parse 本走再確認、bench-277/278/283/286/287/288 から不変)。

## falsify status
- 変更なし。falsify-034 (FK guard repair 未実装、38 連続 refuted・未着手) 残存 — HEAD 不変につき状態変化なし。
- NEXT の test-runner 修復 (.cljk 拡張子 / kbb.edn deps floor 接続) は未着手のまま。

## 再現コマンド
```
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon && clojure -M:test
uptime; sysctl -n hw.ncpu
git -C ../robotics rev-parse HEAD; git -C ../giemon rev-parse HEAD
```
