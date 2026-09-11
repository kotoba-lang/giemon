# bench-153 — giemon sim-loop ベンチ (決定的・タイムスタンプなし)

judgement: **measured** (load 1.38x ncpu < 2x gate)
load: 1min 7.66 / 5min 9.74 / 15min 13.77, ncpu=10 (uptime 11:49)
host: macOS, 9 users

## テスト
- robotics (HEAD 9459ca0): Ran 14 tests, 50 assertions, 0 failures, 0 errors. exit 0
- giemon   (HEAD d0d3cb4): Ran 46 tests, 115 assertions, 0 failures, 0 errors. exit 0

## 再現ベンチ
- seeded repro: not-applicable (sim-loop は L0、学習ジョブ無)

## 回帰
- 基準値 (robotics 14/50/0、giemon 46/115/0) と完全一致。HEAD 2 点とも変化なし (9459ca0, d0d3cb4)。**回帰なし (regression: NO)**

## falsify
- falsify-034〜037 は全て refuted 済み、残存 pending なし。falsify-034 残存なし。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test   # 14/50/0
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test   # 46/115/0
```
コード変更なし。