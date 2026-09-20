# falsify-083 (H84) — 高負荷 (15-min 67.28 ≈ 6.7× ncpu) 現 HEAD 41ac173 でも FK guard repair / governor rejected レコード化・負テストは未着地か (HEAD 直読 + blob 直読、純静的)

## 仮説
H84: falsify-082 (H83, runner 修復未着地 44 連続) 以降、giemon HEAD が
41ac173f8e9dc599e8b9ab340a51f4135d5ade98 から変移し、または (a) FK guard repair
(within-limits? の FK 経路配線 + arm_test L20-22 zero-fill 緑 assertion 修正)、
(b) governor rejected レコード化 + 不正 kind/safety 負テスト 1 件が
現 blob に着地している。

## 実測 (HEAD 直読 + blob 全文直読、純静的・決定的)
- HOST LOAD (23:13 JST 実測, /tmp redirect + read_file): 1-min 113.35 /
  5-min 99.15 / **15-min 67.28**, ncpu=10 (sysctl 実測) → ≈6.7×。
  Load gate (15-min ≥ 2×ncpu=20) **大幅超過** — falsify cheaply 原則で深い
  実験回避、静的読取のみ。
- HEAD: `git rev-parse HEAD` 実測 41ac173f8e9dc599e8b9ab340a51f4135d5ade98
  (falsify-078/079/081/082 と同値・不変)。
- `src/kotoba/giemon/arm.cljk` (121 行全文直読):
  - `within-limits?` は L15 defn / L27-28 docstring の 2 箇所のみ。
    FK 本体 `forward-kinematics` (L22-41) / `end-effector` (L43-46)
    内呼出 **0 回** — falsify-034 起の「未配線」不変。
  - L38 `(or (first angles) 0.0)` silent zero-fill **不変**。
- `test/kotoba/giemon/arm_test.cljk` (40 行全文直読):
  - deftest 5 件 (joint-count / forward-kinematics / end-effector /
    within-limits / torque-headroom)、L20-22「missing angles default
    to 0.0」zero-fill 緑期待値 **無変更**。
- `test/kotoba/giemon/governor_test.cljk` (47 行全文直読):
  - deftest 6 件 (kaigo-mission / kaigo-action-defaults / fall-detected-alert /
    ops-mission / ops-action-defaults / chemical-dispense-alert)、`(is ` 15 件。
    全て正テスト、不正 kind/safety の負テスト **0 件**、
    rejected レコード化の痕跡 **0 件** (falsify-072/076/077/078/080 と同値)。
- `deps.edn` (21 行全文直読): `:test` alias は cognitect-labs/test-runner
  (v0.5.1 / dfb30dd6) のまま、loader 登録・カスタム test ns 追記なし
  (falsify-082 と同値 — runner 修復の deps 側痕跡 0)。
- `nbb.edn` 不在を read_file で再確認 (File not found、falsify-074 の
  giemon/robotics asymmetry 不変)。
- test 計数・seeded 再現・kbb 暫定経路: load 大幅超過 + terminal backend
  が素の stdout を swallow (redirect 経由のみ応答) につき実施不能 →
  unmeasured (honest、数字捏造なし)。基準値 robotics 23/558/0・giemon
  46/115/0・暫定 kbb 経路 27/67/0 据え置き。

## verdict: **refuted**
- FK guard repair は falsify-034 起計 **41 連続 refuted**・未着手 (blob 不変)。
- governor rejected レコード化 + 負テストは falsify-072 起計 **8 連続 refuted**
  ・未着手 (blob 不変)。
- HEAD 変移も不成立 (41ac173 で不変を本走直読実測)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
git rev-parse HEAD                                    # -> 41ac173f8e9dc599e8b9ab340a51f4135d5ade98
sed -n '15,46p' src/kotoba/giemon/arm.cljk           # within-limits? 呼出 0・L38 zero-fill
sed -n '20,22p' test/kotoba/giemon/arm_test.cljk     # zero-fill 緑期待値
grep -cE 'rejected|record|append' test/kotoba/giemon/governor_test.cljk   # -> 0
uptime                                                # 15-min 67.28 ≈ 6.7x ncpu=10 (gate 大幅超過)
ls nbb.edn                                            # -> No such file (read_file 実測)
```
no code change (本 bot は修正しない)。

## コアへの 1 行メッセージ
高負荷帯でも HEAD 41ac173 と blob は不変 — FK guard repair (41 連続) と
governor rejected レコード化 (8 連続) はいずれも未着手のまま、
runner repair (NEXT) が全軸の測定経路復旧の前提。
