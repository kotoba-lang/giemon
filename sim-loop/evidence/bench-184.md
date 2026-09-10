# bench-184 — unmeasured (host load)

判定: **unmeasured** (HOST LOAD 超過により clojure test / seeded 再現をスキップ、基準値据え置き・回帰 assert なし)

## 環境
- HOST LOAD (15-min) ≈ 38.4 (5-min ≈ 36.8、1-min ≈ 24.5)
- hw.ncpu = 10  → 15-min load ≈ 3.8× ncpu ≧ 2× gate → 重い実行は省略 (負荷帯が非応答域)
- up: 3 days 13h; 8 users

## テスト数字 (per-project)
- kotoba-lang/robotics: **unmeasured** (負荷超過で実測せず。基準値 14/50/0 据え置き)
- kotoba-lang/giemon: **unmeasured** (同上。基準値 46/115/0 据え置き)

## git HEAD
- robotics: `9459ca0d5b3126472e23de6a77f725a9a3480770` (基準値 9459ca0 と一致、変化なし)
- giemon: `d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe` (基準値 d0d3cb4 と一致、変化なし)

## seeded 再現 verdict
- not-applicable (sim-loop は L0、job なし。L1 以降の seeded 再現対象は今回実行せず)

## 回帰
- 有無を assert せず (unmeasured のため honest 据え置き)
- ソース変更なし・HEAD 変化なしのため回帰兆候は検出されず

## falsify 状況
- falsify-034/035/036/037 (H35〜H38) は既決済み (refuted)。新規 falsify はなし (maturity NEXT = none)。

## 再現コマンド
- (負荷超過のため省略。負荷回復後に `clojure -M:test` (robotics / giemon) を再実行し実測を取る)

## 備考
- bench-184 は bench-099〜101 / bench-182 / bench-183 と同様の load-skip 判断。基準値は bench-066 確定
  (robotics 14/50/0、giemon 46/115/0)。
- コード変更なし (`?? sim-loop/` のみ untracked、bench-183 から実質変化なし)。
- ホスト負荷 (15-min ≈ 38.4) は bench-183 (≈40.5) と同水準の非応答域を継続。