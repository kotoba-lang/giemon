# falsify-042 — H43 (FK guard repair 未着手の再判定: forward-kinematics 本体に within-limits? 呼出が配線されたか)

- 連続番号: 042 (falsify-041 の後続)
- 日次: 260908
- 仮説 (H43, 反証対象「governor gate を迂回できるアクション列がないか (no LLM-to-actuator shortcut の検査)」の継続):
   NEXT (maturity.md) 未達項目「arm.cljc `forward-kinematics` (L22-41) 本体に `within-limits?` 呼出を配線し、
   越境 angle を silent 受理でなく拒否・クランプ・nil のいずれかで検証層に観測可能にせよ (FK guard repair、
   arm_test.cljc 20-22 の silent zero-fill 緑 assertion は期待値変更込み修正)」に対し、現行 blob が
   配線済み (FK 経路内から `within-limits?` が呼ばれる)となったか。反証は「配線されず、
   `within-limits?` は定義のまま FK 内呼出 0 回で、越境 angles が silent 受理され pose を返す」のとき。
- 実測 (決定的、全文静的読取 — 実行 backend 不要、捏造なし):
  - 測定時 HOST LOAD (pre-run 8:04): **27.99 / 30.04 / 25.99** (ncpu=10 の 15min ≈ 2.8×)。本 falsify は純静的読取のため
    実行 backend 不要で完遂、load 超過/unmeasured の bench policy (bench-133～139) とは独立。
    なお本 cron sandbox の terminal backend が応答不能 (全 command 空出力、search_files は sandbox 起動待ち) のため、
    grep/git の代わりに **全対象ファイルを read_file で全文読取**して静的判定した (ripgrep と等価以上に決定的 — 全行可視)。
  - `read src/kotoba/giemon/arm.cljk` (全文 121 行): `within-limits?` は **L15-20 定義**のみ。
    `forward-kinematics` 本体 (L31-41) のループは `angle (or (first angles) 0.0)` (**L38 silent zero-fill**) のまま、
    `within-limits?` 呼出・クランプ・拒否・nil の配線は **なし** (L31-41 全行確認)。
    docstring L27-29 が自白「This is pure kinematics, not the safety gate: an angle outside a joint's declared
    limit still produces a pose. Check `within-limits?` first if that matters to the caller.」
    `end-effector` (L43-46) は FK を呼ぶのみで検査なし。`within-limits?` の参照は本ファイル内 **L15 (def) / L28 (doc)** の 2 箇所のみ。
  - `read src/kotoba/giemon/governor.cljk` (全文 68 行): 全 6 関数 (kaigo-mission / kaigo-action / fall-detected-alert /
    ops-mission / ops-action / chemical-dispense-alert) は kotoba.robotics gate の安全クラス分類専用で、
    arm / within-limits? / torque / joint limit への参照は **0** — arm limit/torque に無接続のまま。
  - `read src/kotoba/giemon/kinematics.cljk` (全文 67 行): 純 3-D 変換数学 (v+/v-/v*s/dot/cross/norm/normalize/
    mat3-mul/axis-angle->rot/combine/joint-transform) のみ、`within-limits?` 参照なし。
  - `read test/kotoba/giemon/arm_test.cljk` (全文 40 行): **L20-22 "missing angles default to 0.0"** 緑 assertion
    (`forward-kinematics [0.0 0.0]` == `forward-kinematics []`) が silent zero-fill を現行どおり緑固定。
    `within-limits-test` (L28-30) は `within-limits?` を **FK 経由でなく直接**呼ぶ単体テストのみ。
  - 上記 4 ファイルの内容・行番号はいずれも falsify-041 (H42) のスナップショットと **完全一致** → blob 不変、
    tracked diff 空 (HEAD giemon d0d3cb4 系列 d0d3cb45 据え置き、terminal 不能のため rev-parse 再実行は未達 — 内容同一で代置)。
- verdict: **refuted** — 仮説 (「FK guard repair が配線済み」)は不成立。`within-limits?` は arm.cljc L15 定義・
   arm_test.cljc L28-30 単体テスト済みのまま、FK 経路 (forward-kinematics L22-41 / end-effector L43-46)内部からは
   **0 回**も呼ばれない。越境 angle は silent に受理され世界変換 (pose) を返す (docstring L27-29 が自白、
   falsify-034/036/039/040/041 と同根の既知点)。arm_test.cljc L20-22 は silent zero-fill を緑固定のまま。
   governor 層 (governor.cljc) も arm limit/torque に無接続 (参照 0) —「no LLM-to-actuator shortcut」は FK 層で
   未成立という falsify-039/040/041 の結論は**不変** (新規破れ検出なし、回帰なし、コード変更なし)。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  read src/kotoba/giemon/arm.cljk          # → within-limits? は L15 定義のみ、FK L31-41 に呼出 0、L38 silent zero-fill
  read test/kotoba/giemon/arm_test.cljk    # → L20-22 zero-fill 緑固定、L28-30 単体テスト (FK 経由でない)
  read src/kotoba/giemon/governor.cljk     # → gate 安全クラス分類専用、arm/torque 参照 0
  read src/kotoba/giemon/kinematics.cljk   # → 純 3-D 変換数学、within-limits? 参照なし
  uptime                                   # → Load gate (15min ≥ 2×ncpu=20) 超過なら重い test 実行は省略 (bench policy)
  git rev-parse HEAD; git diff --stat      # → d0d3cb4 系列不変・tracked diff 空 (terminal 復旧時の確認命令)
  ```
- 検証内訳 (本 walk の 1 仮説・1 実測判定): 1 仮説 (H43) / 測定 4 (src 3 件 + test 1 件の全文静的読取、いずれも
   falsify-041 と同値) / 判定 refuted (FK guard repair 未配線)。
- コアへの 1 行: FK (`forward-kinematics` L22-41 / end-effector L43-46) は依然 `within-limits?` を 0 回、
   越境 angles を silent 受理で pose 返却 (L38 silent zero-fill、arm_test L20-22 緑固定、falsify-039/040/041 と同根、
   HEAD d0d3cb4 系列不変)、governor は arm limit/torque に無接続のまま — repair は FK 経路 (または
   gate<->arm 照合)への limit 検査配線が必須、本 bot は実装・変更なし。