# falsify-041 — H42 (FK guard repair 未着手の再判定: forward-kinematics 本体に within-limits? 呼出が配線されたか)

- 連続番号: 041 (falsify-040 の後続)
- 日次: 260908
- 仮説 (H42, 反証対象「governor gate を迂回できるアクション列がないか (no LLM-to-actuator shortcut の検査)」の継続):
   NEXT (maturity.md) 未達項目「arm.cljc `forward-kinematics` (L22-41) 本体に `within-limits?` 呼出を配線し、
   越境 angle を silent 受理でなく拒否・クランプ・nil のいずれかで検証層に観測可能にせよ (FK guard repair、
   arm_test.cljc 20-22 の silent zero-fill 緑 assertion は期待値変更込み修正)」に対し、現行 blob が
   配線済み (FK 経路内から `within-limits?` が呼ばれる)となったか。反証は「配線されず、
   `within-limits?` は定義のまま FK 内呼出 0 回で、越境 angles が silent 受理され pose を返す」のとき。
- 実測 (決定的、静的読取 + grep 実測数、実行 backend 不要のため REPL は走らせず — 捏造なし):
  - 測定時 HOST LOAD (7:08): **18.91 / 20.37 / 24.20** (ncpu=10 の 15min ≈ 2.4×)。本 falsify は純静的読取
    (grep 2 本 + read) のため実行 backend 不要で完遂、load 超過/unmeasured の bench policy (bench-135/136) とは独立。
  - `grep -rn 'within-limits?' src/ test/` (実測): **4 行のみ、うち FK 経路内呼出は 0**。
    内訳: arm.cljc L15 (定義)/ L28 (docstring 言及)/ arm_test.cljc L29, L30 (単体テスト 2 行)。— falsify-039/040 と**同値**。
  - `read src/kotoba/giemon/arm.cljc L22-41`: `forward-kinematics` 本体のループは `angle (or (first angles) 0.0)` (L38
    silent zero-fill) のまま、`within-limits?` 呼出・クランプ・拒否・nil の配線は**なし** (L31-41 全行確認)。
    `end-effector` (L43-46) は FK を呼ぶのみで FK に検査はない。
  - git 状態: HEAD **d0d3cb45** (不変, falsify-040 bench-120 から)、`git diff --stat` 空 (tracked 変更なし)、
    `git status --short` は `?? sim-loop/` 未追跡のみ — FK guard repair は依然**未着手**。
- verdict: **refuted** — 仮説 (「FK guard repair が配線済み」)は不成立。`within-limits?` は
   arm.cljc L15 定義・arm_test.cljc L29-30 単体テスト済みのまま、FK 経路 (forward-kinematics L22-41 /
   end-effector L43-46)内部からは **0 回** も呼ばれない。越境 angle は silent に受理され世界変換 (pose)
   を返す (docstring L27-28 が自白、falsify-034/036/039/040 と同根の既知点)。governor 層 (governor.cljc)
   も arm limit/torque に無接続のまま —「no LLM-to-actuator shortcut」は FK 層で未成立という
   falsify-039/040 の結論は**不変** (新規破れ検出なし、回帰なし、コード変更なし)。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  git rev-parse HEAD                          # → d0d3cb45 (不変, 前回から)
  grep -rn 'within-limits?' src/ test/        # → arm.cljc L15(定義)/L28(doc)/arm_test.cljc L29,L30(テストのみ、FK 内呼出 0)
  read src/kotoba/giemon/arm.cljc L22-41      # → forward-kinematics 本体 (L38 zero-fill, limit 検査なし) / L43-46 end-effector
  uptime                                      # → Load gate (15min ≥ 2×ncpu=20) 超過なら重い test 実行は省略
  ```
- 検証内訳 (本 walk の 1 仮説・1 実測判定): 1 仮説 (H42) / 測定 2 (grep within-limits? 呼出回数 + FK 本体 read、
   いずれも falsify-039/040 と同値を確認) / 判定 refuted (FK guard repair 未配線)。
- コアへの 1 行: FK (`forward-kinematics` L22-41) は依然 `within-limits?` を 0 回、
   越境 angles を silent 受理で pose 返却 (falsify-039/040 と同根、HEAD d0d3cb45 不変)、governor 無接続のまま —
   repair は FK 経路 (または gate<->arm 照合)への limit 検査配線が必須、本 bot は実装・変更なし。