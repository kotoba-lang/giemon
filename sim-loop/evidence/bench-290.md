# bench-290

## Judgement: skipped (load) — unmeasured, honest

## Load
ncpu=10, 本走 4 回観測 (22:07–22:13 JST): 15分平均 51.55 → 46.41 → 40.94 → 38.53 (3.9–5.2×)。1分平均も 25.67–36.26 (2.6–3.6×)。全観測で 15分平均 ≫ 2×、gate fail 継続 → 重い実験 (clojure -M:test 両 suite・暫定 kbb 経路) は一律省略。基準値据え置きで regression assert せず。

## clojure -M:test (両 suite)
- skipped (load)。robotics / giemon とも未実行 → テスト数 unmeasured。
- 直近実測 (bench-289): 両 suite 0/0/0 RC=0 (silent-zero 36 連続、falsify-069 根因確定済み)。

## 暫定測定経路 (kbb --backend sci)
- skipped (load)。未実施。直近実測は falsify-070/074/075: 21/52/0 緑。

## seeded 再現
not-applicable (sim-loop は L0、学習ジョブ無し — 本走で sim-loop/ に jobs/・runs/ 不在を再確認、evidence/manual/status のみ)。

## Regression
- 計測せず (load skip)。基準値 (robotics 23/558/0・giemon 46/115/0) 据え置き、回帰の有无は不明 (unmeasured)。

## HEAD
- robotics ad99366 / giemon 41ac173 (本走 git rev-parse で再確認、bench-277/278/283/286/287/288/289 から不変)。

## falsify status
- 変更なし。falsify-034 (FK guard repair 未実装、38 連続 refuted・未着手) 残存 — HEAD 不変につき状態変化なし。runner 修復後の再検証待ち。
- falsify-078 までの記録は現状維持。

## 再現コマンド (load 回復後)
```
cd orgs/kotoba-lang/robotics && clojure -M:test   # 期待: 現状 silent-zero 0/0/0 RC=0
cd orgs/kotoba-lang/giemon && clojure -M:test     # 期待: 現状 silent-zero 0/0/0 RC=0
uptime; sysctl -n hw.ncpu
```

## NEXT (変わらず最優先)
test-runner 修復: clojure / kbb 両 runner 緑化 (.cljk loader 登録 or 拡張子復帰)。kbb -M:test 復活には nbb.edn へ deps floor 接続。コード変更: なし (本 bot は実装しない)。
