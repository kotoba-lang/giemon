# bench-248

- date: 2026-09-13 (JST), cron
- host load: 10.72 / 13.32 / 14.20 (ncpu=10) — 15-min ≈ 1.4x ncpu, gate under → 実行した
- git HEAD: robotics `ad99366bc7bef949e86ee33b7e04d12525dffe46`, giemon `00fd23f9d04743323047c8c29c30aa18320daa70`
  (bench-247 と同一 HEAD、baseline 記載値からは進んだまま)

## テスト実行 (`kbb -M:test`, /tmp/benchrun.sh で cd 固定)

- robotics: `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0
- giemon:   `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0

## judgement: **measured but ANOMALY — 0 tests (bench-247 と同一症状)**

両スイートとも 0 tests。bench-247 の 0-test anomaly が再現 (2 連続)。RC=0 だが
suite 未実行と同等であり green とは扱わない。本 bot はコードを修正しないため
実装側の調査はしない (deps.edn / test dir 構成の変化疑い)。

- regression 判定: **assert しない (baseline 据え置き)** — 0-test を回帰とは断定しない
- seeded 再現: not-applicable (sim-loop は L0, 学習ジョブなし)
- falsify status: falsify-034 残存 (FK guard repair 未実装のまま) — 変更なし

## 再現コマンド

```
bash /tmp/benchrun.sh   # cd robotics && kbb -M:test > /tmp/b_rob.txt; cd giemon && kbb -M:test > /tmp/b_gie.txt
```

生出力: /tmp/b_rob.txt, /tmp/b_gie.txt (RC=0 both)。
no code change.
