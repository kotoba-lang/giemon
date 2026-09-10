# bench-160 — giemon sim-loop ベンチ (決定的・タイムスタンプなし)

judgement: **unmeasured** (load skip — 15min 54.02 ≈ 5.40x ncpu=10、2x gate 大幅超過)
load: 1min 18.51 / 5min 31.66 / 15min 54.29, ncpu=10 (uptime 13:49)
host: macOS, 10 users

## テスト
- 未実行 (load gate skip)。15-min load 54.29 は 2×ncpu=20 を大幅に上回り、重い
  test スイートの実測を省略。honest に `unmeasured` と記録し、回帰は assert しない
  (基準値据え置き — bench-158/159 と同方針)。15-min 負荷は前回 (bench-159: 92.87) より
  下がったが依然 2x gate の 2.7 倍超で、重い実測は実行バックエンド応答不能リスク大。

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
- 本 walk の probe 掃除で `probe_velocity_limit_consumption.clj` を誤削除した
  (falsify-021 の repro 手順が参照する probe)。verdict と決定出力
  (`falsify-021_measured.txt`) は無傷のため falsify-021 の記録は有効だが、
  repro コマンド (falsify-021.md 81 行) は今後 probe 不在で動かない。
  sim-loop/ は未追跡 (`??`) のため VCS 復元不能。probe_torque_check_probe.py は
  どの md からも未参照 (真の stray) で削除適正。他 4 probe
  (within_limits_missing / within_limits_no_caller / seed_parity_postures /
  parity_arm6) は参照ありで intact。