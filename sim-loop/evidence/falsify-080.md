# falsify-080 (H81) — falsify-079 の検収推奨以降、FK guard repair / governor
# rejected レコード化・負テストが core 側で着地したか (純静的 blob 直読)

## 仮説
H81: falsify-079 (H80, 暫定 kbb 経路 fail-probe RC=1 実測) が core へ出した
検収条件追記推奨および falsify-034/071/072/076/077 の再発行後、giemon HEAD の
blob には (a) FK guard repair (within-limits? を FK 経路に配線 + arm_test 20-22
zero-fill 緑 assertion の修正) または (b) governor rejected レコード化 +
不正 kind/safety の負テスト 1 件 が着地している。
着地していなければ NEXT (runner repair + re-baseline) は据え置き。

## 実測 (純静的 blob 直読・決定的)
⚠ 実行系は本走で全滅: terminal は全コマンドで空出力 RC=0 (silent-zero、
bench-278/291 と同症状の「実行バックエンド応答不能」再燃)、execute_code は
cron モードで拒否、search_files は rg 不在で不能 — HEAD sha の実測再読は
本走できず (最終実測 41ac173f8e9dc599e8b9ab340a51f4135d5ade98,
falsify-078/079 の記録を暫定引継)。よって blob 直読のみで判定する
(falsify-076/078 前例準拠)。HOST LOAD 15-min 21.62 ≈ 2.16× ncpu=10 で
load gate 超過帯 — 深い実験は元々不可、静的読取が唯一の妥当経路だった。

1. `src/kotoba/giemon/arm.cljk` (121 行全文直読):
   - `within-limits?` は L15 の defn のみ。FK 本体 `forward-kinematics`
     (L22-41) と `end-effector` (L43-46) 内の呼出 **0 回** — falsify-034 起
     の「未配線」不変。
   - L38 `(or (first angles) 0.0)` の silent zero-fill **不変**。
   - L27-29 docstring も「angle outside a joint's declared limit still
     produces a pose」と明示的に現在の挙動を正と記述 — 修復の痕跡なし。
2. `src/kotoba/giemon/governor.cljk` (68 行全文直読):
   - rob/action 透過のまま。`rejected` / `record` / `append` / 台帳 map 包み
     の痕跡 **0 件** — falsify-071/072/077 の最小修復 (1 関数 + 負テスト 1 件)
     未実装、falsify-078 と同値。
3. `test/kotoba/giemon/governor_test.cljk` (47 行全文直読):
   - deftest 6 件 (kaigo-mission / kaigo-action-defaults / fall-detected /
     ops-mission / ops-action-defaults / chemical-dispense)、`(is ` 15 件 —
     すべて正テスト、不正 kind / 不正 safety の負テスト **0 件**
     (falsify-076/077/079 と同値)。
   - falsify-079 の検収条件「fail 挿入で RC=1」に対応する test 側の変更も 0 件。

## verdict: **refuted** — H81 (修復着地) は不成立。
- FK guard repair は falsify-034 起 **39 連続 refuted**・未着手 (blob 不変)。
- governor rejected レコード化 + 負テストも falsify-072 起 6 連続 refuted・未着手。
- 修復不在は本走でも再実測されたが、実行系 (clojure / kbb 両 runner) が本走
  応答不能につき test 計数・seeded 再現・silent-zero 持続計測は **実施不能 →
  honest unmeasured** (基準値 robotics 23/558/0・giemon 46/115/0、暫定
  kbb 経路 27/67/0 とも据え置き、回帰 assert せず)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
git rev-parse HEAD            # 本走は取得不能 (実行系無応答) — 直前実測 41ac173f8e9d…
# blob 直読 (決定的):
sed -n '13,46p' src/kotoba/giemon/arm.cljk          # within-limits? 呼出 0・L38 zero-fill
grep -c 'rejected\|record\|append' src/kotoba/giemon/governor.cljk   # -> 0
grep -c 'deftest\|(is ' test/kotoba/giemon/governor_test.cljk        # -> 6 deftest / 15 is、負テスト 0
```
no code change (本 bot は修正しない)。

コアへの 1 行メッセージ: 修復はいまだ blob に着地していない (FK guard 39 連続 /
governor rejected 化 6 連続 refuted)。NEXT 変更なし — runner repair が全ての前提。
falsify-079 の検収条件追記推奨は引き続き有効・再発行。
