# bench-224 (giemon sim-loop bench)

## Load gate
uptime 11:51, load averages: 7.45 / 15.62 / 26.92, hw.ncpu = 10
→ 15-min load ≈ 2.7x ncpu (1-min 0.7x, 5-min 1.6x)。15-min がゲート (~2x ncpu) を
超過するため重い test 実行を省略 (skipped (load))。bench-223 と同様の負荷帯。

## Test suites
- clojure -M:test (robotics / giemon): **unmeasured — skipped (load)**。
  実行を省略し基準値据え置き (robotics 14/50/0、giemon 46/115/0)。
  回帰は assert しない (honest unmeasured)。前回実測は bench-222 (基準値一致)。

## Seeded reproduction
not applicable / unmeasured — sim-loop L0 (学習ジョブ無し) に加え本回は負荷超過で
再現実行自体も省略。verdict: skipped (load)。

## Regression
none asserted (unmeasured run)。コード変更なし (in-flight は `?? sim-loop/` のみ、
falsify-063 の git status 観察と同一)。

## Falsify status
falsify-034〜063 記録済み。直近 falsify-063 (H64): FK guard repair 未配線、
refuted (25 連続)。本回は新規反証を実施せず (負荷ゲート超過のため重い検証省略、
静的読取系の反証も担当外の新仮説なし)。

## Reproduction commands
```
sysctl -n hw.ncpu    # 10
uptime               # 11:51, load averages: 7.45 15.62 26.92
# gate: 15-min load >= 2x ncpu → test 実行 skip (本回不発)
```

## 決定性
本記録は決定的・タイムスタンプなし (JST 日付は cron 由来の run 識別のみ)。
