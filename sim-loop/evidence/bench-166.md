# bench-166 — giemon sim-loop ベンチ (決定的・タイムスタンプなし)

judgement: **unmeasured** (load skip — 実行時 15min 53.47 ≈ 5.3x ncpu=10、2x gate 大幅超過)
load: 1min 18.93 / 5min 45.17 / 15min 53.47, ncpu=10 (uptime 15:20)
host: macOS, 7 users

## テスト
- 未実行 (load gate skip)。15-min load 53.47 は 2×ncpu=20 を大きく上回り、重い
  test スイートの実測を省略。honest に `unmeasured` と記録し、回帰は assert しない
  (基準値据え置き — bench-165/164/163/162/161 と同方針)。1min 18.93 / 5min 45.17 で
  負荷は高止まり、実行バックエンド応答不能リスク大。

## 再現ベンチ
- seeded repro: not-applicable (sim-loop は L0、学習ジョブ無)

## 回帰
- 基準値 (robotics 14/50/0、giemon 46/115/0) に対し本 walk は unmeasured のため
  regression assert なし。git HEAD 2 点とも変化なし (robotics 9459ca0、giemon d0d3cb4
  = 基準値と同一)。git status: giemon は `?? sim-loop/` 未追跡のみ、tracked 変更なし
  (git diff --stat 空) → コード変更なし。

## falsify
- 新規 falsify なし (decidable な新仮説なし)。git diff 空 (tracked 変更なし) のため
  コアは falsify-047 計測時と同一ソース。純静的 grep 再確認: `within-limits?` の
  ヒットは arm.cljc L15 (def)・L28 (doc)・arm_test.cljc L29-30 (単体テスト) の計 3 箇所
  のみで、FK 経路 (forward-kinematics L22-41 / end-effector L43-46) 内呼出は 0 回
  (falsify-047 と同値、repair 未着手のまま)。既存 falsify-001〜047 は全て決着、
  残存 pending なし。本 walk の新決着なし。

## 再現コマンド
```
# load gate (15min ≥ 2x ncpu) 超過のため本 walk は未実行。基準時 (bench-066 確定):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test   # 14/50/0
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test   # 46/115/0
# FK guard 未配線の静的再確認:
grep -rn "within-limits?" src test   # arm.cljc L15 def / L28 doc / arm_test L29-30 のみ、FK 内呼出 0 回
```
コード変更なし。

## 補足 (cleanup 副作用の正直記録)
- 本 walk は実測 run なしのため新規 stray probe 掃除は行わなかった (bench-160 の
  誤削除 lesson に従い、削除 0)。参照 probe (parity_arm6 / posture_family_seed /
  seed_parity_postures / within_limits_missing / within_limits_no_caller /
  parity_probe / axis_underflow_parity 等) は intact 確認済 (ls sim-loop/evidence で存在確認)。
- `?? sim-loop/` のみ未追跡。VCS 復元不能領域のまま。