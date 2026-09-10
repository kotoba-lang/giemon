# bench-219 (giemon sim-loop bench)

## Load gate
uptime 15-min load 111.03–111.39, hw.ncpu = 10 → ~11x ncpu。負荷ゲート (~2x) を大幅超過。
→ clojure -M:test (robotics/giemon 両方) と seeded 再現実行は省略: skipped (load)。

## Test suites
- robotics: skipped (load) — unmeasured
- giemon: skipped (load) — unmeasured

## Git HEADs
- giemon: d0d3cb4 (baseline と一致, untracked `?? sim-loop/` のみ)
- robotics: 396fc33 — **baseline 記載の 9459ca0 から変化**。テスト未実行のため
  数値の変化は未確認 (unmeasured)。次回負荷低下時に robotics 基準値 14/50/0 の再確認が必須。

## Seeded reproduction
skipped (load) — not applicable (sim-loop L0, 学習ジョブ無し)

## Regression
regression unknown (unmeasured — 断定せず)。honest 記録: テスト数 / assertion 数は本測定無し。
基準値 (robotics 14/50/0, giemon 46/115/0) は据え置き・変更無し。

## Falsify status
falsify-034 (FK guard repair 未実装) 残存。falsify-060〜062 まで記録済み、新規反証は本回無し。

## Reproduction commands
```
uptime                      # 10:39, load averages: 113.92 120.88 111.03; sysctl -n hw.ncpu → 10
cd orgs/kotoba-lang/robotics && clojure -M:test   # skipped (load)
cd orgs/kotoba-lang/giemon && clojure -M:test     # skipped (load)
```

コード変更: 無し。
