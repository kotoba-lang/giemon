# bench-196 — unmeasured (load)

判定: **unmeasured** (HOST LOAD が 15-min ≈ 7.0× ncpu の非応答域。重い clojure -M:test 実行と seeded 再現を一律 skipped、回帰は assert せず、基準値据え置きで honest。)

## 環境
- HOST LOAD: 直近 15-min ≈　69.79 /　5-min ≈　71.01 /　1-min ≈　　38.84 (hw.ncpu = 10 →　15-min ≈　　7.0×)、up: 3 days 17h、6 users
- 負荷帯は gate (~2×) を大きく超過し、直近 precedent bench-192〜195 (5.6×〜9.1× で skip) と同等の非応答域。1-min (38.84) が 15-min/5-min を下回るものの、依然 high-load 帯。bench-064〜101 と同じ非応答域と判断。

## テスト数字 (per-project)
- kotoba-lang/robotics: **unmeasured** (skipped — load)
- kotoba-lang/giemon: **unmeasured** (skipped — load)
- 基準値 ( bench-066 確定) は据え置き: robotics 14/50/0、giemon 46/115/0

## git HEAD
- robotics: `9459ca0` (基準値 9459ca0 と一致、ソース変化なし)
- giemon: `d0d3cb4` (基準値 d0d3cb4 と一致、ソース変化なし)

## seeded 再現 verdict
- not-applicable (sim-loop は L0、job なし.L1 以降の seeded 再現は対象外..今回も seeded job 実行なし..高負荷のため仮に job があっても skip..

## 回帰
- **assert なし** (unmeasured のため回帰判定は行わない.基準値据え置き)
- HEAD は両方とも基準値と一致し、`?? sim-loop/` のみ untracked でソース変更なし

## falsify 状況
- falsify-056 (H57) 据え置き — 今回新規 falsify 追加なし (前回 bench-195 にて FK guard repair 未着手を refuted、21 連続)。両 HEAD (giemon d0d3cb4 / robotics 9459ca0) 不変・tracked diff 空 (?? sim-loop/ のみ)、`within-limits?` (arm.cljc L15-20) は FK 経路から呼出 0 回、L38 silent zero-fill 不変。ステータス正本 (status/maturity.md) の NEXT は none のまま、継続。

##再現コマンド
- (skipped — load)。復旧時: `cd .../kotoba-lang/robotics && clojure -M:test` →期待 14/50/0、`cd .../kotoba-lang/giemon && clojure -M:test` →期待 46/115/0

##備考
- 基準値は bench-066 確定 (robotics 14/50/0、giemon 46/115/0)。bench-190/191 は実測完走 (~2.4-2.9×) だったが、bench-192〜196 は 15-min ≈5.6×〜9.1× と大幅に高い負荷帯のため skip、負荷が 2× 未満へ下がれば実測復帰の余地あり。
- コード変更なし (`?? sim-loop/` のみ untracked)。probe 類は bench/falsify 多数 md から参照され EVIDENCE のため削除せず。