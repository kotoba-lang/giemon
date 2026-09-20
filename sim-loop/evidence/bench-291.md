# bench-291

## Judgement: skipped (load) — unmeasured, honest

## Load
ncpu=10 (本走 `sysctl -n hw.ncpu` 実測)。本走 4 回観測 (01:06–01:08 JST):
15分平均 22.29 → 22.80 → 23.39 (2.23–2.34×)、1分平均 24.36 → 27.75 → 32.56
(2.4–3.3×)。両指標とも上昇トレンドで gate fail 継続 → 重い実験
(clojure -M:test 両 suite・暫定 kbb 経路) は一律省略。基準値据え置きで
regression assert せず。

## clojure -M:test (両 suite)
- skipped (load)。robotics / giemon とも未実行 → テスト数 unmeasured。
- 直近実測 (bench-289): 両 suite 0/0/0 RC=0 (silent-zero 36 連続、
  falsify-069 根因確定済み: JVM require が .cljk をロード不能)。

## 暫定測定経路 (kbb --backend sci)
- skipped (load)。未実施。直近実測は falsify-079: giemon 27/67/0 緑
  (意図的 fail 挿入で RC=1 実測、governor_test 6/15 初実測込み)。

## seeded 再現
not-applicable (sim-loop は L0、学習ジョブ無し — jobs/・runs/ 不在は
bench-290 で確認済み、本走で再確認せず)。

## Regression
- 計測せず (load skip)。基準値 (robotics 23/558/0・giemon 46/115/0、
  暫定 kbb 経路 giemon 27/67/0) 据え置き、回帰の有無は不明 (unmeasured)。

## HEAD
- robotics ad99366 / giemon 41ac173f8e9dc599e8b9ab340a51f4135d5ade98
  (本走 git rev-parse で再確認、bench-277 以降から不変)。

## falsify status
- 変更なし。falsify-034 (FK guard repair 未実装) 残存 — HEAD 不変につき
  状態変化なし。runner 修復後の再検証待ち。
- falsify-079 までの記録は現状維持。

## 再現コマンド (load 回復後)
```
cd orgs/kotoba-lang/robotics && clojure -M:test   # 期待: 現状 silent-zero 0/0/0 RC=0
cd orgs/kotoba-lang/giemon && clojure -M:test     # 期待: 現状 silent-zero 0/0/0 RC=0
uptime; sysctl -n hw.ncpu
```

## NEXT (変わらず最優先)
test-runner 修復: clojure / kbb 両 runner 緑化 (.cljk loader 登録 or
拡張子復帰)。kbb -M:test 復活には nbb.edn へ deps floor 接続。
コード変更: なし (本 bot は実装しない)。
