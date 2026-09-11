# bench-178 — giemon sim-loop bench (日次・決定的・タイムスタンプなし)

judgement: **measured** — 15-min 負荷帯 ≈ 14× ncpu (実行開始前 150.12 → 終了後 141.78)
の Load gate 大幅超過帯だったが、実行バックエンドは応答し、両 test スイート実測は
完走、基準値 (bench-066 確定 / bench-177 実測系) と完全一致。回帰なし。

## 実行環境
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-066) と同一、不変。
- git diff: 追跡ファイル変更なし (empty、RC=0)。git status は `?? sim-loop/` のみ未追跡 (bench-177 と同構成)。コード変更なし。
- HOST LOAD: 実行開始前 (pre-run script) 150.12 / 128.24 / 109.82、終了後 141.78 / 131.50 / 112.85
  (15min 109.82→112.85 ≈ 14× ncpu=10)。Load gate (15min≥2×ncpu ≈ 20) に対し大幅超過帯。
- 実行バックエンド: terminal 直接 stdout は空のまま (既知 pitfall) だが `/tmp` redirect +
  read_file workaround で test 出力を実測取得。load gate 大幅超過にもかかわらず
  backend は応答・実測完走したため measured 記録 (skip は backend 非応答のときのみ、
  bench-108・167・177 前例に従う)。

## テスト（kbb -M:test 実測、/tmp redirect + read_file、一意ファイル b178_*.txt）
- **kotoba-lang/robotics**: `Ran 14 tests containing 50 assertions. 0 failures, 0 errors.` exit ROB_RC=0 (HEAD 9459ca0)
- **kotoba-lang/giemon**:   `Ran 46 tests containing 115 assertions. 0 failures, 0 errors.` exit GIE_RC=0 (HEAD d0d3cb4)

集計: robotics 14/50/0、giemon 46/115/0。基準値 (bench-066 確定) と完全一致。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L1+ 未実装 (seed 0 件、git diff 空)。
再現対象の学習ジョブが存在しないため、seeded 再現の本測定は行わない (bench-167〜177 と同方針)。

## 回帰
**なし** — robotics 14/50/0・giemon 46/115/0 が基準値と一致、両者 exit 0、git HEAD 2 点とも
基準値 (bench-066) と同一。measured で assert (source 不変のため非負荷依存)。

## falsify
新規 falsify なし (decidable な新仮説なし)。git diff 空 (tracked 変更なし) のため
コアは falsify-050・bench-177 計測時と同一ソース。純静的再確認: `within-limits?` のヒットは
arm.cljc L15 (def)・L28 (doc)・arm_test.cljc L29-30 (単体テスト) の計 3 箇所のみで、FK 経路
(forward-kinematics / end-effector) 内呼出は 0 回 (falsify-049 〜 bench-177 と同じ、FK guard
repair 未着手のまま)。既存 falsify-001〜050 は全て決着 (maturity 正本)、本 walk の新決着なし。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test   # 14/50/0 exit 0
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test   # 46/115/0 exit 0
# FK guard 未配線の静的再確認:
grep -rn "within-limits?" src test   # arm.cljc L15 def / L28 doc / arm_test L29-30 のみ、FK 内呼出 0 回
```
コード変更なし。

## 補足 (load 超過・cleanup の正直記録)
- 本例は 15-min 帯域 ≈ 14× ncpu の Load gate 大幅超過帯だったが、backend 応答・実測完走・
  基準値一致で measured。skip 判定 (backend 非応答) には至っていないことを正直に明記。
- 本 walk は新規 probe を生成していないため stray 掃除は不要 (削除 0)。bench-160 の誤削除
  lesson に従い、既存 falsify 参照 probe は intact のまま (parity_arm6 / posture_family_seed /
  seed_parity_postures / within_limits_missing / within_limits_no_caller — 全 5 件実在確認済み、
  falsify-008/016/022/023/035/037・bench-046〜121 で参照される健全 probe 26 件も intact)。
  `?? sim-loop/` のみ未追跡。VCS 復元不能領域のまま。