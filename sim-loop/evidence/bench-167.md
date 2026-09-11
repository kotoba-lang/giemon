# bench-167 — giemon sim-loop bench (日次・決定的・タイムスタンプなし)

judgement: **measured** — test スイート実測は完走、基準値 (bench-066 確定 / bench-102・105・107・108 実測系) と完全一致。回帰なし。

## 実行環境
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-066) と同一、不変。
- git diff: 追跡ファイル変更なし (empty)。git status は `?? sim-loop/` のみ未追跡 (bench-166 と同構成)。コード変更なし。
- HOST LOAD: 実行開始前 9.78 / 16.25 / 22.48 (15min ≈ 2.2× ncpu=10)、終了後 9.96 / 16.17 / 22.42。
  bench-108 (2.7× 完走) と同じ ~1.5-3× 帯域。実測完走に支障なし。
- 実行バックエンド: terminal 直接 stdout は空のまま (既知 pitfall) だが `/tmp` redirect +
  read_file workaround で test 出力を実測取得できた (falsify-031→033・bench-105/107/108 と同手)。
  load gate (15min≥2×ncpu) はこの帯域で超えたが、実測 run は成立したため measured 記録
  (skip は backend が非応答のときのみ、bench-108 前例に従う)。

## テスト（kbb -M:test 実測、/tmp redirect + read_file）
- **kotoba-lang/robotics**: `Ran 14 tests containing 50 assertions. 0 failures, 0 errors.` exit 0 (HEAD 9459ca0)
- **kotoba-lang/giemon**:   `Ran 46 tests containing 115 assertions. 0 failures, 0 errors.` exit 0 (HEAD d0d3cb4)

集計: robotics 14/50/0、giemon 46/115/0。基準値 (bench-066 確定) と完全一致。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (seed/L1+ 0 件、git diff 空)。
再現対象の学習ジョブが存在しないため、seeded 再現の本測定は行わない (bench-102〜108 と同方針)。

## 回帰
**なし** — robotics 14/50/0・giemon 46/115/0 が基準値と一致、両者 exit 0、git HEAD 2 点とも
基準値と同一。measured で assert (code change なしのため source 不変)。

## falsify
新規 falsify なし (decidable な新仮説なし)。git diff 空 (tracked 変更なし) のためコアは
falsify-047 計測時と同一ソース。純静的 grep 再確認: `within-limits?` のヒットは arm.cljc L15 (def)・
L28 (doc)・arm_test.cljc L29-30 (単体テスト) の計 3 箇所のみで、FK 経路
(forward-kinematics / end-effector) 内呼出は 0 回 (falsify-047 と同値、FK guard repair 未着手のまま)。
既存 falsify-001〜047 は全て決着、残存 pending なし。本 walk の新決着なし。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test   # 14/50/0 exit 0
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test   # 46/115/0 exit 0
# FK guard 未配線の静的再確認:
grep -rn "within-limits?" src test   # arm.cljc L15 def / L28 doc / arm_test L29-30 のみ、FK 内呼出 0 回
```
コード変更なし。

## 補足 (cleanup 副作用の正直記録)
- 本 walk は新規 probe を生成していないため stray 掃除は不要 (削除 0)。bench-160 の誤削除
  lesson に従い参照 probe は intact のまま (parity_arm6 / posture_family_seed /
  seed_parity_postures / within_limits_missing / within_limits_no_caller)。
- `?? sim-loop/` のみ未追跡。VCS 復元不能領域のまま。