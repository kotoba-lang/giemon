# bench-175 — giemon sim-loop bench (日次・決定的・タイムスタンプなし)

judgement: **measured** — 15-min 負荷帯 ≈ 5.1—5.4× ncpu (実行前 53.79 → 実行後 50.71) で
Load gate 大幅超過帯だったが実行バックエンドは応答し、test スイート実測は完走、
基準値 (bench-066 確定 / bench-174 実測系) と完全一致。回帰なし。

## 実行環境
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-066) と同一、不変。
- git diff: 追跡ファイル変更なし (empty)。git status は `?? sim-loop/` のみ未追跡 (bench-174 と同構成)。コード変更なし。
- HOST LOAD: 実行開始前 40.76 / 43.86 / 53.79、終了後 27.20 / 40.29 / 50.71
  (15min 53.79→50.71 ≈ 5.1—5.4× ncpu=10)。bench-174 (≈9.5×) より低い帯域だが Load gate は超過。
- 実行バックエンド: terminal 直接 stdout は空のまま (既知 pitfall) だが `/tmp` redirect +
  read_file workaround で test 出力を実測取得 (bench-167〜174 と同手)。load gate
  (15min≥2×ncpu) を大きく超えたが backend 応答・実測完走のため measured 記録
  (skip は backend 非応答のときのみ、bench-108・167・168 前例に従う)。

## テスト（kbb -M:test 実測、/tmp redirect + read_file、一意ファイル b175_*.txt）
- **kotoba-lang/robotics**: `Ran 14 tests containing 50 assertions. 0 failures, 0 errors.` exit 0 (HEAD 9459ca0)
- **kotoba-lang/giemon**:   `Ran 46 tests containing 115 assertions. 0 failures, 0 errors.` exit 0 (HEAD d0d3cb4)

集計: robotics 14/50/0、giemon 46/115/0。基準値 (bench-066 確定) と完全一致。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (seed/L1+ 0 件、git diff 空)。
再現対象の学習ジョブが存在しないため、seeded 再現の本測定は行わない (bench-102〜108・167〜174 と同方針)。

## 回帰
**なし** — robotics 14/50/0・giemon 46/115/0 が基準値と一致、両者 exit 0、git HEAD 2 点とも
基準値と同一。measured で assert (code change なしのため source 不変)。

## falsify
新規 falsify なし (decidable な新仮説なし)。git diff 空 (tracked 変更なし) のためコアは
falsify-049・bench-174 計測時と同一ソース。純静的 grep 再確認: `within-limits?` のヒットは
arm.cljc L15 (def)・L28 (doc)・arm_test.cljc L29-30 (単体テスト) の計 3 箇所のみで、FK 経路
(forward-kinematics / end-effector) 内呼出は 0 回 (falsify-049・bench-167〜174 と同値、
FK guard repair 未着手のまま)。既存 falsify-001〜049 は全て決着 (maturity 正本: H1〜H50 全決着・
未決残存なし)、本 walk の新決着なし。

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
  seed_parity_postures / within_limits_missing / within_limits_no_caller / fk_guard_ab — 全 6 件実在確認)。
- `?? sim-loop/` のみ未追跡。VCS 復元不能領域のまま。
- 本例は 15-min 帯域 ≈ 5.1—5.4× ncpu の Load gate 超過帯だが、bench-169〜174 と同様に
  backend 応答・実測完走・基準値一致で measured。skip 判定 (backend 非応答) には至っていない
  点を正直に明記。