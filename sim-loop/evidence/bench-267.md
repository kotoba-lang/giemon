# bench-267

- 日時: 2026-09-16 (JST), 決定的記録
- 負荷: 実測開始時 load 15min 19.43 / ncpu 10 ≈ 1.9x (1min 15.98)。bench-265/266 と
  同一判断 (silent-zero 継続確認は軽量、各 runner 数秒) で実測を実行。
- HEAD: robotics ad99366bc7bef949e86ee33b7e04d12525dffe46 / giemon 00fd23f9d04743323047c8c29c30aa18320daa70 (bench-264〜266 と同一、不変)

## 判定: measured (実測完走)

| suite | tests / assertions / failures | RC |
|---|---|---|
| robotics | 0 / 0 / 0 | 0 |
| giemon | 0 / 0 / 0 | 0 |

## 回帰

- 両 suite とも **silent-zero 持続** (kbb -M:test が 0/0/0 RC=0 で緑と見える)。
  bench-244〜266 で観測済みの既知状態で、267 でも同一 → **回帰の増加なし / 修復なし**
  (23 連続目)。基準値 robotics 23/558/0・giemon 46/115/0 との一致は **未達**
  (runner が test をロードできていないため比較不能)。
- 根因は falsify-069 確定済み: JVM require が .cljk をロード不能。test 拡張子を戻すか
  loader 登録するまで clojure/kbb 両 runner の実測緑は再確立できない。NEXT の最優先
  修理項目のまま、本走でも bot はコード修正を行わない。

## seeded 再現

- not-applicable (sim-loop は L0、学習ジョブ無し。bench-266 と同一前提)

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon   && kbb -M:test
# 本走の出力: /tmp/b_rob_test.txt /tmp/b_gie_test.txt (両 suite とも
# "Ran 0 tests containing 0 assertions. / 0 failures, 0 errors." RC=0)
# runner: bash /tmp/bench_run.sh (明示 cd で robotics→giemon の順に実行)
```

## falsify 状態

- 変更なし。falsify-034 (FK guard repair 未実装) 残存。falsify-069 (JVM .cljk
  ロード不能) による runner silent-zero は bench-267 でも持続観測 (23 連続目)。

## コード変更

- なし (bot は測定・記録のみ)
