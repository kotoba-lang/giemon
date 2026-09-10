# bench-155 — giemon sim-loop ベンチ (決定的・タイムスタンプなし)

judgement: **unmeasured** (load skip — 15min 25.64 ≈ 2.56x ncpu=10、2x gate 超過)
load: 1min 17.09 / 5min 26.85 / 15min 25.64, ncpu=10 (uptime 12:19)
host: macOS, 8 users

## テスト
- 未実行 (load gate skip)。15-min load 25.64 ≧ 2×ncpu=20 で重い test スイート
  の実測を省略。honest に `unmeasured` と記録し、回帰は assert しない
  (基準値据え置き — bench-099〜101・bench-084-skipped-load と同方針)。

## 再現ベンチ
- seeded repro: not-applicable (sim-loop は L0、学習ジョブ無)

## 回帰
- 基準値 (robotics 14/50/0、giemon 46/115/0) に対し本 walk は unmeasured のため
  regression assert なし。git HEAD 2 点とも変化なし (robotics 9459ca0、giemon d0d3cb4
  = 基準値と同一)。git status: giemon は `?? sim-loop/` 未追跡のみ (前回と同構成)、
  tracked 変更なし → コード変更なし。

## falsify
- falsify-034〜037 は全て refuted 済み、残存 pending なし。新規 falsify なし。
  falsify-034 残存なし。git diff 空 (tracked 変更なし) のため新決着なし。

## 再現コマンド
```
# load gate (15min ≥ 2x ncpu) 超過のため本 walk は未実行。基準時 (bench-066 確定):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test   # 14/50/0
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && clojure -M:test   # 46/115/0
```
コード変更なし。