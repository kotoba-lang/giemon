# bench-259

- date: 2026-09-15 (JST), cron
- judgement: measured — silent-zero 持続 (bench-244 起の既知状態、変化なし)
- host load: 1m 15.29 / 15m 14.05, ncpu=10 (~1.4x) → 2x gate 未満、通常実施
- git HEAD: robotics `ad99366bc7bef949e86ee33b7e04d12525dffe46`, giemon `00fd23f9d04743323047c8c29c30aa18320daa70` (bench-257/258 と同一)

## テスト実行 (`kbb -M:test`, /tmp/bench259.sh で cd 固定)

- robotics: `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0
- giemon:   `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0

両 suite とも silent-zero (0/0/0 RC=0)。根因確定済 (falsify-069: JVM require が
.cljk をロード不能)。runner 修復待ち — 基準値 robotics 23/558/0・giemon 46/115/0 の
実測緑は現 HEAD で再現できず (既知回帰、新規赤の追加はなし)。

## seeded 再現

- not-applicable (sim-loop は L0, 学習ジョブ無し)

## 回帰

- regression assert: なし (silent-zero は bench-244 起の既知状態、持続観測のみ)
- NEXT 項目 (test-runner 修復 / governor rejected レコード化+負テスト / FK guard repair
  falsify-034 残存) は未着手を確認。変化なし。

## 再現コマンド

```
bash /tmp/bench259.sh
# cd robotics && kbb -M:test > /tmp/b259_rob.txt; cd giemon && kbb -M:test > /tmp/b259_gie.txt
```

生出力: /tmp/b259_rob.txt, /tmp/b259_gie.txt (RC=0 both)、状態 /tmp/b259_status.txt。
no code change.
