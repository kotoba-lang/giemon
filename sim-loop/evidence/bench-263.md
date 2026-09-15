# bench-263

- 日時: 2026-09-15 (JST), 決定的記録
- 負荷: load 15min 12.42 / ncpu 10 ≈ 1.2x → 測定実行 (skip なし)
- HEAD: robotics ad99366bc7bef949e86ee33b7e04d12525dffe46 / giemon 00fd23f9d04743323047c8c29c30aa18320daa70 (前回比 不変)

## 判定: measured (実測完走)

| suite | tests / assertions / failures | RC |
|---|---|---|
| robotics | 0 / 0 / 0 | 0 |
| giemon | 0 / 0 / 0 | 0 |

## 回帰

- 両 suite とも **silent-zero 持続** (kbb -M:test が 0/0/0 RC=0 で緑と見える)。bench-244〜262 で 18 連続観測済みの既知状態で、263 でも同一 → **回帰の増加なし / 修復なし**。基準値 robotics 23/558/0・giemon 46/115/0 との一致は**未検証** (runner が test をロードできていないため比較不能)。
- 根因は falsify-069 確定済み: JVM require が .cljk をロード不能。test 拡張子を戻すか loader 登録するまで clojure/kbb 両 runner の実測緑は再確立できない。
- bench-262 の kbb 第2経路 21/52/0 緑は本走では再実行せず (本 bench は kbb -M:test 実測のみ)。NEXT に従い runner 修復が最優先。

## seeded 再現

- not-applicable (sim-loop は L0、学習ジョブ無し)

## 再現コマンド

```
bash /tmp/bench263.sh
# cd orgs/kotoba-lang/robotics && kbb -M:test > /tmp/b_rob.txt 2>&1
# cd orgs/kotoba-lang/giemon   && kbb -M:test > /tmp/b_gie.txt 2>&1
```

## falsify 状態

- 変更なし。falsify-034 (FK guard repair 未実装) 残存 31+ 連続 refuted。falsify-069 (JVM .cljk ロード不能) 持続観測。

## コード変更

- なし (bot は測定・記録のみ)
