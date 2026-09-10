# falsify-045 — H46 (FK guard repair 未着手の再判定: forward-kinematics 本体に within-limits? 呼出が配線されたか)

- 連続番号: 045 (falsify-044 の後続)
- 日次: 260908
- 仮説 (H46, 反証対象「governor gate を迂回できるアクション列がないか (no LLM-to-actuator shortcut の検査)」の継続):
   NEXT (maturity.md) 未達項目「arm.cljc `forward-kinematics` (L22-41) 本体に `within-limits?` 呼出を配線し、
   越境 angle を silent 受理でなく拒否・クランプ・nil のいずれかで検証層に観測可能にせよ (FK guard repair、
   arm_test.cljc 20-22 の silent zero-fill 緑 assertion は期待値変更込み修正)」に対し、現行 blob が
   配線済み (FK 経路内から `within-limits?` が呼ばれる)となったか。
- 実測 (決定的、全文静的読取 — 実行 backend 不可につき純静的判定):
  - 測定時 HOST LOAD (pre-run script 11:04 実測): **19.82 / 28.42 / 34.08** (ncpu=10 の 15min ≈ 3.4×、Load gate
    15min ≥ 2×ncpu=20 を大きく超過)。さらに cron sandbox の terminal backend が本 run 全コマンド空出力
    (backend 応答不能)、execute_code も cron モードで拒否 — 重い test 実行は実行不能・応答不能リスク高のため
    省略し、read_file / search_files(grep) / .git/HEAD 直読の静的判定で決着 (falsify-042/043/044 と同一手法の
    厳格版)。テスト計数は unmeasured (honest 据え置き、数字捏造ゼロ)。
  - `search_files pattern="within-limits\?" path=src/` (実測): ヒット **arm.cljc L15 (defn) / L28 (docstring 言及)
    の 2 箇所のみ**。repo 全体 (src/ + test/) の呼出 (caller) 実像: arm_test.cljc L28-30 (単体テスト) のみで、
    FK 経路 (forward-kinematics / end-effector) からは **0 箇所**。
  - `read src/kotoba/giemon/arm.cljc` (121 行、byte 不変): `within-limits?` は **L15-20 定義** (lower/upper 比較)。
    `forward-kinematics` (L22-41) ループは `angle (or (first angles) 0.0)` (**L38 silent zero-fill**) のまま、
    `within-limits?` 呼出・クランプ・拒否・nil 配線 **なし**。docstring L27-29 自白「This is pure kinematics,
    not the safety gate … Check `within-limits?` first」。「missing angles default to 0.0」挙動不変。
    `end-effector` (L43-46) は FK を呼ぶのみ。
  - `read test/kotoba/giemon/arm_test.cljc` (test/ 配下、40 行): L20-22 "missing angles default to 0.0" 緑
    assertion (`forward-kinematics two-joint-arm [0.0 0.0]` == `forward-kinematics two-joint-arm []`) で
    silent zero-fill を緑固定。`within-limits-test` (L28-30) は FK 経由でなく直接呼ぶ単体のみ。
  - `read src/kotoba/giemon/governor.cljc` (68 行): 全関数は rob/mission・rob/action・rob/gate の安全クラス
    分類専用 — within-limits? / :joint/limit / torque / arm 力学参照 **0**、arm limit/torque 無接続のまま
    (no LLM-to-actuator shortcut 未成立のまま)。
  - `read .git/HEAD` (直読) = **d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe** (falsify-043/044 と同 一、不変)。
    arm.cljc ソース内容が falsify-043/044 記録と byte 一致 (tracked diff 空の静的確認)。pre-run script も
    未追跡 sim-loop/ のみで tracked 変更なし。git diff --stat は terminal backend 不能のため本 run では未実行
    (HEAD 不変 + ソース内容一致で tracked 変更なしの判定は静的に確定)。
- verdict: **refuted** — `within-limits?` は定義・単体テスト済みのまま FK 経路 (L22-41 / end-effector L43-46)
  内部から呼出 0 回、越境 angle は silent 受理され pose を返す (docstring 自白、arm_test L20-22 が zero-fill 緑
  固定、falsify-034/036/039/040/041/042/043/044 と同根)。governor は arm limit/torque 無接続 (参照 0) —
  no LLM-to-actuator shortcut 未成立の結論不変 (新規破れなし・回帰なし・コード変更なし)。本 bot は測定のみで
  修正しない。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  grep -rn "within-limits?" src/            # L15 def / L28 doc のみ、FK 経路 caller 0
  read src/kotoba/giemon/arm.cljc           # within-limits? L15 定義のみ、FK L31-41 呼出 0、L38 silent zero-fill
  read test/kotoba/giemon/arm_test.cljc     # L20-22 zero-fill 緑固定、L28-30 単体テスト (FK 経由でない)
  read src/kotoba/giemon/governor.cljc      # gate 安全クラス分類専用、arm/torque 参照 0
  cat .git/HEAD                             # d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe 不変
  uptime                                    # 15min 34.08 > 2×ncpu=20 → Load gate 超過、重い test 実行は省略
  ```
  注: 本 run は terminal backend 全コマンド空出力 (応答不能)・execute_code 拒否のため、上記のうち grep・
  read・cat 相当を read_file / search_files で実行した (同一静的結果)。git diff --stat / uptime の再測定も
  backend 回復後に可能。
- 検証内訳: 1 仮説 (H46) / 測定 5 (grep 1 + src 2 + test 1 + HEAD 1 全文静的読取、falsify-043/044 と同値) /
  判定 refuted。テスト計数は load + backend 不能で unmeasured (honest、据え置き)。
- コアへの 1 行: FK は依然 within-limits? を 0 回、越境 angles を silent 受理 (L38 silent zero-fill、
  arm_test L20-22 緑固定、HEAD d0d3cb4 系列不変)、governor は arm limit/torque 無接続のまま — repair は
  FK 経路への limit 検査配線が必須、本 bot は実装・変更なし。