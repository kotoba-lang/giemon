# bench-159 — giemon sim-loop ベンチ (決定的・タイムスタンプなし)

judgement: **unmeasured** (load skip — 15min 92.87 ≈ 9.29x ncpu=10、2x gate 大幅超過)
load: 1min 125.91 / 5min 118.36 / 15min 92.87, ncpu=10 (uptime 13:35)
host: macOS, 9 users

## テスト
- 未実行 (load gate skip)。15-min load 92.87 は 2×ncpu=20 を大きく上回り、重い
  test スイートの実測を省略。honest に `unmeasured` と記録し、回帰は assert しない
  (基準値据え置き — bench-158 と同方針)。負荷帯は前回 (15min 60.34) を更に上回り、
  重い実測は実行バックエンド応答不能リスク大。

## 再現ベンチ
- seeded repro: not-applicable (sim-loop は L0、学習ジョブ無)

## 回帰
- 基準値 (robotics 14/50/0、giemon 46/115/0) に対し本 walk は unmeasured のため
  regression assert なし。git HEAD 2 点とも変化なし (robotics 9459ca0、giemon d0d3cb4
  = 基準値と同一)。git status: giemon は `?? sim-loop/` 未追跡のみ (前回と同構成)、
  tracked 変更なし → コード変更なし。

## falsify
- falsify-034〜037 は全て refuted 済み、残存 pending なし。新規 falsify なし。
  git diff 空 (tracked 変更なし) のため新決着なし。

## 再現コマンド
```
# load gate (15min ≥ 2x ncpu) 超過のため本 walk は未実行。基準時 (bench-066 確定):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test   # 14/50/0
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test   # 46/115/0
```
コード変更なし。