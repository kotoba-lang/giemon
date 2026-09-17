# bench-278 — skipped (load 超過 + 実行 backend 応答不能)

## 判定: unmeasured (skipped — HOST LOAD / backend)

- 15-min load average: ≈95.32 (1-min 107.12, 実測 uptime 107.12/95.32/58.53)。hw.ncpu = 10。
- gate: 15-min ≥ 2× ncpu (= 20) → ≈95 ≈ 9.5× ncpu で大幅超過。
- さらに terminal 実行 backend が全コマンド空出力 (bench-225/226/227 と同一症状) で
  clojure -M:test 両 suite / kbb -M:test / kbb sci 暫定経路 / seeded 再現は実施不能 → unmeasured (honest)。
- 基準値据え置き: robotics 23/558/0・giemon 46/115/0。回帰 assert せず。

## 状態

- HEAD: 実行 backend 応答不能につき本走で未再読 — bench-275/276/277 記録
  (robotics ad99366 / giemon 41ac173) を据え置き (変移は否定も肯定もしない)。
- silent-zero 持続の有無は本走未測定 (bench-244〜276 の実測記録に変更なし、
  bench-271〜274/277 に続く load/backend skip)。
- 新規 falsify: falsify-076 (H77) refuted — FK guard repair 未配線・governor 負テスト 0 件を
  現 blob 直読で再確定 (33 連続 refuted)。arm.cljk L38 silent zero-fill 不変。

## 再現コマンド

```
uptime   # 15-min load ≥ 2× sysctl -n hw.ncpu を確認 (本走: 107.12/95.32/58.53)
```

## 回帰: 無判定 (unmeasured)

- コード変更: なし。
