# bench-162 — giemon sim-loop ベンチ (決定的・タイムスタンプなし)

judgement: **unmeasured** (load skip — 15min 33.15 ≈ 3.3x ncpu=10、2x gate 超過)
load: 1min 18.78 / 5min 26.63 / 15min 33.15, ncpu=10 (uptime 14:20)
host: macOS, 10 users

## テスト
- 未実行 (load gate skip)。15-min load 33.15 は 2×ncpu=20 を上回り、重い
  test スイートの実測を省略。honest に `unmeasured` と記録し、回帰は assert しない
  (基準値据え置き — bench-161/160/159 と同方針)。5min 26.63 / 1min 18.78 で負荷は
  高止まり、実行バックエンド応答不能リスク大。

## 再現ベンチ
- seeded repro: not-applicable (sim-loop は L0、学習ジョブ無)

## 回帰
- 基準値 (robotics 14/50/0、giemon 46/115/0) に対し本 walk は unmeasured のため
  regression assert なし。git HEAD 2 点とも変化なし (robotics 9459ca0、giemon d0d3cb4
  = 基準値と同一)。git status: giemon は `?? sim-loop/` 未追跡のみ (前回と同構成)、
  tracked 変更なし → コード変更なし。

## falsify
- falsify-034〜046 は全て refuted 済み、残存 pending なし。新規 falsify なし。
  git diff 空 (tracked 変更なし) のため新決着なし。

## 再現コマンド
```
# load gate (15min ≥ 2x ncpu) 超過のため本 walk は未実行。基準時 (bench-066 確定):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test   # 14/50/0
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && clojure -M:test   # 46/115/0
```
コード変更なし。

## 補足 (cleanup 副作用の正直記録)
- 本 walk は実測 run なしのため新規 stray probe 掃除は行わなかった (bench-160 の
  誤削除 lesson に従い、参照確認の必要なし = 削除 0)。既知の参照 probe
  (posture_family_seed / seed_parity_postures / within_limits_missing /
  within_limits_no_caller / parity_arm6) は bench/falsify md により参照され intact。
- bench-161 記録時点と同構成の `?? sim-loop/` のみ未追跡。VCS 復元不能領域のまま。