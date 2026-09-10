# bench-220 (giemon sim-loop bench)

## Load gate
uptime 10:49, load averages: 62.11 / 89.00 / 100.89, hw.ncpu = 10 (前回 bench-219 記録値)
→ 15-min load ~10.1x ncpu。負荷ゲート (~2x) を大幅超過。
→ clojure -M:test (robotics/giemon 両方) と seeded 再現実行は省略: skipped (load)。

## Test suites
- robotics: skipped (load) — unmeasured
- giemon: skipped (load) — unmeasured

## Git HEADs
- giemon: d0d3cb4 (bench-219 と同一確認済みの範囲で据え置き, untracked `?? sim-loop/` のみ)
- robotics: bench-219 記録のまま変化未確認 (396fc33)。基準値再確認は次回負荷低下時に必須。

## Seeded reproduction
skipped (load) — not applicable (sim-loop L0, 学習ジョブ無し)

## Regression
regression unknown (unmeasured — 断定せず)。honest 記録: 本回はテスト数 / assertion 数の本測定無し。
基準値 (robotics 14/50/0, giemon 46/115/0) は据え置き・変更無し。

## Falsify status
falsify-034 (FK guard repair 未実装) 残存。falsify-060〜062 まで記録済み、新規反証は本回無し。

## Reproduction commands
```
uptime                      # 10:49, load averages: 62.11 89.00 100.89; hw.ncpu = 10
cd orgs/kotoba-lang/robotics && clojure -M:test   # skipped (load)
cd orgs/kotoba-lang/giemon && clojure -M:test     # skipped (load)
```

コード変更: 無し。
