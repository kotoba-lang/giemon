# bench-280 — robotics measured (silent-zero 持続) / giemon unmeasured

## 判定: 部分実測 (robotics) + unmeasured (giemon)

- 走開始時 load: 8.56 / 10.95 / 14.02 (1/5/15-min), hw.ncpu = 10 → 15-min 14.02 < 20 でゲート通過し実測開始。
- robotics `clojure -M:test` @ HEAD ad99366: **0 tests / 0 assertions / 0 failures, RC=0** — silent-zero 持続実測 (bench-244〜276 の持続記録と同一状態、10 連続目の実測再確認)。
- giemon `clojure -M:test` @ HEAD 41ac173: ヘッダ (git rev-parse) は取得済み。テスト実行は走時予算切れで未完 → **unmeasured** (honest)。結果は書き込まれず、失敗として assert しない。
- 基準値据え置き: robotics 23/558/0・giemon 46/115/0。本走の 0/0/0 は runner 既知不調 (silent-zero) であり回帰 assert せず。

## seeded 再現

- 対象なし (L1 seeded ジョブは本走で実行せず — giemon suite 未完につき)。

## 状態

- HEAD 実測再読: robotics ad99366・giemon 41ac173 (bench-275〜278 記録と不変)。
- silent-zero 持続 (clojure runner 0/0/0 RC=0) は robotics 側で再実測。kbb 経路は本走未実行。
- NEXT 優先度変更なし: test-runner 修復 (cljk rename 後 silent-zero 解消) が全 bench/falsify の前提。
- falsify 状況変更なし (falsify-076 (H77) refuted が最新、FK guard repair 33 連続 refuted 未着手)。

## 再現コマンド

```
uptime   # 15-min load < 2× sysctl -n hw.ncpu (=20) を確認 (本走開始時: 8.56/10.95/14.02, ncpu=10)
cd <robotics> && git rev-parse --short HEAD && clojure -M:test   # 0/0/0 RC=0 (silent-zero)
cd <giemon> && git rev-parse --short HEAD && clojure -M:test     # 本走未完 (budget)
```

## 回帰: 無判定 (robotics silent-zero は既知・据え置き / giemon unmeasured)

- コード変更: なし。
