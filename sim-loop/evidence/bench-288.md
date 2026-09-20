# bench-288

## Judgement: skipped (load) — unmeasured, honest

## Load
ncpu=10, load avg (start 16:08 JST) 21.73/29.28/40.60 ≈ 2.2–4.1× → 15分平均 4.06× ≫ 2×、gate fail。
重い実験 (clojure -M:test 両 suite・暫定 kbb 経路) は省略。基準値据え置きで regression assert せず。

## clojure -M:test (両 suite)
- skipped (load)。robotics / giemon とも未実行 → テスト数 unmeasured。
- 直近実測 (bench-287): 両 suite 0/0/0 RC=0 (silent-zero 35 連続、falsify-069 根因確定済み)。

## 暫定測定経路 (kbb --backend sci)
- skipped (load)。未実施。

## seeded 再現
not-applicable (sim-loop は L0、学習ジョブ無し — bench-287 で jobs/ runs/ 不在確認済み)。

## Regression
- 計測せず (load skip)。基準値 (robotics 23/558/0・giemon 46/115/0) 据え置き、回帰の有无は不明 (unmeasured)。

## HEAD
- robotics ad99366 / giemon 41ac173 (bench-277/278/283/286/287 から不変、本走 git rev-parse で再確認)。

## falsify status
- 変更なし。falsify-034 (FK guard repair 未実装、38 連続 refuted・未着手) 残存のまま — HEAD 不変につき状態変化なし。 runner 修復後の再検証待ち。
- falsify-078 までの記録は現状維持。

## 再現コマンド (load 回復後)
```
cd orgs/kotoba-lang/robotics && clojure -M:test   # 期待: 現状 silent-zero 0/0/0 RC=0
cd orgs/kotoba-lang/giemon && clojure -M:test     # 期待: 現状 silent-zero 0/0/0 RC=0
kbb --backend sci --classpath src:test -e "(require '[clojure.test :as t] 'kotoba.giemon.arm-test 'kotoba.giemon.chassis-test 'kotoba.giemon.kinematics-test 'kotoba.giemon.viewer-test)(apply t/run-tests (map find-ns '[kotoba.giemon.arm-test kotoba.giemon.chassis-test kotoba.giemon.kinematics-test kotoba.giemon.viewer-test]))"   # 期待: 21/52/0 RC=0
```

## NEXT (変わらず最優先)
test-runner 修復: clojure / kbb 両 runner 緑化 (.cljk loader 登録 or 拡張子復帰)。kbb -M:test
復活には nbb.edn へ deps floor 接続。コード変更: なし (本 bot は実装しない)。
