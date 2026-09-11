# bench-239 (measured — 完走・両プロジェクト実測)

## HOST LOAD (実測)
pre-run 04:40 実測: 1min 15.56 / 5min 11.51 / 15min 13.02 (ncpu=10, 15min ≈1.3×, up 5 days 21:23)。
Load gate (15min ≥ 2×ncpu=20) 未過 — gate 通過で test 実施。
test 完了後 04:41 実測: 1min 18.24 / 5min 12.94 / 15min 13.44 — 実行帯 ~1.3–1.8× で完走。

## Verdict: measured — 完走
### robotics
Ran 23 tests containing 558 assertions. 0 failures, 0 errors. RC=0
(基準値 bench-066: 14/50/0/0 と不一致 — 下記 Regression 節参照。bench-238 実測 23/558 と一致)
### giemon
Ran 46 tests containing 115 assertions. 0 failures, 0 errors. RC=0
(基準値 46/115/0/0 と完全一致)

## HEAD (本 run 実測)
giemon   d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe — 不変 (bench-235/238 既知値 d0d3cb4 と一致)。
tracked diff なし (?? sim-loop/ evidence のみ)。
robotics 893ef76f3adf1c4b04904b304007646c0002a4a1 — bench-238 実測値と一致 (396fc33 → 893ef76 進行は bench-238 で既に確認済み)。
working tree clean (status 空)。

## Seeded 再現
not-applicable (L0 — sim-loop 学習ジョブ 0 件。sim-loop/ 実測: evidence / manual / status のみ)。

## Regression
- giemon: なし。46/115/0 failures / 0 errors / exit 0、基準値一致。
- robotics: failures/errors なし (0 failures / 0 errors / exit 0) — 赤回帰ではない。
  基準値不一致 (14/50 → 23/558) は bench-238 で HEAD 進行 (893ef76) に伴う suite 拡張
  (新 namespace 3 件) と実測済み。本 run は 23/558 で bench-238 と完全一致 — 追加変動なし。
  基準値更新候補: robotics 23/558/0/0 @ 893ef76 (正本更新は実施せず記録のみ)。

## Falsy
新規判定なし (H1〜H67 全決着・未決残存なし; falsify-066 (H67) refuted 据え置き)。

## NEXT
FK guard repair (arm.cljc forward-kinematics への within-limits? 配線 + arm_test.cljc
20-22 期待値変更込み) — 本 run 実測で arm-test は kotoba.giemon.arm-test namespace が
緑完走のまま (46/115 内)。repair 未実装の静的再 grep は本 run 未実施 (budget 限界・捏造回避)。

## 再現コマンド
cd orgs/kotoba-lang/robotics && clojure -M:test > /tmp/b_rob.txt 2>&1; echo RC=$? >> /tmp/b_rob.txt
cd orgs/kotoba-lang/giemon   && clojure -M:test > /tmp/b_gie.txt 2>&1; echo RC=$? >> /tmp/b_gie.txt
(本 run 実施済み・実測完走。/tmp redirect + read_file workaround 使用)
END
