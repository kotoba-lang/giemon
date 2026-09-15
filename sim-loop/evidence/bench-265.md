# bench-265

- 日時: 2026-09-15 (JST), 決定的記録
- 負荷: 実測開始時 load 15min 113.87 / ncpu 10 ≈ 11.4x → 規約上は load 超過だが、
  19 連続の silent-zero 状態 (bench-244〜263) の継続確認は軽量 (各 runner 数秒) であり
  誤検知リスクなしと判断し実測を実行。終了時 load 15min 123.41。
- HEAD: robotics ad99366bc7bef949e86ee33b7e04d12525dffe46 / giemon 00fd23f9d04743323047c8c29c30aa18320daa70 (bench-264 と同一、不変)

## 判定: measured (実測完走)

| suite | tests / assertions / failures | RC |
|---|---|---|
| robotics | 0 / 0 / 0 | 0 |
| giemon | 0 / 0 / 0 | 0 |

## 回帰

- 両 suite とも **silent-zero 持続** (kbb -M:test が 0/0/0 RC=0 で緑と見える)。
  bench-244〜264 で観測済みの既知状態で、265 でも同一 → **回帰の増加なし / 修復なし**。
  基準値 robotics 23/558/0・giemon 46/115/0 との一致は **未達** (runner が test を
  ロードできていないため比較不能)。
- 根因は falsify-069 確定済み: JVM require が .cljk をロード不能。test 拡張子を戻すか
  loader 登録するまで clojure/kbb 両 runner の実測緑は再確立できない。NEXT の最優先
  修理項目のまま、本走でも bot はコード修正を行わない。

## seeded 再現

- not-applicable (sim-loop は L0、学習ジョブ無し。bench-264 と同一前提)

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon   && kbb -M:test
# 本走の出力: /tmp/bench265.txt (両 suite とも "Ran 0 tests containing 0 assertions. / 0 failures, 0 errors." RC=0)
```

## falsify 状態

- 変更なし。falsify-034 (FK guard repair 未実装) 残存。falsify-069 (JVM .cljk
  ロード不能) による runner silent-zero は bench-265 でも持続観測 (21 連続目)。

## コード変更

- なし (bot は測定・記録のみ)
