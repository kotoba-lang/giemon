# bench-164 — giemon sim-loop ベンチ (決定的・タイムスタンプなし)

judgement: **unmeasured** (load skip — pre-run 15min 63.30 / 実行時 15min 65.40 ≈ 6.5x ncpu=10、2x gate 大幅超過)
load: 1min 103.38 / 5min 86.16 / 15min 65.40, ncpu=10 (uptime 14:49)
host: macOS, 8 users

## テスト
- 未実行 (load gate skip)。15-min load 65.40 は 2×ncpu=20 を大きく上回り、重い
  test スイートの実測を省略。honest に `unmeasured` と記録し、回帰は assert しない
  (基準値据え置き — bench-163/162/161/160 と同方針)。1min 103.38 / 5min 86.16 で
  負荷は高止まり、実行バックエンド応答不能リスク大。

## 再現ベンチ
- seeded repro: not-applicable (sim-loop は L0、学習ジョブ無)

## 回帰
- 基準値 (robotics 14/50/0、giemon 46/115/0) に対し本 walk は unmeasured のため
  regression assert なし。git HEAD 2 点とも変化なし (robotics 9459ca0、giemon d0d3cb4
  = 基準値と同一)。git status: giemon は `?? sim-loop/` 未追跡のみ、tracked 変更なし
  → コード変更なし。

## falsify
- falsify-001〜047 は総て存在し、最新 falsify-047 も静的読取で refuted 済み
  (FK guard repair 未着手、`within-limits?` は FK 内呼出 0 回)。残存 pending なし、
  新規 falsify なし。git diff 空 (tracked 変更なし) のため本 walk の新決着なし。

## 再現コマンド
```
# load gate (15min ≥ 2x ncpu) 超過のため本 walk は未実行。基準時 (bench-066 確定):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test   # 14/50/0
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && clojure -M:test   # 46/115/0
```
コード変更なし。

## 補足 (cleanup 副作用の正直記録)
- 本 walk は実測 run なしのため新規 stray probe 掃除は行わなかった (bench-160 の
  誤削除 lesson に従い、削除 0)。参照 probe (posture_family_seed / seed_parity_postures /
  within_limits_missing / within_limits_no_caller / parity_arm6) は全て intact 確認済。
- `?? sim-loop/` のみ未追跡。VCS 復元不能領域のまま。