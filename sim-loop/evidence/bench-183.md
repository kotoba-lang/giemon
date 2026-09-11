# bench-183 — unmeasured (host load)

判定: **unmeasured** (HOST LOAD 超過により clojure test / seeded 再現をスキップ、基準値据え置き・回帰 assert なし)

## 環境
- HOST LOAD (15-min) ≈ 40.5 〜 40.6 (5-min ≈ 43.6〜44.1、1-min ≈ 42.3〜44.3)
- hw.ncpu = 10  → 15-min load ≈ 4.0× ncpu ≧ 2× gate → 重い実行は省略 (負荷帯が非応答域)
- up: 3 days 12h; 8 users

## テスト数字 (per-project)
- kotoba-lang/robotics: **unmeasured** (負荷超過で実測せず。基準値 14/50/0 据え置き)
- kotoba-lang/giemon: **unmeasured** (同上。基準値 46/115/0 据え置き)

## git HEAD
- robotics: `9459ca0` (基準値 9459ca0 と一致、変化なし)
- giemon: `d0d3cb4` (基準値 d0d3cb4 と一致、変化なし)

## seeded 再現 verdict
- not-applicable (sim-loop は L0、job なし。L1 以降の seeded 再現対象は今回実行せず)

## 回帰
- 有無を assert せず (unmeasured のため honest 据え置き)
- ソース変更なし・HEAD 変化なしのため回帰兆候は検出されず

## falsify 状況
- falsify-034/035/036/037 (H35〜H38) は既決済み (refuted)。新規 falsify はなし (maturity NEXT = none)。

## 再現コマンド
- (負荷超過のため省略。負荷回復後に `kbb -M:test` (robotics / giemon) を再実行し実測を取る)

## 備考
- bench-183 は bench-099〜101 / bench-182 と同様の load-skip 判断。基準値は bench-066 確定
  (robotics 14/50/0、giemon 46/115/0)。
- コード変更なし (`?? sim-loop/` のみ untracked)。