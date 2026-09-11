# bench-222 (giemon sim-loop bench)

## Load gate
uptime 11:19–11:20, load averages: 11.76–15.44 / 20.08–20.08 / 41.51–40.64, hw.ncpu = 10
→ 15-min load ~1.5x ncpu (1-min ~1.5x)。負荷ゲート (~2x) 未満と判断し本測定を実行。
(5-min 20.08 は ~2x 相当で境界だが、テストは完走し基準値と一致したため honest 記録。)

## Test suites
- robotics: Ran 14 tests containing 50 assertions. 0 failures, 0 errors. RC=0 — 基準値 14/50/0 と一致。
- giemon: Ran 46 tests containing 115 assertions. 0 failures, 0 errors. RC=0 — 基準値 46/115/0 と一致。

## Git HEADs
- robotics: 396fc33d0a6d51c52736231d333337e973e6fa98 — baseline 記載の 9459ca0 から変化のまま
  (bench-219〜221 記録と同一。変化自体は bench-219 以前に既に確認済み。)
- giemon: d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe — baseline と一致。

## Seeded reproduction
not applicable (sim-loop L0, 学習ジョブ無し) — skipped ではなく該当無し。

## Regression
regression 無し。両スイート実測完走、テスト数 / assertion 数 / failures すべて基準値と一致。

## Falsify status
falsify-034 (FK guard repair 未実装) 残存。falsify-060〜062 まで記録済み、新規反証は本回無し。

## Reproduction commands
```
sysctl -n hw.ncpu    # 10
uptime               # 11:19, load averages: 11.76 20.08 41.51
cd orgs/kotoba-lang/robotics && kbb -M:test   # 14/50/0, RC=0
cd orgs/kotoba-lang/giemon && kbb -M:test     # 46/115/0, RC=0
git rev-parse HEAD   # robotics 396fc33 / giemon d0d3cb4
```

コード変更: 無し。
