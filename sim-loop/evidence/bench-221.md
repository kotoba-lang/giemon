# bench-221 (giemon sim-loop bench)

## Load gate
uptime 11:05–11:06, load averages: 45.87–49.86 / 53.42–54.56 / 70.95–73.29, hw.ncpu = 10
→ 15-min load ~7.1x ncpu。負荷ゲート (~2x) を大幅超過。
→ clojure -M:test (robotics/giemon 両方) と seeded 再現実行は省略: skipped (load)。

## Test suites
- robotics: skipped (load) — unmeasured
- giemon: skipped (load) — unmeasured

## Git HEADs
- giemon: d0d3cb4 (baseline と一致, untracked `?? sim-loop/` のみ本回再確認)
- robotics: 396fc33 — baseline 記載の 9459ca0 から変化のまま (bench-219/220 記録と同一)。
  テスト未実行のため数値の変化は未確認 (unmeasured)。次回負荷低下時に
  robotics 基準値 14/50/0 の再確認が必須。

## Seeded reproduction
skipped (load) — not applicable (sim-loop L0, 学習ジョブ無し)

## Regression
regression unknown (unmeasured — 断定せず)。honest 記録: 本回はテスト数 / assertion 数の本測定無し。
基準値 (robotics 14/50/0, giemon 46/115/0) は据え置き・変更無し。

## Falsify status
falsify-034 (FK guard repair 未実装) 残存。falsify-060〜062 まで記録済み、新規反証は本回無し。

## Reproduction commands
```
uptime                      # 11:06, load averages: 49.86 53.42 70.95; sysctl -n hw.ncpu → 10
cd orgs/kotoba-lang/robotics && clojure -M:test   # skipped (load)
cd orgs/kotoba-lang/giemon && clojure -M:test     # skipped (load)
```

コード変更: 無し。
