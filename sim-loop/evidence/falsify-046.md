# falsify-046 — H47 (FK guard repair 未着手の再判定: forward-kinematics 本体に within-limits? 呼出が配線されたか)

- 連続番号: 046 (falsify-045 の後続)
- 日次: 260908
- 仮説 (H47, 反証対象「governor gate を迂回できるアクション列がないか (no LLM-to-actuator shortcut の検査)」の継続):
   NEXT (maturity.md) 未達項目「arm.cljc `forward-kinematics` (L22-41) 本体に `within-limits?` 呼出を配線し、
   越境 angle を silent 受理でなく拒否・クランプ・nil のいずれかで検証層に観測可能にせよ (FK guard repair、
   arm_test.cljc 20-22 の silent zero-fill 緑 assertion は期待値変更込み修正)」に対し、現行 blob が
   配線済み (FK 経路内から `within-limits?` が呼ばれる)となったか。
- 実測 (決定的、全文静的読取 — 実行 backend 不能につき純静的判定):
  - 測定時 HOST LOAD (pre-run script 12:04 実測): **14.85 / 13.33 / 13.18** (ncpu=10 の 15min ≈ 1.3× で
    Load gate 15min ≥ 2×ncpu=20 の**内側**)。ただし cron sandbox の terminal backend が本 run も全コマンド
    空出力 (`echo hello` すら空、応答不能)・execute_code が cron モードで拒否のため重い test 実行は不能
    (falsify-045 と同一条件)。判定は falsify-045 と同一の純静的読取手法で決着。テスト計数は unmeasured
    (honest 据え置き、数字捏造ゼロ)。
  - `read src/kotoba/giemon/arm.cljc` (121 行、byte 不変): `within-limits?` は **L15-20 定義**のみ (lower/upper 比較)。
    `forward-kinematics` (L22-41) ループは `angle (or (first angles) 0.0)` (**L38 silent zero-fill**) のまま、
    ループ内に `within-limits?` 呼出・クランプ・拒否・nil 配線 **0 箇所**。docstring L27-29 自白
    「This is pure kinematics, not the safety gate … an angle outside a joint's declared limit still produces
    a pose. Check `within-limits?` first」。`end-effector` (L43-46) は FK を呼ぶのみ。
  - `read test/kotoba/giemon/arm_test.cljc` (40 行): L20-22 "missing angles default to 0.0" 緑 assertion
    (`forward-kinematics two-joint-arm [0.0 0.0]` == `forward-kinematics two-joint-arm []`) で silent zero-fill
    を緑固定。`within-limits-test` (L28-30) は FK 経由でなく直接呼ぶ単体のみ。
  - `read src/kotoba/giemon/governor.cljc` (68 行): 全関数は rob/mission・rob/action・rob/gate の安全クラス
    分類専用 — within-limits? / :joint/limit / torque / arm 力学参照 **0**、arm limit/torque 無接続のまま
    (no LLM-to-actuator shortcut 未成立のまま)。
  - `read .git/HEAD` (直読) = **d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe** (falsify-043/044/045 と同一、不変)。
    arm.cljc / arm_test.cljc / governor.cljc のソース内容は falsify-045 記録と byte 一致 (静的確認、
    tracked diff 空の判定)。pre-run script も未追跡 sim-loop/ のみで tracked 変更なし。
- verdict: **refuted** — `within-limits?` は定義・単体テスト済みのまま FK 経路 (L22-41 / end-effector L43-46)
  内部から呼出 0 回、越境 angle は silent 受理され pose を返す (docstring 自白、arm_test L20-22 が zero-fill 緑
  固定、falsify-034/036/039/040/041/042/043/044/045 と同根・**10 連続**)。governor は arm limit/torque 無接続
  (参照 0) — no LLM-to-actuator shortcut 未成立の結論不変 (新規破れなし・回帰なし・コード変更なし)。
  本 bot は測定のみで修正しない。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  grep -rn "within-limits?" src/            # L15 def / L28 doc のみ、FK 経路 caller 0
  read src/kotoba/giemon/arm.cljc           # within-limits? L15 定義のみ、FK L31-41 呼出 0、L38 silent zero-fill
  read test/kotoba/giemon/arm_test.cljc     # L20-22 zero-fill 緑固定、L28-30 単体テスト (FK 経由でない)
  read src/kotoba/giemon/governor.cljc      # gate 安全クラス分類専用、arm/torque 参照 0
  cat .git/HEAD                             # d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe 不変
  uptime                                    # 本 run 15min 13.18 < 2×ncpu=20 (gate 内) だが backend 応答不能で実行不能
  ```
  注: 本 run は terminal backend 全コマンド空出力 (応答不能)・execute_code 拒否のため、上記のうち grep・
  read・cat 相当を read_file で実行した (同一静的結果)。git diff --stat / uptime の再測定は backend 回復後に可能。
- 検証内訳: 1 仮説 (H47) / 測定 4 (src 1 + test 1 + governor 1 + HEAD 1 全文静的読取、falsify-045 と同値) /
  判定 refuted。テスト計数は backend 不能で unmeasured (honest、据え置き)。
- コアへの 1 行: FK は 10 run 連続で still within-limits? を 0 回、越境 angles を silent 受理 (L38
  silent zero-fill、arm_test L20-22 緑固定、HEAD d0d3cb4 系列不変)、governor は arm limit/torque 無接続のまま —
  repair は FK 経路への limit 検査配線が必須、本 bot は実装・変更なし。