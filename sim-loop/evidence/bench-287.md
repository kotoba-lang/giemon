# bench-287

## Judgement: measured (load gate pass)

## Load
ncpu=10, load avg (start) 7.94/10.20/11.09、実測完了時 13:05 時点 15分平均 11.09 ≈ 1.1× → 2× 未満、gate pass。重い実験は省略せず完走。

## clojure -M:test (両 suite)
- robotics @ ad99366 (HEAD 不変): `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0
- giemon @ 41ac173 (HEAD 不変): `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0
- **silent-zero 35 連続目 (bench-244〜287 の実測連続)**。cljk rename 起・falsify-069 確定
  (JVM require が .cljk をロード不能)。テスト数は基準値 (robotics 23/558/0・giemon 46/115/0)
  と比較不能 → regression 判定は assert せず基準値据え置き、honest。

## 暫定測定経路 (kbb --backend sci --classpath src:test + 明示 require 4 ns)
- arm-test / chassis-test / kinematics-test / viewer-test: **21 tests / 52 assertions /
  0 failures, 0 errors, RC=0** — bench-262/270/276/282/283/284/285/286 実績 21/52/0 と一致。
  HEAD 41ac173 生存。kbb -M:test 第2経路の RC=1 hard-fail 状態は本走では再実施せず
  (bench-276 測定のまま: deps floor 未接続)。

## seeded 再現
not-applicable (sim-loop は L0、学習ジョブ無し — jobs/ runs/ ディレクトリ不在を本走で再確認)。

## Regression
- 回帰差分は計測不能 (clojure runner silent-zero のためテスト数が 0)。基準値据え置き。
- 暫定経路 21/52/0 は前回同値 → 暫定経路上の回帰なし。

## falsify status
- falsify-034 (H35, FK guard repair 未実装) 残存: bench-286 記録 37 連続 refuted・未着手から
  本走も変化なし (HEAD 不変につき状態変化の可能性なし) → 38 連続目。runner 修復後の再検証待ち。
- 変更なし。falsify-078 までの記録は現状維持。

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
