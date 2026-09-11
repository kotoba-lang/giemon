# bench-188 — unmeasured (load)

判定: **unmeasured** (HOST LOAD が 15-min ≈ 3.8× ncpu の非応答域。重い kbb -M:test 実行と seeded 再現を一律 skipped。回帰は assert せず、基準値据え置きで honest。)

## 環境
- HOST LOAD: 15-min ≈ 38.16 / 5-min ≈ 51.64 / 1-min ≈ 59.51 (hw.ncpu = 10 → 15-min ≈ 3.8×)
- 負荷帯は gate (~2×) を大きく超過し、かつ上昇中 (1-min > 5-min > 15-min)。bench-064〜101 の連続 load 超過 skip と同じ非応答域と判断。
- up: 3 days 14h; 7-8 users

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
- falsify-034/035/036/037 (H35〜H38) は既決済み (refuted)。新規 falsify なし (maturity NEXT = none)。

## 再現コマンド
- (skipped — load)。復旧時: `cd .../kotoba-lang/robotics && kbb -M:test` → 期待 14/50/0、`cd .../kotoba-lang/giemon && kbb -M:test` → 期待 46/115/0

## 備考
- 基準値は bench-066 確定 (robotics 14/50/0、giemon 46/115/0)。bench-187 は実測完走 (2.7×) だったが、bench-188 は 3.8× 上昇帯で非応答域のため skip。
- コード変更なし (`?? sim-loop/` のみ untracked)。probe 類は bench/falsify 多数 md から参照され EVIDENCE のため削除せず。