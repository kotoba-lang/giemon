# falsify-043 — H44 (FK guard repair 未着手の再判定: forward-kinematics 本体に within-limits? 呼出が配線されたか)

- 連続番号: 043 (falsify-042 の後続)
- 日次: 260908
- 仮説 (H44, 反証対象「governor gate を迂回できるアクション列がないか (no LLM-to-actuator shortcut の検査)」の継続):
   NEXT (maturity.md) 未達項目「arm.cljc `forward-kinematics` (L22-41) 本体に `within-limits?` 呼出を配線し、
   越境 angle を silent 受理でなく拒否・クランプ・nil のいずれかで検証層に観測可能にせよ (FK guard repair、
   arm_test.cljc 20-22 の silent zero-fill 緑 assertion は期待値変更込み修正)」に対し、現行 blob が
   配線済み (FK 経路内から `within-limits?` が呼ばれる)となったか。
- 実測 (決定的、全文静的読取 — 実行 backend 不要):
  - 測定時 HOST LOAD (pre-run 9:05): **59.00 / 47.07 / 51.64** (ncpu=10 の 15min ≈ 5.9×、Load gate
    15min ≥ 2×ncpu=20 を超過)。純静的読取のため実行 backend 不要で完遂 (bench load-skip と独立)。cron sandbox の
    terminal backend 応答不能 (search_files sandbox 起動待ち、execute_code cron blocked) のため read_file 全文読取で
    静的判定 (falsify-042 と同一手法)。
  - `read src/kotoba/giemon/arm.cljc` (121 行): `within-limits?` は **L15-20 定義のみ** (下限/上限比較)。
    `forward-kinematics` (L22-41) のループは `angle (or (first angles) 0.0)` (**L38 silent zero-fill**) のまま、
    `within-limits?` 呼出・クランプ・拒否・nil 配線 **なし** (L31-41 確認)。docstring L27-29 自白「This is
    pure kinematics, not the safety gate … Check `within-limits?` first」。`end-effector` (L43-46) は FK を呼ぶのみ。
    `within-limits?` 参照は **L15 (def) / L28 (doc)** の 2 箇所のみ。
  - `read test/kotoba/giemon/arm_test.cljc` (40 行): L20-22 "missing angles default to 0.0" 緑 assertion
    (`forward-kinematics [0.0 0.0]` == `forward-kinematics []`) で silent zero-fill 緑固定。
    `within-limits-test` (L28-30) は FK 経由でなく直接呼ぶ単体のみ。
  - `read src/kotoba/giemon/governor.cljc` (68 行): 全 6 関数は gate 安全クラス分類専用で arm / within-limits? /
    torque / joint limit 参照 **0** — arm limit/torque 無接続のまま。
  - `read src/kotoba/giemon/kinematics.cljc` (67 行): 純 3-D 変換数学のみ、`within-limits?` 参照なし。
  - 上記 4 ファイルは falsify-042/041 のスナップショットと完全一致 → blob 不変・tracked diff 空 (HEAD
    d0d3cb4 系列据え置き、terminal 不能で rev-parse 未達 — 内容同一で代置)。
- verdict: **refuted** — `within-limits?` は定義・単体テスト済みのまま FK 経路 (L22-41 / end-effector L43-46)
   内部から呼出 0 回、越境 angle は silent 受理され pose を返す (docstring 自白、falsify-034/036/039/040/041/042
   と同根)。arm_test L20-22 は zero-fill 緑固定のまま。governor は arm limit/torque 無接続 (参照 0) —
   no LLM-to-actuator shortcut 未成立の結論不変 (新規破れなし・回帰なし・コード変更なし)。本 bot は測定のみで
   修正しない。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  read src/kotoba/giemon/arm.cljc          # within-limits? L15 定義のみ、FK L31-41 呼出 0、L38 silent zero-fill
  read test/kotoba/giemon/arm_test.cljc    # L20-22 zero-fill 緑固定、L28-30 単体テスト (FK 経由でない)
  read src/kotoba/giemon/governor.cljc     # gate 安全クラス分類専用、arm/torque 参照 0
  read src/kotoba/giemon/kinematics.cljc   # 純 3-D 変換数学、within-limits? 参照なし
  uptime                                   # Load gate 超過なら重い test 実行は省略 (bench policy)
  git rev-parse HEAD; git diff --stat      # d0d3cb4 系列不変・tracked diff 空 (terminal 復旧時の確認命令)
  ```
- 検証内訳: 1 仮説 (H44) / 測定 4 (src 3 + test 1 全文静的読取、falsify-042 と同値) / 判定 refuted。
- コアへの 1 行: FK は依然 within-limits? を 0 回、越境 angles を silent 受理 (L38 silent zero-fill、
   L20-22 緑固定、HEAD d0d3cb4 系列不変)、governor は arm limit/torque 無接続のまま — repair は FK 経路
   への limit 検査配線が必須、本 bot は実装・変更なし。