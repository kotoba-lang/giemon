# falsify-039 — H40 (FK 層は越境 angles を silent 受理し、「governor gate を迂回できるアクション列」が FK 経路に存在するか)

- 連続番号: 039 (falsify-038 の後続)
- 日次: 260908
- 仮説 (H40, 反証対象「governor gate を迂回できるアクション列がないか (no LLM-to-actuator shortcut の検査)」):
   FK 経路 (`kotoba.giemon.arm/forward-kinematics` / `end-effector`) は、各 joint 角度が
   宣言 `:joint/limit {:lower :upper}` 内かを検査する — すなわち `within-limits?` が FK 経路内から
   呼ばれ、越境 angles は拒否・クランプ・nil のいずれかで検証層に観測可能である。
   反証は「`within-limits?` は定義されているが FK 経路から 0 回も呼ばれず、
   越境 angles が silent に受理され世界変換 (pose) を返す」のとき。
- 実測 (決定的、静的読取 + grep 実測数、実行 backend 不要のため REPL は走らせず — 捏造なし):
  - **`within-limits?` 定義:** `src/kotoba/giemon/arm.cljk` L15-20 —
    `(and (some? lower) (some? upper) (<= lower angle upper))` と宣言 limit を検査する関数は
    存在する (`fixtures/giemon_arm6/giemon_arm6.edn` に j1..j6 全 6 joint の `:joint/limit {:lower :upper}` が
    j1 [-3.0,3.0] / j2 [-2.2,2.2] / j3 [-2.5,2.5] / j5 [-2.0,2.0] / j6 [-3.0,3.0] 等で実在)。
  - **FK からの呼出回数 (src+test 通算):** `grep -rn 'within-limits?' src/ test/` は **4 行のみ**、
    うち FK 経路内 (`forward-kinematics` 本体) からの呼出は **0**。
    (内訳: arm.cljc L15 定義 / L28 docstring 言及 / arm_test.cljc L29, L30 の単体テスト 2 行)。
    `forward-kinematics` 本体 (L22-41) に `within-limits?` 呼出は皆無。
  - **FK の角度処理:** arm.cljc L38 `angle (or (first angles) 0.0)` — 欠落 angle は silent zero-fill
    (falsify-034/036 と同根の既知点)。越境 angle に対し検査・クランプ・拒否・nil は一切なし —
    docstring 自体 (L27-28) が「an angle outside a joint's declared limit still produces
    a pose. Check `within-limits?` first if that matters」と明言 (自白)。
  - **門 (governor) と FK/torque の接続:** `src/kotoba/giemon/governor.cljk` は mission/action を
    安全クラス (`kaigo-roles` / `ops-roles` の `:default-safety`) に分類する層のみ (:require
    [kotoba.robotics :as rob]) で、`:joint/limit`・`torque-headroom`・FK への参照は **0**
    (grep `gate\|reject\|refuse\|clamp\|violat` src/ は arm.cljc L27 docstring と governor.cljc
    L6/L32/L65 の kotoba.robotics/gate 言及のみ — arm limit/torque への接続なし、
    falsify-001 の「gate<->torque 照合未接続」と整合)。`viewer.cljc` L23 は
    `arm/forward-kinematics` を直接呼び、角度検査は呼び出し側次第で FK 自体は無検証。
  - 測定時 HOST LOAD: pre-run (2:25)10.64 / 10.99 / 11.86 (ncpu=10 の約1.1×)。
    静的読取 (grep 実測 3 本)のみのため実行 backend 不要で完遂。
- verdict: **refuted** — 仮説 (「FK 経路は越境 angles を検査する (FK guard が配線済み)」)は
  不成立。`within-limits?` は定義され単体テスト済み (arm_test.cljc L29-30) だが、FK 経路
  (`forward-kinematics` L22-41 / `end-effector` L43-46)内部からは **0 回** も呼ばれない。
  越境 angle は silent に受理され world 変換 (pose)を返す (docstring L27-28 が自白)。
  governor 層 (governor.cljc) は安全クラス分類専用で arm の limit/torque に無接続 —
  「no LLM-to-actuator shortcut」は FK 層では**未成立** (同一の越境 angles がどんなアクション列
  由来でも silent 受理される経路が存在、falsify-001 の gate<->torque 照合未接続と整合)。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  grep -rn 'within-limits?' src/ test/        # → arm.cljc L15(定義)/L28(doc)/arm_test.cljc L29,L30(テストのみ、FK 内呼出 0
  grep -n 'clamp\|gate\|reject\|refuse\|violat' src/   # → arm.cljc L27(doc)/governor.cljc L6,L32,L65(kotoba.robotics/gate 言及のみ — arm 接続なし)
  read src/kotoba/giemon/arm.cljk L22-41              # forward-kinematics 本体、L38 zero-fill、limit 検査なし
  ```
- 検証内訳 (本 walk の 1 仮説・1 実測判定): 1 仮説 (H40) / 測定 1 (静的読取
  within-limits? 定義 vs FK 呼出 0 回 + governor 接続 grep 2 本) / 判定 refuted (FK guard 未配線)。
- コアへの 1 行: FK (`forward-kinematics`/`end-effector`) は越境 angles を silent 受理
  (`within-limits?` は定義済・単体テスト済みだが FK 内部から呼出 0 回、docstring L27 が自白)、
  governor 層は arm limit/torque に無接続 —「no LLM-to-actuator shortcut」を成立させたければ
   FK 経路 (または gate<->arm 照合)に limit 検査を配線するのが必須、本 bot は実装・変更なし。