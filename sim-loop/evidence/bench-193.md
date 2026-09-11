# bench-193 — unmeasured (load)

判定: **unmeasured** (HOST LOAD が 15-min ≈ 5.6× ncpu の非応答域。重い kbb -M:test 実行と seeded 再現を一律 skipped。回帰は assert せず、基準値据え置きで honest。)

## 環境
- HOST LOAD: 前回 assay 15-min ≈ 55.67、直近 15-min ≈ 55.81 / 5-min ≈ 55.90 / 1-min ≈ 69.70 (hw.ncpu = 10 → 15-min ≈ 5.6×)
- 負荷帯は gate (~2×) を大きく超過し、直近 precedent bench-192 (5.6× で skip) と同等の非応答域。1-min (69.70) が 5-min/15-min を上回る上昇傾向。bench-064〜101 と同じ非応答域と判断。
- up: 3 days 16h; 6 users

## テスト数字 (per-project)
- kotoba-lang/robotics: **unmeasured** (skipped — load)
- kotoba-lang/giemon: **unmeasured** (skipped — load)
- 基準値 (bench-066 確定) は据え置き: robotics 14/50/0、giemon 46/115/0

## git HEAD
- robotics: `9459ca0` (基準値 9459ca0 と一致、ソース変化なし)
- giemon: `d0d3cb4` (基準値 d0d3cb4 と一致、ソース変化なし)

## seeded 再現 verdict
- not-applicable (sim-loop は L0、job なし。L1 以降の seeded 再現は対象外。今回も seeded job 実行なし)

## 回帰
- **assert なし** (unmeasured のため回帰判定は行わない。基準値据え置き)
- HEAD は両方とも基準値と一致、`?? sim-loop/` のみ untracked でソース変更なし

## falsify 状況
- falsify-055 (H56) 追加 — refuted (FK guard repair 未着手、20 連続)。`within-limits?` (arm.cljc L15-20) は FK 経路 (forward-kinematics L22-41 / end-effector L43-46) から呼出 0 回、L38 silent zero-fill 不変、governor.cljc は arm limit/torque 参照 0 行、HEAD d0d3cb4 不変・tracked diff 空。ステータス正本 (status/maturity.md) の NEXT は none のまま。

## 再現コマンド
- (skipped — load)。復旧時: `cd .../kotoba-lang/robotics && kbb -M:test` → 期待 14/50/0、`cd .../kotoba-lang/giemon && kbb -M:test` → 期待 46/115/0

## 備考
- 基準値は bench-066 確定 (robotics 14/50/0、giemon 46/115/0)。bench-190/191 は実測完走 (2.9×/2.4×) だったが、bench-192/193 は 15-min ≈5.6× と大幅に高い負荷帯のため skip。負荷が 2× 未満へ下がれば実測復帰の余地あり。
- コード変更なし (`?? sim-loop/` のみ untracked)。probe 類は bench/falsify 多数 md から参照され EVIDENCE のため削除せず。