# bench-192 — unmeasured (load)

判定: **unmeasured** (HOST LOAD が 15-min ≈ 5.6× ncpu の非応答域。重い clojure -M:test 実行と seeded 再現を一律 skipped。回帰は assert せず、基準値据え置きで honest。)

## 環境
- HOST LOAD: 15-min ≈ 55.83 / 5-min ≈ 49.89 / 1-min ≈ 56.06 (hw.ncpu = 10 → 15-min ≈ 5.6×)
- 負荷帯は gate (~2×) を大きく超過し、直近 precedent bench-189 (4.5× で skip) より更に高水準。1-min (56.06) も 5-min/15-min を上回る上昇傾向。bench-064〜101 と同じ非応答域と判断。
- up: 3 days 15h; 6 users

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
- falsify-034〜054 は FK guard repair 未着手の連続 refuted (最新 falsify-054、H55 で 19 連続 refuted)。HEAD d0d3cb4 不変・tracked diff 空で根因は変化なし。ステータス正本 (status/maturity.md) の NEXT は none のまま。

## 再現コマンド
- (skipped — load)。復旧時: `cd .../kotoba-lang/robotics && clojure -M:test` → 期待 14/50/0、`cd .../kotoba-lang/giemon && clojure -M:test` → 期待 46/115/0

## 備考
- 基準値は bench-066 確定 (robotics 14/50/0、giemon 46/115/0)。bench-190/191 は実測完走 (2.9×/2.4×) だったが、bench-192 は 15-min ≈5.6× と大幅に高い負荷帯のため skip。負荷が 2× 未満へ下がれば実測復帰の余地あり。
- コード変更なし (`?? sim-loop/` のみ untracked)。probe 類は bench/falsify 多数 md から参照され EVIDENCE のため削除せず。