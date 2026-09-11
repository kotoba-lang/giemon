# giemon sim-loop 成熟度 (status/maturity.md — 正本)

集計元: sim-loop/evidence/ bench-001〜241 / falsify-001〜067 (決定的計算、
後続 bench-068〜241 は測定 / skipped (load gate 15min≥2×ncpu=20 超過、backend 応答不能)
の混合 — 最新完走実測は bench-238/239 (giemon 46/115/0 @ d0d3cb4 不変、robotics 23/558/0
@ 893ef76: HEAD 進行 396fc33→893ef76 に伴う suite 拡張 3 namespace、failures 0 で赤回帰なし)、
bench-241 は load gate 超過 (15min 79.48) skipped (honesty-first)。giemon 基準値保持の
判定は bench-066/068 で確定、robotics 基準値は bench-238/239 で 23/558/0 に更新)
判定基準: ADR-2608052000 (7 軸)。Otete のみ成熟度に数える
(Hitogata/Caterpillar の in-design 成果は実装済みと評価しない)。

## 現在段階

- **L0** — sim-loop 学習ジョブ (seed / L1 以降) は giemon リポジトリ内に未実装
  (src+test の .clj* への seed/learn/train 該当 0 件、bench-062〜067 で git diff 空 /
  git log 直近 d0d3cb4 同一を機械再確認)。L1 昇格条件未達。
  既存決定関数の 2 回実行一致 (軽量 seeded 再現 surrogate) のみ。
  ladder を飛ばして L1 以降を宣言することはしない。

## 7 軸スコア

| 軸 | 項目 | 評価 | 根拠 (evidence から決定的計算) |
|---|---|---|---|
| 1 | テスト健全性 | 緑 | robotics 23 tests / 558 assertions / 0 failures @893ef76 (bench-238/239 完走実測、HEAD 進行に伴う suite 拡張で 14/50→23/558、failures 0 で赤回帰なし)、giemon 46 tests / 115 assertions / 0 failures。bench-001→239 の完走 run で同一数字 (回帰 0、負荷 5〜180+ でも同一性 64 点確認 — bench-059 は test 時 load 10〜20 / 1min 12、bench-060 は load 7.16〜8.16 / 5min 9.2 / 15min 12.1、bench-061 は load 9.43 / 5min 7.92 / 15min 9.2、bench-062 は load 12.18 / 5min 10.27 / 15min 9.75、bench-063 は load 31.77 / 5min 32.04 / 15min 24.43 の高負荷、bench-056 はテスト前後 load 92〜180 でも同一、bench-066 は開始時 1min 59.75 / 5min 56.97 / 15min 79.07 → 終了時 84.34 / 76.18 / 79.33 (ncpu=10) の高負荷で 2 スイートとも exit 0)。bench-064〜065 は load 超過 (188 / 92〜116)、bench-067 は load 1min 74〜99 持続・上昇 (5 秒間隔でも 92.70 → 99.45) で test スイート実行を skipped (honesty-first、決定的数字を捏造せず skipped 記録。基準値保持の判定は bench-066 再検証で回帰なしを確定) |
| 2 | 決定性 / seeded 再現 | 黄 | SEED-PARITY true を bench-002〜068 の完走 run で確認 (:xf/pos 同一、bench-066 で再確認、bench-068 で seeded 再現一致)。bench-064〜065/067 は load 超過で seeded 再現未実行 (skip のため点カウント外)。ただし学習ジョブ不在につき「既存決定関数の 2 回実行一致」に限る — 減点事由。falsify-016: 姿勢付き surrogate も 16/16 決定的。falsify-017 により normalize アンダーフロー域での潜在赤あり (現 fixture 軸は安全) |
| 3 | パリティ / 検証自動化 | 赤 | URDF↔EDN 静的 parity は mismatches 0 (falsify-001) だが parity oracle (`from_edn==parse_urdf`) の Clojure 自動検証は未実装 (falsify-001/008 再確認)。caterpillar URDF は XML コメント内 `--` (line 9) で well-formed でなく parse 不能 — falsify-009 により原因はコメント 1 箇所のみ、コメント除去後は well-formed・EDN と mismatch=0、修正は 1 行。offdiag 0-default は数値一致するが strict 読みでは 6/7 link で落ちる暗黙契約のまま (falsify-008) |
| 4 | 安全性 / governor 面 | 赤 | gate↔arm torque 照合未接続が入力空間全面で決定的: falsify-002 (gate は :action/params 無検査)、falsify-010 (750 ケース、torque 1e6/負値でも decision 変化 0)、falsify-011 (:joints map 54 ケース、j99・型混在・非数値も全受理、torque を引数に取る arm 公開関数 0/8)、falsify-012 (構造エッジ 140 ケース、5 層深入れ tau も permit)、falsify-013 (allowed-set 契約+governor 層+id 型 21 ケース、payload 滅菌点は全経路に不在)、falsify-014 (文字列化/別名ンキー/バッチ 14 ケース)、falsfiy-015 (gate :permit 下流面に payload 消費者 0)。安全側要素: sign-off クラス硬コードは正しく機能、safety-critical :emit は payload 付きでも :deny、型違反は :invalid 一様拒否 (falsify-002/012/013) |
| 5 | ベンチ計測 | 黄 | falsify-001〜009 の 9 段階計測: 静的 (2.73 N·m / payload 3 kg で 18.6 < cont 40) → quasi-dynamic (k≈9.8–11.6x) → full dynamic (falsify-003 コリオリ k≈1.4–3.8x、ただし falsify-004 の I·α² 次元誤りを falsify-005 が撤回、falsify-006 で RMS デューティ評価に修正 → k_rms≈3.8–8.3x) → 宣言範囲制約付き → 対象関節拡大 (falsify-007 j1/j5: k≈6.2x 以上) → 姿勢族 (falsify-016: f=1.0/q2=0 が最悪で k_rms_j2=10.40、realistic DR k≈1.2 に対し 8 倍以上の余裕)。残る限界: 点質量モデル (exact RNEA 未実施、破れ点は下限値) |
| 6 | 反証 (falsify) 進捗 | 黄 | H1〜H25 のうち refuted: H2/H3 (FK 正しい・隠れ underrated なし)、H5→H7/H8 の一連の過大評価是正 (最終的に realistic DR k では j2/j5 とも破れず)、H11 の本体仮定 (URDF 本体も壊れている → コメント 1 箇所のみと是正)、H19 (normalize アンダーフローで無正規化・回転偏差 1.0 rad、例外なし — 潜在赤)、H20 (BOM by-name last-wins で重複名 rating 誤対応 + weak→strong 重複で underrated-joints が false-pass — 将来経路で発火)、H21 (actuator 欠落 joint が headroom 行から消え underrated-joints が空で通過 — false-pass、将来経路で発火)、H23 (:joint/limit :velocity は FK/within-limits?/torque-headroom/bom/gate どこでも未消費 = 速度制限強制面の不在)、H24 (within-limits? の limit 欠落面 — 45 ケース列挙で誤受理 0、欠落/nil/逆転は全 pose false-reject 保守側、型混在は CCE loud、src 実行経路なし)、H25 (`within-limits?` caller 不在 — 全 src .cljc 参照は arm.cljc 定義15+FK docstring28 のみで実行呼び出し無し、FK は範囲外角 (upper+50) / limit 欠落 joint を無検証受理 = RANGE 強制面の不在、型混在は CCE loud)、H26 (falsify-024: FK は角度列と chain 長の不一致を検証しない — loop 終端 `(empty? chain)` のみ、短い列は `(or (first angles) 0.0)` でゼロ充填・長い列は末尾を静かに捨てる = 形状強制面の不在、silent false-pass、型混在のみ CCE loud)、H27〜H68 (FK guard repair 未配線の再検証系列 falsify-034/036/039〜067、29 連続 refuted — HEAD d0d3cb4 不変・tracked diff 空、within-limits? の FK 経路内呼出 0 回 / L38 silent zero-fill 不変 / governor.cljc 接続 0 行の機械再確認))。survived: H4/H12〜H18、H22 (falsify-020、`:joint/limit` 欠落/:effort nil はいずれも NPE で loud、false-pass なし)。 |
| 7 | evidence 整合性 | 黄 | bench-001〜241 + falsify-001〜067 (多数 run を含む; bench-064〜065 は load 超過 (188 / 92〜116)、bench-067 は load 1min 74〜99 持続・上昇 (5 秒間隔 92.70 → 99.45) で skipped の honesty 記録、測定の再実行なし。決定的(成功)記録は 86 件 (bench-001〜063,066 + falsify-001〜023)、honesty skipped は 064/065/067 の 3 件)。probe は evidence 配下の測定専用 (コード修正なしを維持)。tmp_*.py debug 残骸 5 件あり (rm block のため残留、実験本体に影響なし)。caterpillar fixture 赤の OPEN は falsify-009 により「最小修正 1 行」と特定済み。bench-062 は中負荷 (load 12.18 / 5min 10.27 / 15min 9.75)、bench-063 は高負荷 (load 31.77 / 5min 32.04 / 15min 24.43) でも同一結果 + :xf/pos 一致を確認 (bench-061 は load 9.43 / 5min 7.92 / 15min 9.2、bench-056 は load 92〜180、falsify-020 は load 49〜57 で 2 回実行一致)、falsify-022 は load 53.91/45.61/41.73 で 2 回実行 byte 一致、falsify-023 は純 FK 数値計算 (load 非依存) で 2 回実行 byte 一致 (cmp_rc=0)、bench-066 は開始時 load 59.75 → 終了時 84.34 で 2 スイート exit 0 + seed parity 一致を確認 (ncpu=10) |

## OPEN (赤)

- URDF parse parity 自動検証 (from_edn==parse_urdf) の Clojure 実装が存在しない
  (falsfy-001/008/009)。caterpillar URDF は XNL コメント内 `--` の 1 箇所 (line 9)
  が原因 — falsify-009 によりコメント除去後は well-formed・EDN と mismatch=0、
  fixture 修正は 1 行 (`--` → `:` 等) で済むことが特定済み (コード修正はコア側)。
- gate↔arm の torque 照合未接続 (falsify-002/010〜015 で入力空間全面決定的)。
  torque 余裕照合層の実装自体が存在しない「不在」の赤 (コア側実装対象)。
- H19/H20/H21 の要修理点 (k/normalize アンダーフロー zero 分岐誤判定、
  BOM joint 名重複の last-wins 衝突解決と false-pass、actuator 欠落 joint の
  検証母集団からの静かな脱落) — 現 fixture では顕在化せず、
  DR/importer/variant の将来経路で発火する潜在契約破れ (コア側修理対象)。
- H23 — `:joint/limit :velocity` は arm/kinematics/governor/export/ui/viewer の
  どこにも読まれない「不在の安全面」 (falsify-021) — 速度制限 (rad/s) 強制が
  実行経路に無い潜在赤 (現 API に速度入力面なしのため現 fixture では非発火、
  速度安全を取り扱う導入判断はコア側)。
- H24 — `within-limits?` の「limit 未宣言」と「範囲超過」を共に false に
  折り畳む意味的 conflate (falsify-022) — 誤受理ゼロ (false-pass なし) で
  安全側だが、未宣言 joint の RANGE 検証は全 pose false-reject で静かに
  失われる否定方向の面 (H23 の velocity 不在と同型の潜在面、単一の
  RANGE 検証述語自体には src 実行経路なし — 導入判断はコア側)。
- H25 -- `within-limits?` が唯一の RANGE 検証だが src caller 不在 (falsify-023)
  -- FK は範囲外角 (upper+50 rad)/limit 欠落 joint を無検証・無例外で `:xf/pos`
  に受理し、全 src .cljc の within-limits? 参照は arm.cljc 定義行 15 + FK docstring のみ
  (実行呼び出し無し) = **ジョイント角 RANGE 強制面の不在** の潜在赤。型混在 (string) 角は
  CCE loud で false-pass にはならない (現 API に入力面なしのため現 fixture では非発火、
  FK への pre-check / within-limits? の gate 接続はコア側導入判断)。
- FK guard repair 未配線 (falsify-034/036/039〜067 の 29 連続 refuted)。`within-limits?`
  は arm.cljc 定義 L15-20・docstring・単体テストのみで FK 経路 (forward-kinematics
  L22-41 / end-effector L43-46) 内部呼出 0 回、L38 `(or (first angles) 0.0)` の
  silent zero-fill と越境 angle silent 受理が HEAD d0d3cb4 不変のまま未修理 —
  修理 (配線 + arm_test L20-22 期待値変更) はコア側実装対象の継続 NEXT。

## NEXT

- NEXT: FK guard repair — `forward-kinematics`/`end-effector` 経路に `within-limits?`
  を配線し、越境 angle を silent 受理でなく fail-loud (拒否/クランプ) にする
  (arm_test L20-22 の zero-fill 緑固定期待値の変更込み)。
  falsify-024 (H26: FK は角度列と chain 長の不一致を検証しない = 形状強制面の不在、
  短い列ゼロ充填 / 長い列末尾静かに捨て) で確定した形状面と falsify-034/036/039〜067
  (H27〜H68) の **29 連続 refuted** (HEAD d0d3cb4 不変・tracked diff 空) を受けた
  再発行。修理 > 新機能 — 実装されるまで NEXT を前進させない。
  本 bot は実装しない (falsify-068 として再検証を記録するまで繰り返す)。

## 前回までの NEXT 履歴 (実施済み / 役割外として記録)

- falsify-002〜009 は測定 probe のみで実施済み (fixture 修正はコア側)。
  gate↔arm torque 照合未接続赤の深掘り probe は falsify-010〜015 で input 空間
  全面 (grid 750 / :joints 54 / 構造 140 / 契約 21 / 拡大 14 / permit 面 11
  ケース) まで決定的に網羅済み — 同系 probe の追加は不要。
- caterpillar URDF の XML コメント内 `--` 修正と parity oracle (from_edn==parse_urdf)
  の Clojure 実装はコード修正を伴うためコア側対応 (falsify-009 により最小修正
  1 行と特定済み、実施待ち)。
- sim 受付口 torque 照合入力空間拡大 probe → falsify-011〜015 として実施済み。
- DR 初期姿勢 worst-case × seeded 再現組合せ probe → falsify-016 として実施済み。
- H19 (normalize アンダーフロー) → falsify-017 として実施済み (refuted、
  閾値ガード修理はコア側)。
- H20 (BOM joint 名重複 false-pass) → falsify-018 として実施済み (refuted)。
- H21 (actuator 欠落 joint の静かな検証脱落) → falsify-019 として実施済み
  (refuted、chain joint 数と headroom 行数の一致チェック要修理はコア側)。
- H22 (torque-headroom `:joint/limit` 欠落面) → falsify-020 として実施済み
  (survived — 欠落は NPE loud、false-pass なし。修理は不要、H21 側に集中)。
- H23 (`:joint/limit :velocity` 消費面) → falsify-021 として実施済み (refuted —
  velocity は FK/within-limits?/torque-headroom/bom/gate どこでも未消費で値
  {3/欠落/"high"/1000} に無反応、速度制限強制面が存在しない潜在赤。コア側は
  速度安全面の扱い要判断)。
- H24 (`within-limits?` の limit 丸ごと欠落面) → falsify-022 として実施済み
  (refuted — 45 ケース (9 limit 変種 × 5 角) で誤受理 0。欠落/nil/逆転の
  6 変種は全 pose constant-false (false-reject 保守側、false-pass なし)、
  型混在 (string) は ClassCastException loud、`within-limits?` には src 実行
  経路がない。否定方向の意味的 conflate のみ潜在面 → 単一 RANGE 検証の
  caller 不在 (H25) へ)。
- H25 (`within-limits?` caller 不在 / ジョイント角 RANGE 強制面の不在) →
  falsify-023 として実施済み (refuted — FK は各 joint upper+50 rad の範囲外角・
  limit 丸ごと欠落 joint の角度列を無検証・無例外で `:xf/pos` に受理、全 src .cljc
  の within-limits? 参照は arm.cljc 定義行 15 + FK docstring のみで実行経路無し。
  型混在 (string) 角は CCE loud で false-pass にはならない。RANGE 強制面の導入判断
  (FK pre-check / within-limits? の gate 接続) はコア側)。

- H26 (FK 角度列形状検証面の不在) → falsify-024 として実施済み (refuted —
  loop 終端 `(empty? chain)` のみ、長さ検査行なし、短い列 0.0 充填・長い列静かに捨て。
  長さ guard の導入判断はコア側)。以後の falsify-025〜067 は FK guard repair の
  「着手されたか」再検証系列で全て refuted (29 連続、HEAD d0d3cb4 不変)。
- bench-068〜241 は測定 / skipped 記録のみ — giemon 46/115/0 基準値保持、
  robotics は bench-238/239 で 23/558/0 @893ef76 に更新 (suite 拡張・赤回帰なし)、
  bench-241 は load gate 超過 skipped。新規 refute は falsify-024 (H26) のみ。
- bench-056〜063 (2026-09 cron 基準) は測定のみ追加 — 新規 refute・戦略変化なし。
  bench-062 は中負荷 (load 12.18 / 5min 10.27 / 15min 9.75)、bench-063 は高負荷
  (load 31.77 / 5min 32.04 / 15min 24.43) でテスト・軽量 seeded 再現の同一性を
  維持 (bench-061 は load 9.43 / 5min 7.92 / 15min 9.2)。
- bench-064〜065 (2026-09-06) は load 1min 188 / 92〜116 の極端負荷で test スイート・seeded 再現
  とも skipped (honesty-first、決定的数字を捏造せず skipped 記録)。新規 refute なし、
  スコア不変。bench-063 値 (robotics 14/50/0、giemon 46/115/0) を基準に
  load < 60 へ落ちた後の再検証を待機。
- bench-066 (2026-09-06) で再検証成功 — 開始時 load 1min 59.75 / 5min 56.97 /
  15min 79.07 が条件ぎりぎりで通常実行を試行、測定中 59.75 → 84.34 へ上昇したが
  2 スイートとも exit 0 (robotics 14/50/0、giemon 46/115/0) + seed parity 一致
  (:xf/pos 63 点目)。回帰なし・スコア不変を確定。新規 refute ・戦略変化なし
  (probe/falsify 再実行は省略、falsify-023 (H25) は 2026-09-06 に純 FK probe で実施済み)。
- **bench-067 (2026-09-06)** は load 1min 74〜99 持続・上昇 (5 秒間隔でも 92.70 → 99.45、
  bench-064 で設定した再実行条件 load 1min < 60 を超過) で test スイート・seeded 再現とも
  skipped (honesty-first)。決定的数字を捏造せず skipped 記録、git head d0d3cb4 不変を確認。
  新規 refute ・スコア不変。基準値 (robotics 14/50/0、giemon 46/115/0) は bench-066 確定値。
  load < 60 に落ちた後の再検証 (:xf/pos 64 点目相当) を bench-068 で実施予定。