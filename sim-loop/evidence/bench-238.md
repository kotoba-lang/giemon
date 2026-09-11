# bench-238 (measured — 完走・両プロジェクト実測)

## HOST LOAD (実測)
pre-run 01:07 実測: 1min 8.76 / 5min 8.76 / 15min 13.69 (ncpu=10, 15min ≈1.37×, up 5 days 17:50)。
Load gate (15min ≥ 2×ncpu=20) 未過 — gate 通過で test 実施。
test 完了後 01:11 実測: 1min 20.77 / 5min 15.50 / 15min 15.37 — 実行帯 ~1.5–2× で完走
(bench-102~108 と同負荷帯)。bench-237 の backend 応答不能は本 run 解消
(git / clojure / file 系すべて stdout 実測成功)。

## Verdict: measured — 完走
### robotics
Ran 23 tests containing 558 assertions. 0 failures, 0 errors. RC=0
(基準値 bench-066: 14/50/0/0 と不一致 — 下記 Regression 節参照)
### giemon
Ran 46 tests containing 115 assertions. 0 failures, 0 errors. RC=0
(基準値 46/115/0/0 と完全一致)

## HEAD (本 run 実測)
giemon   d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe — 不変 (bench-235/237 既知値 d0d3cb4 と一致)。
tracked diff なし (?? sim-loop/ evidence のみ)。
robotics 893ef76f3adf1c4b04904b304007646c0002a4a1 — bench-235 既知値 396fc33 から進行。
git log -5 実測: 893ef76 Merge jv/drop-nbb-cache / 55c0180 drop nbb cache /
31df0a4 Merge jv/kotoba-text-cljs / a065267 kotoba.lang.text in .cljs /
b75a54f Merge agent/maturity-robotics-test (safety invariants, 7 of 8 regressions used to ship green)。
working tree clean (status 空)。

## Seeded 再現
not-applicable (L0 — sim-loop 学習ジョブ 0 件。sim-loop/ 実測: evidence / manual / status のみ)。

## Regression
- giemon: なし。46/115/0 failures / 0 errors / exit 0、基準値一致。
- robotics: failures/errors なし (0 failures / 0 errors / exit 0) — 赤回帰ではない。
  ただし基準値不一致: 14 tests/50 assertions (bench-066) → 実測 23 tests/558 assertions。
  HEAD 進行 (396fc33 → 893ef76) に伴う suite 拡張が由来:
  新 test namespace 3 件 (export-test / safety-invariants-test / ui-test) が本 run の
  test 出力に実測出現。基準値更新候補: robotics 23/558/0/0 @ 893ef76 (正本更新は実施せず記録のみ)。

## Falsy
新規判定なし (H1〜H67 全決着・未決残存なし; falsify-066 (H67) refuted 据え置き)。

## NEXT
FK guard repair (arm.cljc forward-kinematics への within-limits? 配線 + arm_test.cljc
20-22 期待値変更込み) — 本 run 実測で arm-test は kotoba.giemon.arm-test namespace が緑完走
のまま (46/115 内)。repair 未実装の静的再 grep は本 run 未実施 (budget 限界・捏造回避)。

## 再現コマンド
cd orgs/kotoba-lang/robotics && kbb -M:test > /tmp/b_rob.txt 2>&1; echo RC=$? >> /tmp/b_rob.txt
cd orgs/kotoba-lang/giemon   && kbb -M:test > /tmp/b_gie.txt 2>&1; echo RC=$? >> /tmp/b_gie.txt
(本 run 実施済み・実測完走。/tmp redirect + read_file workaround 使用)
END
