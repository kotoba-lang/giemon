# giemon sim-loop 成熟度 ( status/maturity.md - 正本)

集計元: sim-loop/evidence/ bench-001〜268 / falsify-001〜075 (決定的計算)。
bench-064～101 は連続 load 超過 + 実行バックエンド応答不能で test スイート・seeded
再現・各 H 本測定を一律 skipped したが、falsify-024～030 (H26～H32) は純静的読取で
それぞれ refuted、falsify-031～033 (H33, FK guard 実行系 A/B) は /tmp redirect
workaround の決定的測定で決着 ( falsify-031 refuted: FK guard は arm_test.cljc 20-22 の
silent zero-fill 緑 assertion と干渉。falsify-032 refuted: 高負荷下で決定性は生き残る。falsify-033
refuted: 孤立挿入は存在せず、test 20-22 期待値変更込み repair が必須)。
基準値は bench-066 確定 ( robotics 14/50/0、giemon 46/115/0)。bench-099～101 は load
超過で skip ( unmeasured  honist 据え置き)。bench-102～108 は負荷帯 ~1.5-3x で実測
完走・基準値一致、unmeasured は回帰 assert せず honest。
falsify-034 (H35) refuted — FK angle-count guard repair 未実装 (arm.cljc L38
silent zero-fill、arm_test.cljc 20-22 緑 zero-fill 無変更)。
falsify-035 (H36) refuted — URDF<->EDN parity、全 6 joint x  7 link の全数値が
1e-12 内で完全一致し無破れ;;ただ監査ツール probe_parity_arm6.py が現行 blob で
PARSE-ERR -> exit 1 (陳腐化)。
falsify-036 (H37) refuted — FK guard repair 依然未実装 (実測 arm-test 5/11/0/0 緑)。
falsify-037 (H38) refuted — 陳腐化の真因は slice anchor バグ (name 起点捕捉が
先行する axis を除外。現行 blob は二重 backslash 無し、単一 fold で escape 完全復元)。
falsify-072 (H73) refuted — governor silent-nil 修正は未実装 (governor_test.cljk
負テスト 0 件・governor.cljk 透過不変)。bench-260: runner silent-zero 継続
(robotics 0/0/0 RC=0 @ ad99366 / giemon 0/0/0 RC=0 @ 00fd23f、bench-244〜259 と同値)。
parity 本丸結論は不変。falsify-038 (H39) refuted — damping/摩擦 仮説: EDN `:joint/damping` 6 件・URDF damping
6 件は 1 対 1 同値で parity 無破れだが、コア (src/ test/) は `:joint/damping` を
0 件も読まない (言及は chassis.cljc L14 コメント "ground friction" のみ)。純キネマ
ティクス契約のため DR の damping worst-case 振りは FK / torque-headroom に観測不能 —
摩擦・粘性の動力学面は現コアに存在しない。。
falsify-039 (H40) refuted — FK guard 未配線:`within-limits?` は定義済
   (arm.cljc L15-20、arm_test.cljc L29-30 単体) が FK 経路 ( forward-kinematics
   L22-41 / end-effector) 内部からは呼出 0 回、越境 angles は silent 受理で pose を返す
   (docstring L27-28 自白、L38 silent zero-fill と同根の既知点)。governor 層
   (governor.cljc) は安全クラス分類専用で arm limit/torque に無接続 —「no
   LLM-to-actuator shortcut」は FK  層で未成立 ( falsy-001 の gate<->torque 照合未接続と整合)。
falsify-040 (H41) refuted — FK guard repair 依然未着手 (`within-limits?` は arm.cljc L15 定義/
   L28 doc のみ、FK  本体 L22-41 呼出 0 回、grep 実測で falsify-039 と同値、HEAD d0d3cb4 不変・
   tracked diff 空、governor 無接続のまま — FK  経路は越境 angles を silent  受理、新規破れ・回帰なし)。
falsify-067 (H68) refuted — FK guard repair 29 連続 refuted (純静的読取, `within-limits?`
は arm.cljc L15 defn / L28 docstring のみ・FK 本体 (forward-kinematics L22-41 /
end-effector L43-46) 呼出 0 回、L38 silent zero-fill 不変、arm_test L20-22 緑固定不変)。
bench-237 (skipped — execution backend 応答不能、負荷 gate 内 ~1.1×) unmeasured。
bench-238/239/240 (実測完走、負荷 ~1.3-1.5×) — robotics 23/558/0/0・giemon 46/115/0/0
両 RC=0。giemon HEAD d0d3cb4 不変・robotics HEAD 396fc33 → 893ef76f3adf 進行
( suite 拡張: 新 test namespace 3 件 / 14/50 → 23/558、0 failures/0 errors で赤回帰なし —
robotics 基準値を 23/558/0/0 @ 893ef76 に更新)。bench-241 (skipped — load, 15min ≈79.5 ≈7.9×)。
本 run 静的再確認 (giemon HEAD 実測 d0d3cb4 → 00fd23f9d047 に進行を観測、tracked diff 空
(?? sim-loop/ のみ)): `within-limits?` は arm.cljc 2 行 (L15 defn / L28 doc) のみ・FK 経路
caller 0・silent zero-fill 不変 — repair 未配線を新 HEAD でも再確定・計 30 連続 refuted。
負荷 15min ≈51 (≈5.1×) で Load gate 超過につき本 run は test 未実施・静的のみ (honest)。

bench-109～114 (6 連続実測) — 負荷帯 ~1.0～3x で test スイート実測完走 ( robotics
14/50/0、giemon 46/115/0、exit 0。HEAD giemon d0d3cb4 / robotics 9459ca0 全回不変・
tracked diff 空) — 基準値完全一致、回帰なし measured assert。新規 falsy なし、
未決 falsy 残存なし (H25～H41 全決着)。bench-115 / bench-116 は load 超過
(~3.3× / ~3.6×) で unmeasured (honest 据え置き) とし、bench-117 (負荷 ~1.5×) で
実測完走・基準値一致・回帰なし measured 復帰 (同 HEAD giemon d0d3cb4、tracked diff 空)。
bench-118 / bench-119 (連続実測、負荷 ~1.1×) — test スイート実測完走 ( robotics
14/50/0、giemon 46/115/0、exit 0。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked
diff 空) — 基準値完全一致、回帰なし measured assert。新規 falsy なし (H25～H41 全決着・
未決残存なし、code 無変更で新仮説判定なし)。
bench-120 (load 超過) — HOST LOAD 15min ~24.18 が ncpu=10 の ~2.4× で Load gate
(15min ≥ 2×ncpu=20) 超過し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 /
robotics 9459ca0 不変・tracked diff 空、新規 falsy なし (H25～H41 全決着)。回帰
assert せず基準値 ( bench-066 / bench-119) を据え置き、コード変更なし。。

bench-121 (load 超過) — HOST LOAD 15min ~25.11 が ncpu=10 の ~2.5× で Load gate
(15min ≥ 2×ncpu=20) 超過し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 /
robotics 9459ca0 不変・tracked diff 空、新規 falsy なし (H25～H41 全決着)。回帰
assert せず基準値 ( bench-066 / bench-120) を据え置き、コード変更なし。


bench-122  (実測完走、負荷 ~1.9x) — HOST LOAD 15min ~18.95 が ncpu=10 の Load gate
(15min >= 2xncpu=20) 未満の負荷帯で test スイート実測完走 ( robotics 14/50/0、giemon
46/115/0、exit 0。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空) — 基準値
( bench-066 確定 / bench-111 最新実測) と完全一致、回帰なし measured assert。新規 falsy なし
(H25～H41 全決着・未決残存なし、code 無変更で新仮説判定なし)。


bench-254 (measured, silent-zero 継続・負荷 ~1.6x 帯) — 両スイート kbb -M:test で
0/0/0 RC=0 を再実測 (基準値 robotics 23/558/0・giemon 46/115/0 に対し 0/0/0)。既知の
test-runner silent-zero 不具合と同一症状であり新規回帰ではないが、実測緑は未回復。
HEAD robotics ad99366 / giemon 00fd23f 不変・tracked diff 空。falsify-034 (FK guard
repair) 残存・falsify-070 の kbb 第2測定経路 (21/52/0 緑) 変化なし。
bench-255 (measured, silent-zero 継続・負荷 ~1.6x 帯) — 同様に 0/0/0 RC=0 再実測。
本 run は HEAD 捕捉も失敗 (redirect 順序不良) につき HEAD 変化を assert せず honest。
bench-254 の HEAD 不変観測のみが 最新の確定情報。回帰 assert なし (silent-zero は
runner defect で green pass にも test-count regression にも数えない)。
falsify-071 (H72) refuted — governor 経路の LLM-to-actuator shortcut 仮説: 実在は
せず、ただ `kotoba.robotics/action` (robotics.cljk L64-71) が不正 kind/safety で nil
を返し、governor.cljk L21-27/L53-60 が unvalidated 透過するため「gate による deny」
ではなく silent nil で gate・audit の両方から消える (決定の痕跡喪失)。actuator 直送
は不成立 (nil を gate に渡せば :invalid→deny)。governor_test.cljk は :move のみ網羅で
nil 経路の負テスト 0 件 — 検証の穴。


bench-256 (measured, silent-zero 継続・負荷 ~1.9x 帯) — 両スイート kbb -M:test で
0/0/0 RC=0 を再実測 (silent-zero 持続、bench-244 以来 13 連続)。回帰 assert なし
(runner defect)。HEAD robotics ad99366 / giemon 00fd23f 不変・tracked diff 空。
bench-257 (skipped — load, 15min ≈22.1 ≈2.2× ncpu=10) — unmeasured 据え置き。
HEAD 同一。falsify 新規なし、falsify-034 (FK guard repair 未配線) 据え置き。
NEXT は runner repair + re-baseline を再発行 (継続)。H1〜H72 全決着・未決残存なし。
bench-259 (measured, silent-zero 持続 16 連続・負荷 ~1.4x 帯) — 両スイート kbb -M:test で
0/0/0 RC=0 を再実測 (bench-244 起の既知 runner defect、新規赤の追加なし)。HEAD robotics ad99366 /
giemon 00fd23f 不変・tracked diff 空。回帰 assert なし。falsify-072 (H73) refuted — governor
silent-nil の rejected レコード化 + 負テストは推奨後も未実装 (governor_test.cljk 負テスト 0 件・
governor.cljk 透過不変) — NEXT 推奨の再発行を確定。NEXT は runner repair を継続発行。
bench-261 (measured, silent-zero 持続・負荷 ~1.3x 帯・gate 内完走) — 両スイート kbb -M:test で
0/0/0 RC=0 を再実測 (bench-244 起の既知 runner defect・silent-zero 持続、新規赤の追加なし)。
HEAD robotics ad99366 / giemon 00fd23f 不変・code changes none。回帰 assert なし (honest:
unmeasured-equivalent)。falsify-069 (.cljk load 不能) 根因のまま、test-runner 修復未着手。
falsify 新規なし、falsify-034 (FK guard repair 未配線) 据え置き。NEXT は runner repair +
re-baseline を再発行 (継続)。H1〜H73 全決着・未決残存なし。bench-263 (measured, silent-zero 持続 19 連続・負荷 ~1.2x 帯) — 両スイート kbb -M:test で
0/0/0 RC=0 を再実測 (bench-244 起の既知 runner defect・silent-zero 持続、新規赤の追加なし)。
HEAD robotics ad99366 / giemon 00fd23f 不変。回帰 assert なし (honest: unmeasured-equivalent、
基準値 23/558/0・46/115/0 とは比較不能)。falsify-069 (.cljk load 不能) 根因のまま、
test-runner 修復未着手。falsify 新規なし、falsify-034 据え置き。NEXT は runner repair +
re-baseline を再発行 (継続)。H1〜H73 全決着・未決残存なし。END

## 現在段階
L0 — sim-loop 学習ジョブ未実装のため L1 昇格条件未達 ( seed / L1+ 学習ジョブ 0 件、
テスト・git 差分空、、seeded 再現 N/A)。Honest-default: :in-design (Hitogata/Caterpillar) の成果は
スコアに参入しない。。



## 7 軸スコア ( ADR-2608052000, 決定的計算)
集計: H1〜H67 全決着、未決 falsy ゼロ (falsify-063 (H64) refuted — FK guard repair 未配線・25 連続 refuted、falsify-064 (H65) refuted — 26 連続、falsify-065 (H66) refuted — 27 連続、falsify-066 (H67) refuted — 28 連続、bench-225〜228 の走査・falsify-057 (H58) は FK shortcut 別系で src 内 gate 迂回 shortcut 不存在確定)。bench-192〜196・bench-208〜213・bench-216〜221・bench-223〜227 は load 超過 / backend 応答不能で unmeasured (honest 据え置き; bench-227 の evidence verdict は skipped (execution backend) — 旧集計の「bench-227 実測完走」記載は evidence と不整合につき本回修正)、bench-235 (負荷 ~1.3×帯) は実測完走・基準値一致 measured (robotics 14/50/0・giemon 46/115/0・両者 RC=0、HEAD giemon d0d3cb4 / robotics 396fc33 不変・tracked diff 空)、bench-236 は load 超過 (15min ≈26.54 ≈2.7×) で unmeasured (honest 据え置き・新規 falsy なし)。falsify-067 (H68) refuted — FK guard repair 29 連続 refuted (静的)。bench-237 skipped (backend 応答不能)・bench-241 skipped (load ≈7.9×)。bench-238/239/240 実測完走 (負荷 ~1.3-1.5×): robotics 23/558/0/0・giemon 46/115/0/0 両 RC=0、robotics HEAD 893ef76 進行 (suite 拡張 14/50→23/558・赤回帰なし — robotics 基準値を 23/558/0/0 @ 893ef76 に更新)、giemon HEAD は bench-238/239 実測 d0d3cb4 不変の後、本 run 静的実測で d0d3cb4 → 00fd23f9d047 進行を観測 — 新 HEAD でも `within-limits?` FK 経路 caller 0・silent zero-fill 不変で repair 未配線を再確定 (計 30 連続 refuted)。bench-234 は load 超過 (15min ≈23.57 ≈2.36× ncpu=10) で unmeasured (honest 据え置き)、最新実測完走は bench-235 (負荷 ~1.3× 帯・基準値一致) (負荷 ~2.5× 帯で backend 応答し両スイート完走・基準値一致; bench-232 も連続実測完走・基準値一致)。bench-232 (負荷 ~2.6×) / bench-233 (負荷 ~2.5×) はいずれも robotics 14/50/0・giemon 46/115/0・両 RC=0、HEAD giemon d0d3cb4 / robotics 396fc33 不変・tracked diff 空 (?? sim-loop/ のみ) — 基準値一致・回帰なし measured。robotics HEAD 396fc33 は bench-222 実測 (14/50/0 exit 0) で基準値一致を確認 — 回帰なし measured、移動 HEAD の実測検証済み。 bench-231 は実行 backend 応答不能 + 高負荷帯 (15min ≈24.67 ≈2.5×) で skipped / unmeasured (honest 据え置き)。 bench-242/243 は高負荷 (15min ≈11.4× / ≈6.6×) で skip (unmeasured 据え置き)。bench-244〜249 は低負荷帯 (≈0.9-1.4×) で実測: cljk rename + kbb cutover HEAD (robotics ad99366 / giemon 00fd23f) で kbb -M:test silent-zero 0/0/0 RC=0 を 5 連続実測、kbb -M:test は双方 RC=1 (bench-244)。falsify-069 (H70): .cljk extension 起因 discovery+loadability 二重破れで復帰なし。falsify-034 系 (FK guard repair 未配線) は不変・計 31 連続 refuted。red は bench-244 (measured REGRESSION) を正とする。



bench-231 — 実行バックエンド応答不能 (terminal 全コマンド空出力) + 高負荷帯
(15min ~24.67 ≈ 2.5× ncpu=10) で test / seeded 再現一律 skipped → unmeasured
(honest 据置置。基準値 robotics 14/50/0 / giemon 46/115/0 変更なし、回帰 assert せず)。


1. **Test health — RED (measured, bench-244〜249)** — cljk rename + kbb cutover HEAD (robotics ad99366 / giemon 00fd23f) で両スイート `kbb -M:test` silent-zero (0 tests/0 assertions/RC=0) を 5 連続実測 (bench-244〜252)。新エントリ `kbb -M:test` も RC=1 (bench-244)。falsify-069 (H70): JVM require も .cljk load 不能 (RC=1) — discovery+loadability 二重破れ。最後の実測緑は bench-240: robotics 23/558/0 (893ef76) / giemon 46/115/0 (d0d3cb4)。
   両者 exit 0。bench-066 基準と一致 ( bench-133〜146・bench-149・bench-192〜196・bench-208〜221・bench-223〜227 は load 超過 / backend 応答不能で unmeasured、honest
   据え置き)。
2. **Regression — RED (measured, bench-244)** — HEAD 進行 (robotics d0d3cb4→ad99366 の suite 拡張は bench-238〜240 実実測で緑確認) の後、cljk rename + kbb cutover で test 計数が 0/0/0 に崩壊 (bench-244 measured REGRESSION、bench-245-252 で持続確認)。bench-246 以降は collection-failed (false pass) 扱いで新規破れ assert なし — red は bench-244/245 の measured を据え置き。



   bench-133〜146・bench-149・bench-192〜196・bench-208・bench-209・bench-212・bench-213 は unmeasured (load) で回帰 assert せず。
3. **Reproducibility — L0 (構造的制限)** — seeded 再現は学習ジョブ未実装のため N/A。。
4. **Oracle / parity — 生存 (measured)** — falsy-035: parity 無破れ。falsy-038:
   damping 面も EDN/URDF 1 対 1 同値で無破れ;;監査ツールは slice anchor バグで
   exit 1 (陳腐化、oracle 自体は健全)。falsify-061 (H62): 独立修正 parser (probe_parity_arm6_fixed.py, mutation 検証済) で全 6 joint × 7 link 全数値 1e-12 内一致・mismatch 0 — parity 健全を再確定、赤「監査ツール陳腐化」は解消。
5. **Soundness / fidelity — 潜在修理点あり** — falsy-034/036: arm に角度 guard なし
   silent zero-fill、、falsy-039 / falsy-040: FK 経路は越境 angles を silent  受理 (`within-limits?`
   は定義済だが FK 内呼出 0 回)、governor 層は arm limit/torque に無接続, falsy-058/059/060 (H59/H60/H61) も同根で FK guard repair 未配線継続。。
   falsy-038: コアは `:joint/damping` を読まない純キネマティクス契約で、摩擦面の
   検証面なし — いずれも実装側タスク。。6. **Determinism / cross-run — 生き残り (measured)** — falsy-032 で決定性確立。。
7. **Coverage / honest — 欠落 (従来 OPEN 赤字)** — 長期 sim・parity 自動検証・torque
   照合が未実装; falsy-038: damping/摩擦の動力学面が未実装のため DR worst-case 振り
   は検証不能。falsy-039/040: FK 層に limit 検査が無く、「no LLM-to-actuator shortcut」
   は未成立 (gate 迂回 shortcut は falsify-057 (H58) で src 内不存在`rob/action` 経由のみに確定、FK 層の limit 検査欠落のみ残存)。bench は unmeasured を honest 扱い、数字捏造ゼロ。。



## OPEN 赤字
- **赤: FK angle-count guard repair 未実装** (falsy-034/036/060 refuted, falsify-062 (H63) も refuted, falsify-063 (H64) も refuted, falsify-064 (H65) も refuted) — 実装側タスク。。
- **赤: FK 経路に limit 検査なし** ( falsy-039/040/058/059/060 refuted, falsify-062 (H63) と falsify-063 (H64) も refuted) — `within-limits?` は定義済だが
  FK ( forward-kinematics / end-effector)内部から呼出 0 回、越境 angles を silent 受理。
   governor 層は arm limit/torque に無接続 (gate 迂回 shortcut は falsify-057 で src 内不存在 確定、FK 層の limit検査欠落のみ残存・「no LLM-to-actuator shortcut」の routing 側は成立)。実装側
   タスク。。
- **赤: damping/摩擦の動力学面なし** (falsy-038 refuted) — コアは `:joint/damping` を
  読まない純キネマティクス契約。DR damping worst-case 検証には動力学実装が前提。。
- **赤: parity oracle の Clojure 実装が存在しない (falsy-001)** / caterpillar URDF
  コメント内  -- / gate<->torque 照合未接続 / H19/H20/H21/H23 — 実装側タスク。。



## NEXT ( 1 件)
**NEXT: test-runner 修復 — cljk rename 後の silent-zero (kbb -M:test 両 suite 0/0/0 RC=0、bench-244〜268 で持続実測、24 連続、bench-267 実測 0/0/0 RC=0、bench-262 で kbb 第2経路 21/52/0 緑再現済み) を解消し、robotics 23/558/0ヨgiemon 46/115/0 の実測緑を現 HEAD (robotics ad99366 / giemon 00fd23f) で再確立すること。根因確定済み (falsify-069: JVM require が .cljk をロード不能) で修復未着手を falsify-073 (H74) が静的再確定 (テスト 10 件全て .cljkヨloader 登録なしヨHEAD 不変): test 拡張子を戻すか loader 登録を行い clojure / kbb 両 runner を緑化。runner 修復と同時に、falsify-071 (H72) 起因の governor silent-nil 経路 (不正 kind/safety が deny でなく nil で消える) は falsify-072 (H73) で未実装と確定現存 (負テスト 0 件ヨ透過不変) — rejected レコード化 + 負テスト 1 件追加を core 側へ推奨 (再発行)。FK guard repair (falsify-034 起 31 連綜 refutedヨ未着手) は runner 修復後の再検証。全ての bench/falsify の前提であり最優先修理。**
— 優先理由: measured REGRESSION で全軸の測定経路が失活中。FK guard repair (falsify-068/069 で
31 連続 refuted・未着手) は runner 修復・re-baseline 完了後に再検証する。
( 本 rank  は読み取り + status 更新のみ。sim-loop の evidence・コードは不変更。。)
bench-123 (実測完走、負荷 ~1.42x) — HOST LOAD 15min ~14.20 が ncpu=10 の Load gate
(15min >= 2xncpu=20) 未満の負荷帯で test スイート実測完走 ( robotics 14/50/0、giemon
46/115/0、exit 0。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 — 新規
falsy なし、未決残存なし (H25～H41 全決着)) — 基準値 ( bench-066 確定 / bench-122
最新実測) と完全一致、回帰なし measured assert ( bench-122 に続く実測完走)。


bench-124 (load 超過) — HOST LOAD 15min ~26.2→30.6 (約 2.6×～3.1× ncpu=10) で Load gate
(15min ≥ 2×ncpu=20) 超過・継続上昇中のため重い test 実行を省略し unmeasured
(honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・ tracked diff 空、新規 falsy なし
(H25〜H41 全決着)。回帰 assert せず基準値 ( bench-066 確定 / bench-123 最新実測) を据え置き、
コード変更なし。
bench-125 (load 超過) — HOST LOAD 15min ~48.2→51.4 (約 4.8×〜5.1× ncpu=10) で Load gate
(15min ≥ 2×ncpu=20) を大きく超過・継続上昇中のため重い test 実行を省略し unmeasured
(honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・ tracked diff 空、新規 falsy なし
(H25〜H41 全決着)。回帰 assert せず基準値 ( bench-066 確定 / bench-123 最新実測) を据え置き、
コード変更なし。bench-126 (load 超過) — HOST LOAD 15min ~56.5→58.7 (約 5.6×〜5.9× ncpu=10) で Load gate
(15min ≥ 2×ncpu=20) を大きく超過・継続高止まりのため重い test 実行を省略し unmeasured
(honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空、新規 falsy なし
(H25〜H41 全決着)。回帰 assert せず基準値 ( bench-066 確定 / bench-123 最新実測) を据え置き、
コード変更なし。
bench-127 (load 超過) — HOST LOAD 15min ~50.1→48.8 (約 5× ncpu=10) で Load gate
(15min ≥ 2×ncpu=20) を大きく超過・継続中のため重い test 実行を省略し unmeasured
(honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空、新規 falsy なし
(H25〜H41 全決着)。回帰 assert せず基準値 ( bench-066 確定 / bench-123 最新実測) を据え置き、
コード変更なし。bench-128 (load 超過) — HOST LOAD 15min ≈ 33.99 (約 3.4× ncpu=10) で Load gate (15min ≥ 2×ncpu=20)
を超過帯で継続 (降坂傾向: 5min 21.83、1min 13.59) のため重い test 実行を省略し unmeasured
(honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空、新規 falsy なし
(H25〜H41 全決着)。回帰 assert せず基準値 ( bench-066 確定 / bench-123 最新実測) を据え置き、
コード変更なし。
bench-129 (実測完走、負荷 ~1.9×) — HOST LOAD 15min ~18.74→19.27 が ncpu=10 の ~1.9× で Load gate (15min ≥  2×ncpu=20) 未満の負荷帯で test スイート実測完走 ( robotics 14/50/0、giemon 46/115/0、exit 0。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 — 新規 falsy なし、未決残存なし (H25～H41 全決着)) — 基準値 ( bench-066 確定 / bench-123 最新実測) と完全一致、回帰なし measured assert。

bench-130 (load 超過) — HOST LOAD 15min ~23.15 (約 2.3× ncpu=10) で Load gate
(15min ≥   2×ncpu=20) 超過の負荷帯 (降坂傾向: 5min+/1min 34.83 から降下)。重い test 実行を
省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空、新規 falsy なし
(H25～H41 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値 ( bench-066 確定 /
bench-129 最新実測) を据え置き、コード変更なし。。

bench-131 (実測完走、負荷 ~1.9×) - HOST LOAD 15min 19.1 が ncpu=10 の ~1.9× で Load gate (15min 2×ncpu=20) 未満の負荷帯で test スイート実測完走 ( robotics 14/50/0、giemon 46/115/0、exit 0。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 - 新規 falsy なし、未決残存なし (H25-H41 全決着)) - 基準値 ( bench-066 確定 / bench-123 最新実測) と完全一致、回帰なし measured assert ( bench-129 に続く実測完走)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 - NEXT 再発行継続。。
bench-132 (実測完走、負荷 ~2.0x) — HOST LOAD 15min ~19.78→19.41 が ncpu=10 の ~2.0× で Load gate (15min ≥  ‍2×ncpu=20) 未満の負荷帯で test スイート実測完走 ( robotics 14/50/0、giemon 46/115/0、exit 0。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 — 新規 falsy なし、未決残存なし ( H25〜H41 全決着)) — 基準値 ( bench-066 確定 / bench-129 最新実測) と完全一致、回帰なし measured assert ( bench-131 に続く実測完走)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。。bench-133 (load 超過) — HOST LOAD 15min ~24.6→24.7 (約 2.5× ncpu=10) で Load gate
(15min ≥　2×ncpu=20) を大きく超過、重い test 実行を省略し unmeasured
(honest 据え置き) 一 HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空、新規 falsy なし
(H25〜H41 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値 ( bench-066
確定 / bench-132 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・
tracked diff 空で依然未着手 — NEXT 再発行継続。;bench-134 (load 超過) — HOST LOAD 15min ~25.17 (約 2.5× ncpu=10、1min 43.31/5min 32.00) が Load gate
(15min ≥ 2×ncpu=20) を超過 ( 前回 bench-133 の skip 帯と同水準・上回る高負荷、負荷は上昇
トレンド) のため重い test 実行を省略し unmeasured (honest 据え置き)。HEAD giemon
d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 ( 未追跡 sim-loop/ のみ)、新規 falsy なし
(H25〜H41 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値
( bench-066 確定 / bench-132 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD
不変・tracked diff 空で依然未着手 — NEXT 再発行継続。。bench-135 (load 超過) — HOST LOAD 15min ≈30.76→31.01 ( 約 3.1× ncpu=10、1min 35.06-42.83/5min 36.27-37.60) が Load gate
(15min ≥  2×ncpu=20) を大きく超過 ( 前回 bench-133/134 の skip 帯 ~24.6-25.2 を上回る高負荷・継続上昇) のため重い test 実行を省略し unmeasured (honest
据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 ( 未追跡 sim-loop/ のみ)、新規 falsy なし
(H25〜H41 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値
( bench-066 確定 / bench-132 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked
diff 空で依然未着手 — NEXT 再発行継続。;bench-136 (load 超過) — HOST LOAD 15min ~25.35 (約 2.5× ncpu=10) が Load gate (15min ≥ 2×ncpu=20) を超過 ( 前回 bench-135 の skip 帯よりは低いが依然 gate 超の高負荷帯、1min 16.74 は gate 内だが 15min 基準超過で skip 判断維持)。重い test スイート実行は応答不能リスク高のため省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 ( 未追跡 sim-loop/ のみ)、新規 falsy なし (H25〜H42 全決着・未決残存なし、code 無変更で新仮説判定は falsify-041 のみ)。回帰 assert せず基準値 ( bench-066 確定 / bench-132 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手。

falsify-041 (H42) refuted — FK guard repair 依然未着手 (`within-limits?` は arm.cljc L15 定義・arm_test.cljc L29-30 単体テスト・L28 doc のみ、FK 経路 ( forward-kinematics L22-41 / end-effector L43-46)内部からは呼出 0 回、L38 silent zero-fill 不変、grep 実測で falsify-039/040 と同値、HEAD giemon d0d3cb4 不変・tracked diff 空、governor 層 ( governor.cljc) は arm limit/torque に無接続のまま — 越境 angles を silent 受理で pose 返却、新規破れ・回帰なし)。FK guard repair は HEAD不変・tracked diff 空で依然未着手 — NEXT ( FK guard repair) 再発行継続。。END

bench-137 (load 超過) — HOST LOAD 15min ~21.92 (07:19-21 実測: 1min 16.49 / 5min 19.58 / 15min 21.92) が ncpu=10 の ~2.2× で Load gate (15min ≥ 2×ncpu=20) を超過 (前回 bench-136 の skip 帯より低いが依然 gate 超過の高負荷帯、1min・5min は gate 内 (16.49/19.58<20) だが 15min 基準超過で skip 判断維持)。重い test スイート実行は応答不能リスク高のため省略し unmeasured ( honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (未追跡 sim-loop/ のみ)、新規 falsy なし (H25〜H42 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値 ( bench-066 確定 / bench-132 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。。

bench-138 (load 超過) — HOST LOAD 15min ~24.93 (07:34 実測: 1min 34.09 / 5min 29.86 /  ̈15min 24.93) が ncpu=10 の ~2.5× で Load gate (15min ≥  ̃2×ncpu=20) を超過 (前回 bench-137 の skip 帯 ~22 より更に高い高負荷帯,1min・5min も gate 超過 ( 34.09/29.86>20) で全窓 gate 超過)。重い test スイート実行は応答不能リスク高のため省略し unmeasured ( honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空(未追跡 sim-loop/ のみ)、新規 falsy なし (H25〜H42 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値 ( bench-066 確定 / bench-132 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。。
bench-139 (load 超過) — HOST LOAD 15min ≈20.38 (07:50 実測: 1min 28.05 / 5min 20.76 / 15min 20.38) が ncpu=10 の ≈2.0× で Load gate (15min ≥  2×ncpu=20) を超過 (前回 bench-138 の skip 帯 ≈24.93 よりはやや低下だが依然 gate 超過、1min・5min も gate 超過 (28.05/20.76>20) で全窓 gate 超過)。重い test スイート実行は応答不能リスク高のため省略し unmeasured ( honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 ( 未追跡 sim-loop/ のみ)、新規 falsy なし (H25〜H42 全決着・未決残存なし,code 無変更で新仮説判定なし)。回帰 assert せず基準値 ( bench-066 確定 / bench-132 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。。
bench-140 (load 超過) — HOST LOAD 15min 25.80( 8:04 実測: 1min 25.01、5min 29.18、15min 25.80) が ncpu=10 の ~2.6× で Load gate( 15min ≥ 2×ncpu=20) を超過・全窓( 1min・5min・15min) が gate 超の高負荷で応答不能リスク高のため重い test 実行は省略しunmeasured( honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空( 未追跡 sim-loop/ のみ)、新規 falsy なし( H25〜H43 全決着・未決残存なし、code 無変更で新仮説判定は falsify-042 のみ)。回帰 assert せず基準値( bench-066 確定 / bench-132 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。。
falsify-042 (H43) refuted — FK guard repair 依然未配線( `within-limits?` は arm.cljc L15 定義・arm_test.cljc L28-30 単体テストのみ、FK 経路( forward-kinematics L31-41 / end-effector L43-46)内部からは呼出 0 回、L38 silent zero-fill 不変、governor.cljc 参照 0 なのまま — 越境 angles を silent受理で pose 返却、docstring L27-29 自白、falsify-039/040/041 と同根、HEAD 不変・trackeddiff 空)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。。END


bench-141 (load 超過) — HOST LOAD: 1min 52.75 /  5min 48.86 /  15min 40.43 (8:19 実測) が ncpu=10 の ≈4.0× で Load gate ( 15min ≥ ≈2×ncpu=20) を大きく超過・全窓( 1min・5min・15min) が gate 超過の高負荷で応答不能リスク高のため重い test 実行は省略し unmeasured ( honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空( 未追跡 sim-loop/ のみ)、新規 falsy なし( H25〜H43 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値( bench-066 確定 / bench-132 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。。
bench-142 (load 超過) — HOST LOAD 15min ~39.85 (8:35 実測: 1min 86.38/5min 52.85/15min 39.85) が ncpu=10 の ≈4.0× で Load gate (15min ≥ 2×ncpu=20) を大きく超過・全窓(1min・5min・15min) が gate 超過 (86.38/52.85/39.85>20) の高負荷で応答不能リスク高のため重い test 実行は省略し unmeasured ( honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空( 未追跡 sim-loop/ のみ)、新規 falsy なし( H25〜H43 全決着・未決残存なし_code 無変更で新仮説判定なし)。回帰 assert せず基準値( bench-066 確定 / bench-132 最新実測) を据え置き_コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。;bench-143 (load 超過) — HOST LOAD 15min ≈74.92 (8:50 実測: 1min 41.49/5min 70.80/15min 74.92) が ncpu=10 の ≈7.5× で Load gate (15min ≥  ̃2×ncpu=20) を大きく超過・全窓 (1min・5min・15min) が gate 超過 (>20) の極高負荷で応答不能リスク高のため重い test 実行は省略し unmeasured ( honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (未追跡 sim-loop/ のみ)、新規 falsy なし (H25〜H43 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値 ( bench-066 確定 / bench-132 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。。
bench-144 (load 超過) — HOST LOAD 15min ≈55.33 (9:06 実測: 1min 89.45 / 5min 58.12 / 15min 55.33) が ncpu=10 の ≈5.5× で Load gate (15min ≥ 2×ncpu=20) を大きく超過・全窓 (1min・5min・15min) が gate 超過 (>20) の極高負荷で応答不能リスク高のため重い test 実行は省略し unmeasured ( honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空( 未追跡 sim-loop/ のみ)、新規 falsy なし( H25〜H44 全決着・未決残存なし、code 無変更で新仮説判定は falsify-043 のみ)。回帰 assert せず基準値( bench-066 確定 / bench-132 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。。
falsify-043 (H44) refuted — FK guard repair 依然未配線( `within-limits?` は arm.cljc L15-20 定義・arm_test.cljc L28-30 単体テストのみ、FK 経路( forward-kinematics L22-41 / end-effector L43-46)内部からは呼出 0 回、L38 silent zero-fill(`angle (or (first angles) 0.0)`) 不変、governor.cljc 参照 0 のまま — 越境 angles を silent受理で pose 返却、docstring L27-29 自白、falsify-039/040/041/042 と同根、HEAD d0d3cb4 系列不変・tracked diff 空)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。。ENDbench-145 (load 超過) — HOST LOAD 15min ≈52.95 (9:50 実測: 1min 31.75 / 5min 29.43 / 15min 52.95) が ncpu=10 の ≈5.3× で Load gate (15min ≥ 2×ncpu=20) を大きく超過・全窓(1min・5min・15min) が gate 超過 (>20) の極高負荷で応答不能リスク高のため重い test 実行は省略し unmeasured ( honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空( 未追跡 sim-loop/ のみ)、新規 falsy なし( H25〜H44 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値( bench-066 確定 / bench-132 最新実測) を据え置き_コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。;;falsify-044 (H45) refuted - FK guard repair still unwired (within-limits? src hits: L15 def / L28 doc only, FK path forward-kinematics L22-41 calls 0x, L38 silent zero-fill unchanged, governor.cljc refs 0; HEAD d0d3cb45.. unchanged, tracked diff empty, load 15min 24.04>2xncpu=20 so heavy tests skipped, static read verdict). NEXT reissue continues. ENDbench-146 (load 超過) — HOST LOAD 15min ≈27.08 (10:04 実測: 1min 11.15 / 5min 12.42 / 15min 27.08) が ncpu=10 の ≈2.7× で Load gate (15min ≥  2×ncpu=20) を超過・15min 窓のみ gate 超過 (1min/5min は gate 内だが 15min 基準超過で skip 判断維持) の高負荷で重い test 実行は省略し unmeasured ( honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 ( 未追跡 sim-loop/ のみ)、新規 falsy なし ( H25〜H45 全決着・未決残存なし_code 無変更で新仮説判定は falsify-044 のみ)。回帰 assert せず基準値( bench-066 確定 / bench-132 最新実測) を据え置き_コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。
bench-147 (実測完走、負荷 ~1.9×) — HOST LOAD 15min ~19.10 (10:19 実測: 1min 7.54 / 5min 13.91 / 15min 19.10) が ncpu=10 の ~1.9× で Load gate (15min ≥ 2×ncpu=20) 未満の負荷帯で test スイート実測完走 ( robotics 14/50/0、giemon 46/115/0、両者 exit 0。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 — 新規 falsy なし、未決残存なし (H25〜H45 全決着、code 無変更で新仮説判定なし)) — 基準値 ( bench-066 確定 / bench-146 load skip ・HEAD 不変) と完全一致、回帰なし measured assert ( bench-146 load gate 超過 skip 明けに実測再開・bench-145 以来の実測完走復帰)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。
bench-148 (実測完走、負荷 ~1.65×) — HOST LOAD 15min ~16.47 (10:35 実測: 1min 17.52 / 5min 16.74 / 15min 16.47) が ncpu=10 の ~1.65× で Load gate (15min ≥ 2×ncpu=20) 未満の負荷帯で test スイート実測完走 ( robotics 14/50/0、giemon 46/115/0、両者 exit 0。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 — 新規 falsy なし、未決残存なし (H25〜H45 全決着、code 無変更で新仮説判定なし)) — 基準値 ( bench-066 確定 / bench-147 実測完走・HEAD 不変) と完全一致、回帰なし measured assert ( bench-147 に続く連続実測完走)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。
bench-149 (load 超過) — HOST LOAD 15min ≈32.19 (10:50 実測: 1min 59.53 / 5min 48.85 / 15min 32.19) が ncpu=10 の ≈3.2× で Load gate (15min ≥ 2×ncpu=20) を大きく超過・1min は約 6× (54→59) で上昇中、応答不能リスク高のため重い test 実行は省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (未追跡 sim-loop/ のみ)、新規 falsy なし (H25〜H45 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値 ( bench-066 確定 / bench-148 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。bench-150 (load 超過) — HOST LOAD 15min ≈33.83 (11:04 計測: 1min 18.77 / 5min 27.91 / 15min 33.83) が
ncpu=10 の ≈3.4× で Load gate (15min ≥ 2×ncpu=20) を大きく超過・応答不能リスク高のため重い
test 実行は省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・
tracked diff 空 (未追跡 sim-loop/ のみ)、新規 falsy は falsify-045 のみ判定。回帰 assert せず基準値
(bench-066 確定 / bench-148 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・
tracked diff 空で依然未着手 — NEXT 再発行継続。。END
falsify-045 (H46) refuted — FK guard repair 依然未配線 (`within-limits?` は arm.cljc L15-20 定義・
arm_test.cljc L28-30 単体テストのみ、FK 経路 (forward-kinematics L22-41 / end-effector L43-46) 内部
からは呼出 0 回、L38 silent zero-fill (`angle (or (first angles) 0.0)`) 不変、arm_test L20-22 が silent
zero-fill 緑固定、governor.cljc 参照 0 のまま — 越境 angles を silent 受理で pose 返却、docstring
L27-29 自白、falsify-034/036/039/040/041/042/043/044 と同根、HEAD giemon d0d3cb4 系列不変・
tracked diff 空 (純静的読取、load 15min ≈34 > 2×ncpu=20 + 実行 backend 不能で test 計数は
unmeasured、数字捏造ゼロ))。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT
再発行継続。ENDbench-151 (load 超過) — HOST LOAD 15min ≈23.06 (計測: 1min 21.24 / 5min 20.17 / 15min 23.06) が
ncpu=10 の ≈2.3× で Load gate (15min ≥ 2×ncpu=20) を超過・応答不能リスク高のため重い
test 実行は省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・
tracked diff 空 (未追跡 sim-loop/ のみ)、新規 falsy なし・新仮説判定なし (H25〜H46 全決着)。
回帰 assert せず基準値 (bench-066 確定 / bench-148 最新実測) を据え置き、コード変更なし。
FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。END
bench-217 (load 超過) — HOST LOAD 154.73/116.09/95.25 (1/5/15min, ncpu=10 ≈ 9.5-15×) が Load gate (15min ≥ 2×ncpu=20) を大幅超過のため test スイート・seeded 再現・各 H 本測定を一律省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 (基準一致) / robotics 396fc33 — robotics HEAD が基準 9459ca0 から移動を観測 (負荷超過で test 未測定のため回帰判定せず、実測検証は負荷収束後の次回に必要)。新規 falsy なし (H1〜H62 全決着)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。END
bench-218 (load 超過) — HOST LOAD 82.55/106.47/109.01 (≈ 8-11×) が Load gate を大幅超過のため重い test 実行を一律省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 / robotics 396fc33 (bench-217 と同一 HEAD、移動は bench-217 前から継続、回帰判定せず負荷収束後に実測検証必要)。新規 falsy なし (H1〜H62 全決着)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。END

bench-196 (load 超過) ( HOST LOAD 15min approx 69.79 (approx 7.0x ncpu=10, 1min approx 38.84 = 非応答域) が Load gate
(15min >= 2x ncpu=20) を大幅超過= 応答不能リスク高のため重い test 実行と seeded 再現を
一律省略し unmeasured (honest 据え置き, HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff
空 (未追跡 sim-loop/ のみ, 新規 falsy なし (前回 bench-195 にて FK guard repair 未着手を
refuted 済み, 既決 falsify-056 (H57) 据え置き,H1〜H57 全決着・未決残存なし,code 変更なしで新仮説判定なし).)
回帰 assert せず, 基準値 (bench-066 確定 / bench-191 最新実測完走) を据え置き,コード変更なし.FK guard repair は
HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続.END

bench-197 (実測完走, 負荷 ≈4.8×) — HOST LOAD 15min ≈46.48 (≈4.6-4.8× ncpu=10, 実行後 1-min 44.31 / 5-min 41.67) が Load gate 超過帯だったが backend 応答で /tmp redirect + read_file workaround により test スイート実測完走 (robotics 14/50/0、giemon 46/115/0、両者 exit 0.) HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (未追跡 sim-loop/ のみ)) — 新規 falsy なし, 未決残存なし (H1〜H57 全決着, code 無変更で新仮説判定なし)) — 基準値 (bench-066 確定 / bench-191 実測) と完全一致, 回帰なし measured assert (bench-196 load skip 明けに実測再開)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT ( FK guard repair) 再発行継続。END
falsify-057 (H58) refuted — giemon src 内に governor gate を迂回する LLM-to-actuator shortcut 経路は存在
しない (area4: gate 迂回 / no-LLM-to-actuator-shortcut 検査。純静的読取、load 15min ≈33.7
= ≈3.4× ncpu=10 で Load gate 超過帯 + terminal backend が素の stdout を吞むため重い test は省略し
test 計数 unmeasured、数字捏造ゼロ)。src 全 8 ファイル( kotoba.giemon / .arm / .kinematics /
.chassis / .governor / .export / .ui / .viewer) の外部実行/プロセス/ネット呼出 grep (process|spawn|
socket|http|Thread|future|sh/|Runtime|System/|dispatch|bang) は実 match 0 (hit 4 行は全て
docstring/UI「never dispatches」物語文のみ)、駆動系 grep (drive|actuat|execute|transmit|publish|send-|
emit!|move!) は actuator BOM 記述専用 + governor「never drives hardware」宣言で実行駆動呼出
0。action 構築 (governor.cljc L16-68 全読) は全て `kaigo-action` / `ops-action` → `rob/action`
( kotoba.robotics 契約) 経由のみ、`:emit` エスカレーション (fall-detected-alert / chemical-dispense-alert) も
`rob/action :safety-critical` で gate の human sign-off 経路に流れる — `rob/action` 迂回 dispatch /
gate迂回呼出 0。トップ契約 (giemon.cljc L1-13) docstring「never drives hardware ... No network, no I/O」は
実装と一致。両 HEAD (giemon d0d3cb4 / robotics 9459ca0) 不変・ tracked diff 空 (?? sim-loop/ のみ)。verdict:
refuted — gate 迂回 shortcut は src 内に存在せず、`rob/action` 経由のみで robotics の gate 契約に流れる
(H58 仮説反証、実測判定 1/1、判定材料 5 観測点)。gate 実体 ( rob/gate 本体) は robotics repo 側にあり
本測定の射程は「Giemon src 内に gate 迂回 shortcut なし」に限定。NEXT ( FK guard repair) は HEAD 不変・
tracked diff 空で依然未着手 — 再発行継続。END
bench-198 (実測完走, 負荷 approx 3.1x) - HOST LOAD approx 3.1x ncpu=10 で Load gate 超過帯だったが backend 応答で /tmp redirect + read_file workaround により test スイート実測完走 (robotics 14/50/0, giemon 46/115/0, 両者 exit 0.) HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (未追跡 sim-loop/ のみ)) - 新規 falsy なし, 未決残存なし (H1〜H59 全決着, code 無変更で新仮説判定なし)) - 基準値 (bench-066 確定 / bench-197 実測) と完全一致, 回帰なし measured assert (bench-197 に続く連続実測完走}. FK guard repair は HEAD 不変・tracked diff 空で依然未着手 - NEXT ( FK guard repair) 再発行継続。END

bench-199 (実測完走, 負荷 ≈4.4×) — HOST LOAD 15min ≈ 37.3-44.1 (≈3.7-4.4× ncpu=10) が Load gate 超過帯だったが backend 応答で /tmp redirect + read_file workaround により test スイート実測完走 (robotics 14/50/0、giemon 46/115/0、両者 exit 0。, HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (未追跡 sim-loop/ のみ)) — 新規 falsy なし, 未決残存なし (H1〜H59 全決着, code 無変更で新仮説判定なし)) — 基準値 (bench-066 確定 / bench-198 実測) と完全一致, 回帰なし measured assert (bench-198 に続く連続実測完走)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。END

bench-200 (実測完走, 負荷 ~7.4×) — HOST LOAD 15min ≈73.59 (≈7.4× ncpu=10, 1-min 66.75 / 5-min 81.34) が Load gate 大幅超過帯だったが backend 応答で /tmp redirect + read_file workaround により test スイート実測完走 (robotics 14/50/0、giemon 46/115/0、両者 exit 0, HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (未追跡 sim-loop/ のみ)) — 新規 falsy なし,, 未決残存なし (H1〜H59 全決着,, code 無変更で新仮説判定なし)) — 基準値 (bench-066 確定 / bench-199 実測) と完全一致,, 回帰なし measured assert (bench-199 に続く連続実測完走)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。END
bench-201 (実測完走,, 負荷 ≈4.2×) — HOST LOAD 15min ≈ 23.40→42.21 (≈4.2× ncpu=10心中 1-min 23.40 / 5-min 26.98) が Load gate 大幅超過帯だったが backend 応答で /tmp redirect + read_file workaround により test スイート実測完走 (robotics 14/50/0, giemon 46/115/0,, 両者 exit 0.) HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空( 未追跡 sim-loop/ のみ)) — 新規 falsy なし,, 未決残存なし (H1〜H59 全決着,, code 無変更で新仮説判定なし)) — 基準値 (bench-066 確定 / bench-200 実測) と完全一致,, 回帰なし measured assert (bench-200 に続く連続実測完走)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。,END
falsify-058 (H59) refuted — FK guard repair 依然未配線 (`within-limits?` は arm.cljc L15-20 定義・L28 doc・arm_test.cljc L28-30 単体のみ、FK 経路 (forward-kinematics L22-41 / end-effector L43-46) 内部からは呼出 0 回,L38 silent zero-fill (`angle (or (first angles) 0.0)`) 不変,arm_test L20-22 が silent zero-fill 緑固定,governor.cljc refs 0 のまま — 越境 angles を silent 受理で pose 返却,docstring L27-29 自白,falsify-034/036/039/040/041/042/043/044/045/046/047/048/049/050/051/052/053/054/055/056 と同根 (falsify-057 は FK shortcut 仮説で別系),HEAD giemon d0d3cb4 系列不変・tracked diff 空(純静的読取, git HEAD/status・grep・read は /tmp redirect workaround で実測取得, load 15min ≈42.83 は gate 大幅超過 + terminal backend が素の stdout を swallow で test 計数 unmeasured, 数字捏造ゼロ)).,FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。,END

bench-202 (実測完走, 負荷 ≈3.2×) — HOST LOAD 15-min ≈31.95 (≈3.2× ncpu=10) が Load gate
  超過帯だったが backend 応答で /tmp redirect + read_file workaround により test スイート実測完走
  (robotics 14/50/0, giemon 46/115/0, 両者 exit 0.) HEAD giemon d0d3cb4 / robotics 9459ca0 不変・
  tracked diff 空( 未追跡 sim-loop/ のみ)) — 新規 falsy なし,, 未決残存なし (H1〜H59 全決着,, code 無変更で新仮説判定なし))
  — 基準値 (bench-066 確定 / bench-201 実測) と完全一致,, 回帰なし measured assert (bench-201 に続く連続実測完走,, high-load 帯
  (~3.2×) でも backend 応答で measured 記録)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 —
  NEXT(FK guard repair) 再発行継続。,END

bench-203 (実測完走,, 負荷 ≈4.5×) — HOST LOAD 15-min ≈45.42 (≈4.5× ncpu=10, 1-min 55.19 / 5-min 51.53)
が Load gate 大幅超過帯だったが backend 応答で /tmp redirect + read_file workaround
(bench-197〜202 と同手) により test スイート実測完走 (robotics 14/50/0, giemon
46/115/0., 両者 exit 0,, per-project 出力 /tmp/b_rob_203.txt /tmp/b_gie_203b.txt 完走 fixture
あり)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空( 未追跡 sim-loop/ のみ))
— 新規 falsy なし,, 未決残存なし (H1〜H59 全決着,, code 無変更で新仮説判定なし))
— 基準値 (bench-066 確定 / bench-202 実測) と完全一致,, 回帰なし measured assert
(bench-202 に続く連続実測完走,, load gate 大幅超過帯 (~4.5×) でも backend 応答で
measured 記録)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 —
NEXT(FK guard repair) 再発行継続。,END
bench-203 (実測完走,, 負荷 ≈4.5×) — HOST LOAD 15min ≈ 45.42 (≈4.5× ncpu=10, 1-min 55.19 / 5-min 51.53、実行終了時) が Load gate ( 15min ≥	 2×ncpu=20) を大幅超過帯だったが backend 応答で /tmp redirect + read_file workaround により test スイート実測完走 (robotics 14/50/0, giemon 46/115/0,, 両者 exit 0.) HEAD giemon d0d3cb45fcc / robotics 9459ca0d5b3 不変・tracked diff 空( 未追跡 sim-loop/ のみ)) — 新規 falsy なし,, 未決残存なし (H1〜H59 全決着,, code 無変更で新仮説判定なし; `within-limits?` ヒット arm.cljc L15 def /L28 doc/arm_test L29-30 の計 3 箇所のみ・FK 経路内呼出 0 回で falsify-058 と同値)) — 基準値 (bench-066 確定 / bench-202 実測) と完全一致,, 回帰なし measured assert (bench-202 に続く実測完走,, high-load 帯 (≈4.5×) でも backend 応答で measured 記録)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT(FK guard repair)) 再発行継続。,END

bench-204 (実測完走, 負荷 ≈4.6×) — HOST LOAD 15-min ≈46.62 (≈4.6× ncpu=10, 1-min 41.08 / 5-min 41.97)
が Load gate 大幅超過帯だったが backend 応答で /tmp redirect + read_file workaround (bench-197〜203
と同手) により test スイート実測完走 (robotics 14/50/0, giemon 46/115/0, 両者 exit 0, per-project
fixture /tmp/b_rob_204.txt /tmp/b_gie_204.txt)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked
diff 空 (未追跡 sim-loop/ のみ) — 新規 falsy なし, 未決残存なし (H1〜H59 全決着, code 無変更で新仮説判定
なし) — 基準値 (bench-066 確定 / bench-203 実測) と完全一致, 回帰なし measured assert (bench-203 に続く
実測完走, load gate 大幅超過帯 (~4.6×) でも backend 応答で measured 記録)。FK guard repair は HEAD 不変・
tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。END

bench-205 (実渫完走, 負荷 ≈4.1×) — HOST LOAD 15-min ≈40.64 (≈4.1× ncpu=10, 1-min 37.33 / 5-min 37.53)
が Load gate 大幅超過帯だったが backend 応答で /tmp redirect + read_file workaround (bench-200〜204
と同手) により test スイート実渫完走 (robotics 14/50/0, giemon 46/115/0, 両者 exit 0, per-project
fixture /tmp/b_rob_205.txt /tmp/b_gie_205.txt 完走確認済み, final 行 RC=0 / DONE-MARKERあり。HEAD giemon d0d3cb4 /
robotics 9459ca0 不変・ tracked diff 空 (未追跡 sim-loop/ のみ) — 新規 falsy なし, 未決残存なし (H1〜H59 全決着,
code 無変更で新仮説判定なし)) — 基準値 (bench-066 確定 / bench-204 実渫) と完全一致, 回帰なし measured assert
(bench-204 に続く実渫完走, load gate 大幅超過帯 (~4.1×) でも backend 応答で measured 記録))。FK guard repair は HEAD 不変・
tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。END

bench-206 (実測完走, 負荷 ≈2.8×) — HOST LOAD 15-min ≈27.55 (≈2.8× ncpu=10, 1-min 18.93 / 5-min 21.93) が Load gate (15min ≥ 2×ncpu=20) を超過した帯域だったが backend 応答で /tmp redirect + read_file workaround (bench-200〜205 と同手) により test スイート実測完走 (robotics 14/50/0, giemon 46/115/0, 両者 exit 0, per-project fixture /tmp/b_rob_206.txt /tmp/b_gie_206.txt に完走 fixture あり, final 行 RC=0 / DONE-MARKER 確認済)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・ tracked diff 空 (未追跡 sim-loop/ のみ) — 新規 falsy なし, 未決残存なし (H1〜H59 全決着, code 無変更で新仮説判定なし) — 基準値 (bench-066 確定 / bench-205 実測) と完全一致, 回帰なし measured assert (bench-205 に続く実測完走, load gate 超過帯 (≈2.8×) でも backend 応答で measured 記録)。FK guard repair は HEAD 不変・ tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行続。END


falsify-059 (H60) refuted — FK guard repair
依然未配線 (`within-limits?` は arm.cljc L15-20 定義・L28 doc・arm_test.cljc L28-30 単体のみ、
FK 経路 (forward-kinematics L22-41 loop 本体 L31-41 / end-effector L43-46) 内部から呼出
0 回。L38 silent zero-fill (`angle (or (first angles) 0.0)`) 不変、arm_test L20-22
が silent zero-fill 緑固定,governor.cljc refs 0 のまま — 越境 angles を silent 受理で pose
返却,docstring L27-29 自白,falsify-034/036/039/040/041/042/043/044/045/046/047/048/049/050/051/052/053/054/055/056/058 と同根 (falsify-057
は FK shortcut 仮説で別系,,HEAD giemon d0d3cb45fcc8 / robotics 9459ca0 系列不変・tracked
diff 空(純静的読取, git HEAD/status・grep・read は /tmp redirect workaround で実測取得, load
15min ≈39.94 ≈4.0× ncpu=10 は gate 大幅超過 + terminal backend が素の stdout を swallow
で test 計数 unmeasured, 数字捏造ゼロ)).,FK guard repair は HEAD 不変・tracked diff 空で依然
未着手 — NEXT(FK guard repair)) 再発行継続。,END

bench-207 (実測完走, 負荷 ≈3.6×) — HOST LOAD 15-min 36.38 (≈3.6× ncpu=10, 実行中 1-min peak 81.91) が Load gate 超過帯だったが backend 応答で /tmp redirect + read_file workaround (ベンチ 200〜206 と同手) により test スイート実測完走 (robotics 14/50/0, giemon 46/115/0, 両者 exit 0, fixture /tmp/b_rob_207.txt /tmp/b_gie_207.txt 完走確認済み). HEAD giemon d0d3cb4 / robotics 9459ca0 不変・ tracked diff 空 (未追跡 sim-loop/ のみ) — 新規 falsy なし, 未決残存なし (H1〜H60 全決着, code 無変更で新仮説判定なし) — 基準値 (bench-066 確定 / bench-206 実測) と完全一致, 回帰なし measured assert (bench-206 に続く実測完走). FK guard repair は HEAD 不変・ tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行続。END

bench-208 (load 超過) — HOST LOAD 15-min ≈50.62 (≈5.1× ncpu=10, 実行時実測 15-min 48.57/1-min 35.15/5-min 48.76) が Load gate (15min ≥ 2×ncpu=20) を大きく超過 (前回 bench-207 の ≈3.6× よりも高負荷帯)・実行 spike で backend 応答喪失リスク高のため重い test 実行は省略し unmeasured (honest 据え置き). HEAD giemon d0d3cb4 / robotics 9459ca0 不変・ tracked diff 空 (未追跡 sim-loop/ のみ), 新規 falsy なし (H1〜H60 全決着, falsify-034〜037 は既決 refuted, 未決残存なし, code 無変更で新仮説判定なし). 回帰 assert せず基準値 (bench-066 確定 / bench-207 最新実測) を据え置き, コード変更なし. FK guard repair は HEAD 不変・ tracked diff 空で依然未着手 — NEXT 再発行続。END
bench-209 (load 超過) — HOST LOAD 15-min ≈41.57 (≈4.2× ncpu=10, 1-min 42.69 / 5-min 38.15) が Load gate (15min ≥ 2×ncpu=20) を大きく超過 (直前 bench-208 ≈5.1× よりやや低いが依然 ~4× の高負荷帯)・実行 spike で backend 応答喪失リスク高のため重い test 実行は省略し unmeasured (honest 据え置き). HEAD giemon d0d3cb4 / robotics 9459ca0 不変・ tracked diff 空 (未追跡 sim-loop/ のみ), 新規 falsy なし (H1〜H60 全決着, falsify-034〜037 は既決 refuted, 未決残存なし, code 無変更で新仮説判定なし). 回帰 assert せず基準値 (bench-066 確定 / bench-207 最新実測) を据え置き, コード変更なし. FK guard repair は HEAD 不変・ tracked diff 空で依然未着手 — NEXT 再発行続。END
bench-210 (load 超過) — HOST LOAD 15min ≈67.99 (=≈6.8× ncpu=10, 1min 83.33 / 5min 78.99) が Load gate (15min ≥  2×ncpu=20) を大幅超過・応答不能リスク高のため重い test 実行は省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (未追跡 sim-loop/ のみ)、新規 falsy は falsify-060 のみ判定 (H61, FK guard repair 仮説 refuted — `within-limits?` は arm.cljc L15-20 定義・arm_test.cljc L28-30 単体・docstring のみで,FK 経路 (forward-kinematics L22-41 / end-effector L43-46) 内部から呼出 0 回・L38 silent zero-fill 不変・governor.cljc refs 0 のまま — 越境 angles を silent 受理で pose 返却,HEAD d0d3cb4 系列不変・tracked diff 空,falsify-034/036/039/040/041/042/043/044/045/046/047/048/049/050/051/052/053/054/055/056/058/059 と同根 (falsify-057 は FK shortcut 仮説で別系)・22連続 refuted)、H1〜H62 全決着・未決残存なし, code 無変更で新仮説判定なし). 回帰 assertせず基準値 (bench-066 確定 / bench-207 最新実測) を据え置き, コード変更なし. FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行続。,END
bench-211 (load 超過) — HOST LOAD 15-min ≈146.34 (≈14.6× ncpu=10, 本系列最大負荷帯, 1-min 146.34 / 5-min 107.58) が Load gate (15min ≥ 2×ncpu=20) を大幅超過・応答不能リスク高 (素の uptime/ls すら 60s timeout で応答喪失 を観測) のため重い test 実行は省略し unmeasured (honest 据え置き). HEAD giemon d0d3cb4 / robotics 9459ca0 不変・ tracked diff 空 (未追蹡 sim-loop/ のみ), 新規 falsy は falsify-060 (H61, FK guard repair 仮説 refuted — `within-limits?` は arm.cljc L15-20 定義・arm_test.cljc L28-30 単体・docstring のみで FK 経路 (forward-kinematics L22-41 / end-effector L43-46) 内部から呼出 0 回・L38 silent zero-fill 不変・governor.cljc refs 0 のまま — 越境 angles を silent 受理で pose 返却, HEAD d0d3cb4 系列不変・tracked diff 空, falsify-034/036/039/040/041/042/043/044/045/046/047/048/049/050/051/052/053/054/055/056/058/059 と同根 (falsify-057 は FK shortcut 仮説で別系)・23連続 refuted), H1〜H62 全決着・未決残存なし, code 無変更で新仮説判定なし). 回帰 assert せず基準値 (bench-066 確定 / bench-207 最新実測) を据え置き, コード変更なし. FK guard repair は HEAD 不変・ tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行続。END
bench-212 (load 超過) — HOST LOAD 15-min ≈62.40 (≈6.2× ncpu=10) が Load gate (15min ≥ 2×ncpu=20) を大幅超過・応答不能リスク高のため重い test 実行は省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (未追跡 sim-loop/ のみ)、新規 falsy なし (最新 falsify-060 (H61) FK guard repair 仮説 refuted、H1〜H62 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値 (bench-066 確定 / bench-207 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。END

bench-213 (load 超過) — HOST LOAD 15-min ≈43.14 (≈4.3× ncpu=10, 1-min ≈2.0× へ下降傾向) が Load gate (15min ≥ 2×ncpu=20) を超過したが応答不能リスクのため重い test 実行は省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (未追跡 sim-loop/ のみ)、新規 falsy なし (最新 falsify-060 (H61) refuted、H1〜H62 全決着・未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値 (bench-066 確定 / bench-207 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。END

bench-214 (実測完走, 負荷 ≈2.3×) — HOST LOAD 15-min ≈23.31→23.27 (≈2.3× ncpu=10, 実行前 1min 26.93/5min 21.03/15min 23.31) が Load gate (15min ≥ 2×ncpu=20) を僅かに超過した帯域だったが deps warm で両スイート短時間応答し /tmp redirect + read_file workaround (bench-202〜207 と同手) により test スイート実測完走 (robotics 14/50/0, giemon 46/115/0, 両者 exit 0, fixture /tmp/rob_out.txt /tmp/gie_out.txt 完走確認済み). HEAD giemon d0d3cb45fcc8 / robotics 9459ca0d5b32 不変・tracked diff 空 (未追跡 sim-loop/ のみ) — 新規 falsy なし, 未決残存なし (H1〜H62 全決着, code 無変更で新仮説判定なし) — 基準値 (bench-066 確定 / bench-207 最新実測) と完全一致, 回帰なし measured assert (bench-208〜213 の skip 帯明けに実測復帰). FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。END


## falsify-061 (H62) survived — 監査ツール陳腐化を解消: 陳腐化した slice-anchor 監査 (probe_parity_arm6.py PARSE-ERR exit 1) を廃し独立修正 parser (probe_parity_arm6_fixed.py: `:joint/axis [` 起点捕捉で axis/origin 除外バグ無し、mutation 検証済 — 実 EDN j1 :effort 40→41 で mismatch 1/exit 1 を捕捉) で URDF↔EDN 再監査 — 全 6 joint × 7 link 全数値 (base off-diag ixy/ixz/iyz 含む) が 1e-12 内で一致、mismatches 0 / exit 0 (実測判定 1/1、負荷 ≈1.8× は gate 内且つテキスト照合で負荷影響ゼロ)。parity は無破れ、赤「監査ツール陳腐化」は解消 (oracle 健全、falsify-035/037 の結論を独立 parser で再確定)。FK guard repair (falsify-034〜060 refuted) とは別系 — NEXT (FK guard repair) は HEAD 不変・tracked diff 空で依然未着手、再発行継続。END

bench-215 (実測完走, 負荷 ≈2.3×, execution 中 spike) — HOST LOAD 15-min ≈22.73 (≈2.3× ncpu=10, 1min 19.91 / 5min 21.41) が Load gate (15min ≥ 2×ncpu=20) を僅かに超えた帯域だったが (spike 1-min 48.35→59.50 の上振れも見た) deps warm + /tmp redirect + read_file workaround (bench-202〜214 と同手) により test スイート実測完走 (robotics 14/50/0, giemon 46/115/0, 両者 exit 0). HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (未追跡 sim-loop/ のみ) — 新規 falsy なし, 未決残存なし (H1〜H62 全決着, code 無変更で新仮説判定は falsify-060 (H61 refuted) 据え置き) — 基準値 (bench-066 確定 / bench-214 最新実測) と完全一致, 回帰なし measured assert (bench-214 に続く連続実測完走, load gate 僅か超過帯でも deps warm/redirect workaround で measured 記録). FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。END
bench-216 (load 超過) — HOST LOAD 15min ≈ 73.79 (15-min ≈ 7.4× ncpu=10, 1-min 84.05 / 5-min 89.30 / 15-min 73.79) が Load gate (15min ≥ 2×ncpu=20) を大幅超過 · 応答不能リスク高のため重い test 実行と seeded 再現を一律省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変 · tracked diff 空 (未追跡 sim-loop/ のみ)、新規 falsy なし (latest falsify-061 (H62) survived・falsify-060 (H61) refuted、H1〜H62 全決着 · 未決残存なし、code 無変更で新仮説判定なし)。回帰 assert せず基準値 (bench-066 確定 / bench-215 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変 · tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。END

falsify-062 (H63) refuted — FK guard repair 依然未配線 (`within-limits?` は arm.cljc L15-20 定義・L28 doc のみの計 2 箇所、FK 経路 (forward-kinematics L22-41 loop 本体 L31-41 / end-effector L43-46) 内部から呼出 0 回、L38 silent zero-fill (`angle (or (first angles) 0.0)`) 不変、arm_test L20-22 が silent zero-fill 緑固定・期待値変更なし、governor.cljc arm/limit/torque/joint 参照 0 行のまま — 越境 angles を silent 受理で pose 返却、docstring L27-29 自白、falsify-034/036/039/040/041/042/043/044/045/046/047/048/049/050/051/052/053/054/055/056/058/059/060 と同根 (falsify-057 は FK shortcut 仮説で別系)・24 連続 refuted、HEAD giemon d0d3cb45fcc8 系列不変・tracked diff 空 (純静的読取、git HEAD/status は /tmp redirect workaround で実測取得、負荷 ~15.5× ncpu=10 は Load gate (15min ≥ 2×ncpu=20) 大幅超過 + 重い test は省略で test 計数 unmeasured、数字捏造ゼロ))。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT(FK guard repair) 再発行継続。END

bench-219 (load 超過) — HOST LOAD 15min ≈111.03–111.39 (≈11× ncpu=10) が Load gate
(15min ≥ 2×ncpu=20) を大幅超過のため test スイート・seeded 再現を一律省略し unmeasured
(honest 据え置き)。HEAD giemon d0d3cb4 (基準一致) / robotics 396fc33 — robotics HEAD
移動は bench-217 以来継続、test 未実行につき回帰判定せず・負荷収束後の再確認必要。
新規 falsy なし (H1〜H63 全決着)。FK guard repair は HEAD 不変・tracked diff 空で
依然未着手 — NEXT 再発行継続。END
bench-220 (load 超過) — HOST LOAD 15min ≈100.89 (≈10× ncpu=10) が Load gate (15min ≥ 2×ncpu=20) を大幅超過したため test スイート・seeded 再現を一律省略し unmeasured(honest 据え置き)。HEAD giemon d0d3cb4 (bench-219 同一確認範囲) / robotics 396fc33 据え置き・tracked diff 空 (?? sim-loop/ のみ)、新規 falsy なし (H1〜H63 全決着)。回帰 assert せず基準値 (bench-066 確定 / bench-215 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。END

## falsify-063 (H64) refuted — FK guard repair 依然未配線 (純静的読取, HEAD giemon d0d3cb45fcc8 不変・tracked diff 空 (?? sim-loop/ のみ)。`within-limits?` 出現は arm.cljc 2 行 (L15 defn / L28 docstring)・governor.cljc 0 行・arm_test.cljc L28-30 単体のみ、FK 経路 (forward-kinematics L22-41 / end-effector L43-46) 内部から呼出 0 回・L38 silent zero-fill `(angle (or (first angles) 0.0))` 不変・arm_test L20-22 silent zero-fill 緑固定不変 — 越境 angles を silent 受理で pose 返却, falsify-034/036/039〜063 と同根・26 連続 refuted。負荷 15min ≈71 (~7.2× ncpu=10) gate 大幅超過につき test/seeded は省略 unmeasured。NEXT(FK guard repair) 再発行継続。END

bench-221 (load 超過) — HOST LOAD 15min ≈45.87–49.86→70.95–73.29 (≈7.1× ncpu=10) が Load gate (15min ≥ 2×ncpu=20) を大幅超過のため kbb -M:test (両スイート) と seeded 再現を 一律省略し unmeasured (honest 据え置き)。HEAD giemon d0d3cb4 (baseline 一致) / robotics 396fc33 (bench-219/220 と同一・基準 9459ca0 からの移動継続、test 未実行につき回帰判定せず・負荷収束後の 再確認必要)。新規 falsy は falsify-063 (H64) のみ判定・refuted (FK guard repair 依然未配線、25 連続 refuted)。H1〜H65 全決着・未決残存なし。回帰 assert せず基準値 (bench-066 確定 / bench-215 最新実測) を据え置き、コード変更なし。FK guard repair は HEAD 不変・tracked diff 空で 依然未着手 — NEXT 再発行継続。END

bench-222 (実測完走) — bench 記載の HOST LOAD 15min ≈40.6-41.5 (ncpu=10 の ~4×, gate 超過帯) だが bench-222 側は 1-min 11.76-15.44 (~1.5×) を根拠にゲート未満と判断して実行、両スイート実測完走 (robotics 14/50/0、giemon 46/115/0、exit 0、基準値 bench-066 と完全一致) — 回帰なし measured assert。HEAD giemon d0d3cb45 (baseline 一致・不変) / robotics 396fc33 (移動後の初実測で基準値一致を確認、回帰判定 measured)。新規 falsy なし (H1〜H65 全決着・未決残存なし)。FK guard repair は HEAD 不変・tracked diff 空 (?? sim-loop/ のみ) で依然未着手 — NEXT 再発行継続。END
bench-223 (load 超過) — HOST LOAD 15min ≈42.55 (≈4.7× ncpu=10, 1min 68.87 / 5min 46.84) が Load gate (15min ≥ 2×ncpu=20) を大きく超過のため kbb -M:test (robotics/giemon) と seeded 再現を一律省略し unmeasured (honest 据え置き)。基準値 (robotics 14/50/0、giemon 46/115/0) 据え置き、回帰 assert せず。HEAD giemon d0d3cb4 不変・tracked diff 空 (未追跡 sim-loop/ のみ)。新規 falsy なし (H1〜H65 全決着・未決残存なし; falsify-038 (H39) damping 仮説は前回分で既集計済み・今回ファイル再確認のみ)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。END

bench-224 (load 超過) — HOST LOAD 15min ≈26.92 (≈2.7× ncpu=10, 1min 7.45 / 5min 15.62) が Load gate
(15min ≥ 2×ncpu=20) を超過のため kbb -M:test (robotics/giemon) と seeded 再現を省略し unmeasured
(honest 据え置き)。基準値 (robotics 14/50/0、giemon 46/115/0) 据え置き、回帰 assert せず。前回実測は
bench-222 (基準値一致)。HEAD giemon d0d3cb4 不変・tracked diff 空 (未追跡 sim-loop/ のみ)。新規 falsy
なし (H1〜H65 全決着・未決残存なし)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 —
NEXT 再発行継続。END

falsify-064 (H65) refuted — FK guard repair 依然未配線 (純静的読取, HEAD giemon
d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe 不変・tracked diff 空 (?? sim-loop/ のみ)。
`within-limits?` 出現は arm.cljc 2 行 (L15 defn / L28 docstring)・governor.cljc 0 行・
arm_test.cljc 単体のみ、FK 経路 (forward-kinematics / end-effector) 内部から呼出 0 回・
silent zero-fill `(angle (or (first angles) 0.0))` 不変・arm_test「missing angles
default to 0.0」緑固定不変 — 越境 angles を silent 受理で pose 返却,
falsify-034/036/039〜063 と同根・26 連続 refuted。負荷 15min ≈27-36 (~2.7-3.6×
ncpu=10) gate 超過につき test/seeded は省略 unmeasured。NEXT(FK guard repair) 再発行継続。END

bench-226 (load 超過) — HOST LOAD 15min ≈50.15 (1min 93.45 / 5min 69.27, ≈5.0× ncpu=10) が
Load gate (15min ≥ 2×ncpu=20) を大幅超過 + terminal backend 応答不能継続 (echo を含む全コマンド
空出力・bench-225 と同一症状) のため kbb -M:test (robotics/giemon) と seeded 再現を
一律省略し unmeasured (honest 据え置き)。基準値 (robotics 14/50/0、giemon 46/115/0)
据え置き、回帰 assert せず。前回実測は bench-222 (基準値一致)。HEAD giemon d0d3cb4
不変・tracked diff 空 (?? sim-loop/ のみ)、robotics 396fc33 (bench-222 実測で基準値一致
確認済み)。新規 falsy なし (H1〜H65 全決着・未決残存なし)。FK guard repair は
HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。END

bench-227 (skipped — execution backend, 負荷 ~2.4× 低下傾向) — HOST LOAD 15min ≈23.60 は低下したが terminal
実行バックエンドが継続応答不能 (echo / date を含む全コマンド空出力・bench-225/226 と同一症状) のため
kbb -M:test・seeded 再現は実施不能 → unmeasured (honest, 数字捏造ゼロ)。
※旧集計の「bench-227 実測完走」記載は evidence (bench-227.md verdict: skipped) と不整合につき本回で修正。
基準値 (robotics 14/50/0、giemon 46/115/0) 据え置き、回帰 assert せず。
HEAD giemon d0d3cb45 / robotics 396fc33 不変・tracked diff 空 (?? sim-loop/ のみ)。
新規 falsy なし (falsify-064 (H65) refuted 据え置き, H1〜H65 全決着・未決残存なし)。
FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。END

falsify-065 (H66) refuted — FK guard repair 依然未配線 (純静的読取, HEAD giemon d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe 不変・tracked diff 空 (?? sim-loop/ のみ)。`within-limits?` 出現は arm.cljc 2 行 (L15 defn / L28 docstring)・governor.cljc 0 行・arm_test.cljc 単体のみ、FK 経路 (forward-kinematics L22-41 / end-effector L43-46) 内部から呼出 0 回・silent zero-fill `(angle (or (first angles) 0.0))` 不変・arm_test「missing angles default to 0.0」緑固定不変 — 越境 angles を silent 受理で pose 返却, falsify-034/036/039〜064 と同根・27 連続 refuted。負荷 15min ≈22.1 (~2.2× ncpu=10) gate 超過につき test/seeded は省略 unmeasured。NEXT(FK guard repair) 再発行継続。END

bench-228 (実測完走, 負荷 ~2.7×→完了時 ~2.5×) — HOST LOAD 15min ≈27.10 が Load gate (15min ≥ 2×ncpu=20) を超過する帯だったが実行バックエンドは応答し kbb -M:test 両スイート実測完走 (robotics 14 tests/50 assertions/0 failures/0 errors RC=0、giemon 46 tests/115 assertions/0 failures/0 errors RC=0) — 基準値 (bench-066) と完全一致、回帰なし measured assert。HEAD giemon d0d3cb45fcc8 (基準一致) / robotics 396fc33d0a6 (bench-227 と同一; 9459ca0 から移動継続だが bench-222 実測で基準値一致確認済み) 不変・tracked diff 空 (?? sim-loop/ のみ)。seeded 再現は not-applicable (L0)。新規 falsy なし (falsify-034 残存, falsify-035〜037 refuted 済, H1〜H66 全決着)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。END
bench-229 (実測完走, 負荷 ~2.9×) — HOST LOAD 15min ≈28.60 (≈2.9× ncpu=10) が Load gate (15min ≥ 2×ncpu=20) を超過する帯だったが実行バックエンドは応答し kbb -M:test 両スイート実測完走 (robotics 14 tests/50 assertions/0 failures/0 errors RC=0、giemon 46 tests/115 assertions/0 failures/0 errors RC=0) — 基準値 (bench-066) と完全一致、回帰なし measured assert。HEAD giemon d0d3cb4 (基準一致) / robotics 396fc33 (bench-227/228 と同一) 不変・tracked diff 空 (?? sim-loop/ のみ)。seeded 再現は not-applicable (L0)。新規 falsy なし (falsify-034 残存, falsify-035〜037 refuted 済, H1〜H66 全決着)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。END
bench-230 (実測完走, 負荷 ~4.2×) — HOST LOAD 15min ≈41.53 (≈4.2× ncpu=10, 開始時 1min 78.82 / 5min 58.08) が Load gate (15min ≥ 2×ncpu=20) を超過する帯だったが実行バックエンドは応答し kbb -M:test 両スイート実測完走 (robotics 14 tests/50 assertions/0 failures/0 errors RC=0、giemon 46 tests/115 assertions/0 failures/0 errors RC=0) — 基準値 (bench-066) と完全一致、回帰なし measured assert。HEAD giemon d0d3cb45fcc8 (基準一致) / robotics 396fc33d0a6 (bench-227/228/229 と同一) 不変・tracked diff 空 (?? sim-loop/ のみ)。seeded 再現は not-applicable (L0)。新規 falsy なし (falsify-034 残存, falsify-035〜037 refuted 済, H1〜H66 全決着)。FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。END

falsify-066 (H67) refuted — FK guard repair 依然未配線 (純静的読取, HEAD giemon d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe 不変・tracked diff 空 (?? sim-loop/ のみ)。`within-limits?` 出現は arm.cljc 2 行 (L15 defn / L28 docstring)・governor.cljc 0 行・arm_test.cljc L28-30 単体のみ、FK 経路 (forward-kinematics L22-41 / end-effector L43-46) 内部から呼出 0 回・silent zero-fill `(angle (or (first angles) 0.0))` L38 不変・arm_test「missing angles default to 0.0」緑固定不変 — 越境 angles を silent 受理で pose 返却, falsify-034/036/039〜065 と同根 (falsify-057 は別系)・28 連続 refuted。負荷 15min ≈24.5 (~2.5× ncpu=10) gate 超過 + backend が素の stdout を吞むため test/seeded は省略 unmeasured (honest, /tmp redirect + read_file で静的実測取得、数字捏造ゼロ)。NEXT(FK guard repair) 再発行継続。END

bench-234 (load 超過) — HOST LOAD 15min ≈23.57 (1min 22.49 / 5min 23.57 / 15min 29.82 時点計測, ≈2.36× ncpu=10) が
Load gate (15min ≥ 2×ncpu=20) を超過のため kbb -M:test (robotics/giemon) と seeded 再現を一律省略し unmeasured
(honest 据え置き)。基準値 (robotics 14/50/0、giemon 46/115/0) 据え置き、回帰 assert せず。前回実測は bench-233
(基準値一致)。HEAD giemon d0d3cb4 不変・tracked diff 空 (?? sim-loop/ のみ)、robotics 396fc33 (bench-222 実測で
基準値一致確認済み)。新規 falsy なし (falsify-066 (H67) refuted 据え置き, H1〜H67 全決着・未決残存なし)。
FK guard repair は HEAD 不変・tracked diff 空で依然未着手 — NEXT 再発行継続。END

falsify-066 (H67) refuted — FK guard repair 依然未配線 (純静的読取, HEAD giemon
d0d3cb45fcc8 不変・tracked diff 空 (?? sim-loop/ のみ)。`within-limits?` 出現は arm.cljc 2 行
(L15 defn / L28 docstring)・governor.cljc 0 行・arm_test.cljc L28-30 単体のみ、FK 経路
(forward-kinematics L22-41 / end-effector L43-46) 内部から呼出 0 回・silent zero-fill
`(angle (or (first angles) 0.0))` L38 不変・arm_test「missing angles default to 0.0」緑固定不変 —
越境 angles を silent 受理で pose 返却, falsify-034/036/039〜065 と同根 (falsify-057 は別系)・
28 連続 refuted。負荷 15min ≈24.5 (~2.5× ncpu=10) gate 超過 + backend が素の stdout を吞むため
test/seeded は省略 unmeasured (honest, /tmp redirect + read_file で静的実測取得、数字捏造ゼロ)。
NEXT(FK guard repair) 再発行継続。END
bench-242 skipped (load 15-min 113.79 ≈ 11.4x ncpu; unmeasured, baselines
robotics 23/558/0 / giemon 46/115/0 据え置き)。HEAD drift 記録: giemon 00fd23f /
robotics ad99366 — 基準値参照 d0d3cb4 / 893ef76 は陳腐化、次回 measured run で
両 suite を現行 HEAD で re-baseline する事を NEXT に含める事。


falsify-068 (H69) refuted — FK guard repair 依然未配線 (純静的読取, /tmp redirect + read_file workaround, HOST LOAD 15min ≈22.37 ≈2.6× ncpu=10 で Load gate 超過につき test/seeded 省略 unmeasured)。HEAD giemon 00fd23f9d047 (bench-242 観測と同一・不変)・tracked diff 空 (?? sim-loop/ のみ)。within-limits ヒット 5 行のみ (arm.cljk L15 defn / L28 doc・arm_test.cljk L28-30 単体)、FK 経路 (forward-kinematics L22 / end-effector L46) 内部呼出 0 回・silent zero-fill (angle (or (first angles) 0.0)) L38 不変・governor.cljk limit/torque/within 参照 0 行 — 新 HEAD でも repair 未着手を再確定・計 31 連続 refuted。NEXT (FK guard repair) 再発行継続。END


bench-244 (実測完走, 負荷 gate 内 15min 9.55-10.09 ≈1.0×) — HEAD giemon d0d3cb4→00fd23f9d047 /
robotics 893ef76→ad99366f 両進行 (cljk rename + kbb cutover) の後、kbb -M:test 両 suite が
「Ran 0 tests containing 0 assertions」RC=0 に崩壊 (実測 REGRESSION / silent-zero、基準値
robotics 23/558/0・giemon 46/115/0 から -100%)。新 entry point kbb -M:test も両 project RC=1
(robotics: nbb_deps.js ERR_INVALID_ARG_TYPE / giemon: clojure.java.io 未解決) — 緑 runner は現状
存在しない。root-cause 属性 (runner が *_test.cljk をマッチしない) は推論・0/0/0 自体は measured。
7 軸更新: axis 1 test health と axis 2 regression を RED (runner 崩壊・measured) に改定。
新規 falsify なし (falsify-068 (H69) 31 連続 refuted は既集計)。NEXT を FK guard repair から
runner repair + re-baseline に差し替え (repair > 新機能・測定経路復旧が全検証の前提)。END

bench-245 (実測完走, 負荷 gate 内 15min ~8.2-9.0 ≈0.9×、4 件の常駐 runaway nbb node ~99% CPU が
負荷の主体・本 bench 起因ではない実測) — bench-244 と同一 HEAD (giemon 00fd23f / robotics
ad99366) で silent-zero REGRESSION の持続を再実測: kbb -M:test 両 suite とも
「Ran 0 tests containing 0 assertions」RC=0 (基準値 robotics 23/558/0・giemon 46/115/0 から
-100% 不変)。kbb -M:test は再実行せず bench-244 の RC=1 両 project を最終実測として据え置き。
回帰: 持続 (carry-over・新規破れなし)。measured RED。

falsify-069 (H70) refuted — silent-zero は discovery 不一致のみでなく loadability 破れ
(実行系実測, load gate 通過 15min 8.02): giemon HEAD 00fd23f で
`kbb -M -e "(require 'kotoba.giemon.arm-test)"` → FileNotFoundException
(kotoba/giemon/arm_test.clj[c] on classpath 無し) RC=1 — JVM require は .cljk を
ロード不能。runner の discovery を直しても現 extension のままでは復帰しない。静的補助:
within-limits? は arm.cljk L15/L28・arm_test.cljk L28-30 単体・FK 本体呼出 0・silent
zero-fill L38 不変 (falsify-068 再確認、計 31 連続 refuted)。NEXT を extension/loader
修復込み runner 緑化 + re-baseline に差し替え (本 run)。H1〜H70 全決着・未決残存なし。END

bench-246 (実測, 負荷 gate 内 15min 9.34 ≈0.93×・LOAD OPEN) — bench-244/245 と同一 HEAD
(giemon 00fd23f / robotics ad99366) で kbb -M:test 再実測: 両 suite とも
「Ran 0 tests containing 0 assertions」RC=0 (silent-zero 持続・bench-244/245 と同値)。
diagnostics 実測 (probe3): test ファイルは robotics test/kotoba/robotics/ 配下 4 件
(*_test.cljk)・src も .cljk 存在・deps.edn :test alias intact — runner は namespace を
1 件も発見できず (collection failed) → bench-246 の 0/0/0 は false pass 扱い、
regression は bench-244/245 の measured RED を据え置き (新規破れ assert せず)。
falsify-069 (H70) の loadability 破れ結論と整合: .cljk extension 起因の
discovery+loadability 二重破れで復帰なし。falsify-034 (FK guard repair 未配線) は
据え置き (arm.cljk L15/L28・L38 silent zero-fill 不変)。NEXT は runner repair
(extension 戻し or loader 登録) + re-baseline を再発行。H1〜H70 全決着・未決残存なし。END
bench-243 (load 超過 skip) — HOST LOAD 15min ≈78.72 (≈6.6× ncpu=10) で Load gate 大幅超過のため
unmeasured (honest 据え置き)。HEAD giemon 00fd23f9d047 / robotics ad99366f 不変。test 試行は
高負荷下で 0/0/0 を観測したが測定として無効扱い・回帰 assert せず。falsify-034 残存のまま。

bench-247 (実測, 負荷 gate 内 15min ≈10.7 ≈1.1×) — bench-244/245/246 と同一 HEAD
(giemon 00fd23f / robotics ad99366) で kbb -M:test 再実測: 両 suite とも
「Ran 0 tests containing 0 assertions」RC=0 (silent-zero REGRESSION 持続・bench-244/245/246
と同値, 基準値 robotics 23/558/0・giemon 46/115/0 から -100% 不変)。0-test は緑でなく
suite 未実行と同等につき regression は bench-244/245 の measured RED を据え置き
(carry-over, 新規破れ assert せず)。falsify-069 (H70) の loadability 破れ結論と整合:
.cljk extension 起因の discovery+loadability 二重破れで復帰なし。falsify-034
(FK guard repair 未配線) は据え置き。新規 falsy なし。NEXT は runner repair
(extension 戻し or loader 登録) + re-baseline を再発行 (継続)。H1〜H70 全決着・未決残存なし。END
bench-248 (実測, 負荷 gate 内 15min ≈14.20 ≈1.4×) — bench-247 と同一 HEAD (giemon 00fd23f /
robotics ad99366) で kbb -M:test 再実測: 両 suite とも「Ran 0 tests containing 0 assertions」
RC=0 (silent-zero 持続・bench-244〜247 と同値, 基準値 robotics 23/558/0・giemon 46/115/0 から
-100% 不変, 4 連続)。0-test は緑でなく suite 未実行と同等につき regression は bench-244/245 の
measured RED を据え置き (carry-over, 新規破れ assert せず)。falsify-069 (H70) の loadability
破れ結論と整合 (.cljk extension 起因 discovery+loadability 二重破れ)。falsify-034 (FK guard
repair 未配線) は据え置き (arm.cljk L15/L28・L38 silent zero-fill 不変)。新規 falsy なし。
NEXT は runner repair (extension 戻し or loader 登録) + re-baseline を再発行 (継続)。
H1〜H70 全決着・未決残存なし。END

bench-253 (実測, 負荷 gate 内 15min ≈12.50 ≈1.3× ncpu=10) — bench-244〜252 と同一 HEAD (giemon 00fd23f / robotics ad99366) で kbb -M:test 再実測: 両 suite とも「Ran 0 tests containing 0 assertions」RC=0 (silent-zero 持続・10 連続, 基準値 robotics 23/558/0・giemon 46/115/0 から -100% 不変)。0-test は suite 未実行と同等につき regression は bench-244/245 の measured RED を据え置き (honest: unmeasured-equivalent, 新規破れ assert せず)。maturity.md NEXT の test-runner 修復 (cljk rename 後の silent-zero, kbb --classpath src:test + 明示 require による 21/52/0 緑は falsify-070 実測のまま) は解消されていない — 46/115 完全回復には deps floor (kotoba.lang.text / kotoba.robotics) 接続 + host interop (`catch Exception`) 修正が別途必要。falsify-034 (FK guard repair 未配線) は据え置き。新規 falsify なし (正本: H1〜H71 全決着・未決残存なし)。7 軸更新なし (全軸据え置き)。NEXT は runner repair + re-baseline を再発行 (継続)。END

bench-258 (measured, 負荷 gate 内 15min ≈12.70 ≈1.3× ncpu=10) — HEADs robotics
ad99366 / giemon 00fd23f 不変・tracked diff 空, kbb -M:test 両 suite とも 0/0/0
RC=0 (silent-zero 持続・bench-244〜258 で 13 連続)。基準値 robotics 23/558/0・
giemon 46/115/0 から -100% 不変。regression は bench-244/245 の measured RED を
据え置き (honest, 新規破れ assert せず)。falsify-072 (H73) refuted —「governor
silent-nil 修正は実装済み」は成り立たない: governor_test.cljk deftest 6 件中不正
kind/safety 負テスト 0 件・governor.cljk は rob/action 透過のまま (kaigo L25-27 /
ops L58-60), rejected レコード化の痕跡なし (robotics 本体は deps 先で静的範囲外)。
新規 falsify はこれのみ (H1〜H73 全決着・未決残存なし)。7 軸更新なし (全軸据え置き)。

=== NEXT ===
NEXT: test-runner 修復 — cljk rename 後の silent-zero (kbb -M:test 両 suite 0/0/0 RC=0、bench-244〜263 持続実測 (19 連続)、bench-264 は load-skip unmeasured) を解消し robotics 23/558/0・giemon 46/115/0 の実測緑を現 HEAD (robotics ad99366 / giemon 00fd23f) で再確立。falsify-070: kbb --classpath src:test + 明示 require で 21/52/0 緑 (第2測定経路)、46/115 完全回復には deps floor 接続 + host interop (`catch Exception`) 修正が別途必要。同時に falsify-071/072 (H72/H73) の governor silent-nil 経路 (不正 kind/safety が deny でなく nil で消える・負テスト 0 件) の rejected レコード化 + 負テスト 1 件追加を推奨。全ての bench/falsify の前提であり最優先修理。
bench-252 測定済み: silent-zero 持続 9 連続 (bench-244〜252 の各 measured; bench-243 のみ load-skip) (kbb -M:test 両 suite 0/0/0 RC=0、HEAD ad99366 / 00fd23f 不変・tracked diff 空) — 未解決につき NEXT 再発行継続。

falsify-070 (H71) refuted —「緑 runner は現状存在しない」は過剰主張 (実行系実測,
Load gate 内 15min ≈17.4 ≈1.7× ncpu=10, giemon HEAD 00fd23f 不変)。
kbb --backend sci --classpath src:test + 明示 require: loadable 4/9 ns
(arm/chassis/kinematics/viewer -test, RC=0) を run-tests →
**Ran 21 tests containing 52 assertions. 0 failures, 0 errors. RC=0 (measured 緑)**。
RC=1 5 ns の失敗は discovery でなく (a) deps floor (kotoba.lang.text / kotoba.robotics)
が kbb classpath 未接続、(b) host interop `catch Exception` (arm-edn-test L23)
解析不能。silent-zero (kbb -M:test 0/0/0) は runner/discovery 側の破れで
suite 自体は生存を再確定。NEXT (runner repair) に追記: kbb 経路を第 2 測定経路として
使用可・kbb -M:test 修正のみでは 46/115 に届かない (text/robotics 接続 +
interop 記法修正が別途必要)。H1〜H71 全決着。END

bench-250 (実測, 負荷 gate 内 15min ≈10 ≈1.9× ncpu=10) — bench-244〜248 と同一 HEAD (giemon 00fd23f / robotics ad99366) で kbb -M:test 再実測: 両 suite とも 0/0/0 RC=0 (silent-zero 持続・5 連続, 基準値 robotics 23/558/0・giemon 46/115/0 から -100% 不変)。0-test は suite 未実行と同等につき regression は bench-244/245 の measured RED を据え置き (honest: unmeasured-equivalent, 新規破れ assert せず)。falsify-070 (H71) refuted 測定と整合 — kbb 経路で 21/52/0 緑測定可能、kbb -M:test 側の runner/discovery 破れのみが残存。falsify-034 (FK guard repair 未配線) は据え置き。新規 falsy なし。NEXT は runner repair + re-baseline を再発行 (kbb 第2経路・deps floor・interop 追記)。H1〜H71 全決着・未決残存なし。END

bench-251 (実測, 負荷 gate 内 15min ≈11.2 ≈1.2× ncpu=10) — bench-244〜250 と同一 HEAD (giemon 00fd23f / robotics ad99366) で kbb -M:test 再実測: 両 suite とも「Ran 0 tests containing 0 assertions」RC=0 (silent-zero 持続・bench-244/245/246/247/248/250 に続き 6 連続, 基準値 robotics 23/558/0・giemon 46/115/0 から -100% 不変)。0-test は suite 未実行と同等につき regression は bench-244/245 の measured RED を据え置き (honest: unmeasured-equivalent, 新規破れ assert せず)。maturity.md NEXT の test-runner 修復は解消されていない (kbb 第2経路 21/52/0 緑は falsify-070 実測のまま)。falsify-034 (FK guard repair 未配線) は据え置き。新規 falsy なし。NEXT は runner repair + re-baseline を再発行 (継続)。H1〜H71 全決着・未決残存なし。END

bench-252 (実測, 負荷 gate 内 15min ≈15.82 ≈1.6× ncpu=10) — bench-244〜251 と同一 HEAD (giemon 00fd23f / robotics ad99366) で kbb -M:test 再実測: 両 suite とも「Ran 0 tests containing 0 assertions」RC=0 (silent-zero 持続・bench-244〜252 の各 measured で 9 連続, 基準値 robotics 23/558/0・giemon 46/115/0 から -100% 不変)。0-test は suite 未実行と同等につき regression は bench-244/245 の measured RED を据え置き (honest: unmeasured-equivalent, 新規破れ assert せず)。maturity.md NEXT の test-runner 修復 (cljk rename 後の silent-zero, kbb --classpath src:test + 明示 require による 21/52/0 緑は falsify-070 実測のまま) は解消されていない — 46/115 完全回復には deps floor (kotoba.lang.text / kotoba.robotics) 接続 + host interop (`catch Exception`) 修正が別途必要。falsify-034 (FK guard repair 未配線) は据え置き (arm.cljk L15/L28・L38 silent zero-fill 不変)。新規 falsify なし (正本: H1〜H71 全決着・未決残存なし)。7 軸更新なし (全軸据え置き — bench-252 は既知 silent-zero の持続 re-measured のみ)。NEXT は runner repair + re-baseline を再発行 (継続)。END
bench-262 (measured, silent-zero 持続 18 連続・負荷 ~1.5x 帯 gate 内) — HEAD giemon 00fd23f / robotics ad99366 不変・tracked diff 空、kbb -M:test 両 suite とも 0/0/0 RC=0 を再実測 (基準値 robotics 23/558/0・giemon 46/115/0 から -100% 不変、bench-244〜262 で 18 連続)。falsify-070 第2測定経路 (kbb --backend sci --classpath src:test + aliased t/run-tests — bare clojure.test/run-tests は sci で RC=1) を再実測し 21/52/0 緑 RC=0 を再現。falsify-034 (FK guard repair 未配線)・falsify-071/072 (governor silent-nil) 据え置き。回帰 assert なし (runner defect 持続 re-measured、新規破れなし)。NEXT は runner repair + re-baseline を再発行 (継続)。H1〜H74 全決着・未決残存なし。END

bench-263 (measured, silent-zero 持続 19 連続・負荷 ~1.2x 帯 gate 内) — HEAD robotics ad99366 /
giemon 00fd23f 不変、kbb -M:test 両 suite とも 0/0/0 RC=0 を再実測 (bench-244〜263 で 19 連続、
基準値 robotics 23/558/0・giemon 46/115/0 から -100% 不変)。kbb 第2経路は本走未実行 (falsify-070
の 21/52/0 緑が最終実測)。falsify-034 (FK guard repair 未配線)・falsify-069 (.cljk load 不能)・
falsify-071/072 (governor silent-nil・負テスト 0 件) 据え置き。回帰 assert なし (runner defect 持続
re-measured、新規破れなし)。NEXT は runner repair + re-baseline を再発行 (継続)。END

bench-264 (skipped, load 15min ≈91.81 ≈9.2× ncpu=10) — Load gate 大幅超過につき kbb -M:test
(robotics/giemon) と seeded 再現を省略し unmeasured (honest 据え置き)。基準値 robotics 23/558/0・
giemon 46/115/0 据え置き、回帰 assert せず。HEAD robotics ad99366 / giemon 00fd23f 不変
(bench-263 と同一)。silent-zero 持続の有無は本走未測定 (repaired / unchanged とも断定せず)。
falsify 新規なし。falsify-034 (FK guard repair 未配線)・falsify-069 (.cljk load 不能)・
falsify-071/072 (governor silent-nil・負テスト 0 件) 据え置き。NEXT は runner repair +
re-baseline を再発行 (継続)。H1〜H73 全決着・未決残存なし。END
bench-267 (measured, silent-zero 持継 24 連続・負荷 gate 内 15min 19.43 ≈1.9× ncpu=10) — HEAD robotics ad99366 / giemon 00fd23f 不変・tracked diff 空、kbb -M:test 両 suite とも 0/0/0 RC=0 を再実測 (基準値 robotics 23/558/0ヾgiemon 46/115/0 から -100% 不変、bench-244〜267 で 23 連綜)。回帰 assert なし (runner defect 持継 re-measured、新規破れなし)。falsify-034 (FK guard repair 未配線)・falsify-069 (.cljk load 不能)・falsify-071/072 (governor silent-nil・負テスト 0 件) 据え置き。falsify 新規なし (H1〜H74 全決着・未決残存なし)。7 軸更新なし (全軸据え置き)。NEXT は runner repair + re-baseline を再発行 (継綜)。END


bench-268 (measured, silent-zero 持続 24 連続・負荷 gate 内 15min 15.39 ≈1.54× ncpu=10) —
HEAD robotics ad99366 / giemon 00fd23f 不変・tracked diff 空、kbb -M:test 両 suite とも
0/0/0 RC=0 を再実測 (基準値 robotics 23/558/0・giemon 46/115/0 から -100% 不変)。
bench-265 (21 連続) / bench-266 (22 連続) も同様に silent-zero 持続 re-measured。
回帰 assert なし (runner defect 持続 re-measured、新規破れなし)。falsify-034 (FK guard repair
未配線)・falsify-069 (.cljk load 不能)・falsify-071/072 (governor silent-nil・負テスト 0 件) 据え置き。
falsify 新規なし (H1〜H74 全決着・未決残存なし)。7 軸更新なし (全軸据え置き)。
NEXT は runner repair + re-baseline を再発行 (継続)。END
