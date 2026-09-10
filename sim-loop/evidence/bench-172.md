# bench-172 — giemon sim-loop bench (日次・決定的・タイムスタンプなし)

judgement: **measured** — 高負荷帯 (15min ≈ 5.4× ncpu、peak 1-min ≈ 74) だったが実行
バックエンドは応答し、test スイート実測は完走、基準値 (bench-066 確定 / bench-167〜171 実測系) と完全一致。回帰なし。

## 実行環境
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-066) と同一、不変。
- git diff: 追跡ファイル変更なし (empty)。git status は `?? sim-loop/` のみ未追跡 (bench-171 と同構成)。コード変更なし。
- HOST LOAD: 実行開始前 54.79 / 61.02 / 51.74、終了後 74.18 / 64.71 / 53.76
  (15min 53.76 ≈ 5.4× ncpu=10、peak 1-min 74.18)。bench-171 (3.7× 完走) を大幅に
  上回る帯域だが backend は応答し実測完走。
- 実行バックエンド: terminal 直接 stdout は空のまま (既知 pitfall) だが `/tmp` redirect +
  read_file workaround で test 出力を実測取得 (falsify-031→033・bench-167〜171 と同手)。
  load gate (15min≥2×ncpu) は大きく超えたが実測 run は成立したため measured 記録
  (skip は backend 非応答のときのみ、bench-108・167・168 前例に従う)。

## テスト（clojure -M:test 実測、/tmp redirect + read_file、一意ファイル b172_*.txt）
- **kotoba-lang/robotics**: `Ran 14 tests containing 50 assertions. 0 failures, 0 errors.` exit 0 (HEAD 9459ca0)
- **kotoba-lang/giemon**:   `Ran 46 tests containing 115 assertions. 0 failures, 0 errors.` exit 0 (HEAD d0d3cb4)

集計: robotics 14/50/0、giemon 46/115/0。基準値 (bench-066 確定) と完全一致。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (seed/L1+ 0 件、git diff 空)。
再現対象の学習ジョブが存在しないため、seeded 再現の本測定は行わない (bench-102〜108・167〜171 と同方針)。

## 回帰
**なし** — robotics 14/50/0・giemon 46/115/0 が基準値と一致、両者 exit 0、git HEAD 2 点とも
基準値と同一。measured で assert (code change なしのため source 不変)。

## falsify
新規 falsify なし (decidable な新仮説なし)。git diff 空 (tracked 変更なし) のためコアは
falsify-047・bench-171 計測時と同一ソース。純静的 grep 再確認: `within-limits?` のヒットは
arm.cljc L15 (def)・L28 (doc)・arm_test.cljc L29-30 (単体テスト) の計 3 箇所のみで、FK 経路
(forward-kinematics / end-effector) 内呼出は 0 回 (falsify-047・bench-167〜171 と同値、
FK guard repair 未着手のまま)。既存 falsify-001〜048 は全て決着、残存 pending なし。本 walk の新決着なし。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test   # 14/50/0 exit 0
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && clojure -M:test   # 46/115/0 exit 0
# FK guard 未配線の静的再確認:
grep -rn "within-limits?" src test   # arm.cljc L15 def / L28 doc / arm_test L29-30 のみ、FK 内呼出 0 回
```
コード変更なし。

## 補足 (cleanup 副作用の正直記録)
- 本 walk は新規 probe を生成していないため stray 掃除は不要 (削除 0)。bench-160 の誤削除
  lesson に従い参照 probe は intact のまま (parity_arm6 / posture_family_seed /
  seed_parity_postures / within_limits_missing / within_limits_no_caller)。
- `?? sim-loop/` のみ未追跡。VCS 復元不能領域のまま。