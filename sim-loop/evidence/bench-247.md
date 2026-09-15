# bench-247

- date: 2026-09-13 (JST), cron
- host load: 10.50 / 10.56 / 10.69 (ncpu=10) — 15-min ≈ 1.0–1.1x ncpu, under gate → 実行した
- git HEAD: robotics `ad99366bc7bef949e86ee33b7e04d12525dffe46`, giemon `00fd23f9d04743323047c8c29c30aa18320daa70`
  (baseline skill 記載 robotics 893ef76 / giemon d0d3cb4 から **双方 HEAD が進んでいる**)

## テスト実行 (`kbb -M:test`, /tmp/run.sh で cd 固定)

- robotics: `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0
- giemon:   `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0

## judgement: **measured but ANOMALY — 0 tests**

両スイートとも test が 0 件。baseline (robotics 23/558/0, giemon 46/115/0) と比較して
テスト数が完全に 0 であり、RC=0 で「緑」に見えるが実質テストが走っていない。
考えられる原因: HEAD 前進により test runner / test dir 構成が変わり
`Running tests in #{"test"}` が空になった (deptest の取りこぼし等)。
本 bot はコードを修正しないため実装側の調査はしない。

- regression 判定: **assert しない (baseline 据え置き)** — 0-test は green ではなく
  suite 未実行と同等。回帰とは断定しないが、anomaly として記録。
- seeded 再現: not-applicable (sim-loop は L0, 学習ジョブなし)
- falsify status: falsify-034 残存 (FK guard repair 未実装のまま) — 変更なし

## 再現コマンド

```
bash /tmp/run.sh   # cd robotics && kbb -M:test > /tmp/b_rob.txt; cd giemon && kbb -M:test > /tmp/b_gie.txt
```

生出力: /tmp/b_rob.txt, /tmp/b_gie.txt (RC=0 both)。
no code change.
