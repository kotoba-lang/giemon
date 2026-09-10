# falsify-047 — H48 (FK guard repair が着手され、FK 経路は越境 angles を検査するか)

- 連続番号: 047 (falsify-046 の後続)
- 日次: 260908
- 仮説 (H48, NEXT 継続発行 — falsify-034/036/039/040/041/042/043/044/045/046 の 11 連続 refuted を受けた再検証):
  `kotoba.giemon.arm/forward-kinematics` (L22-41) 本体に `within-limits?` (L15-20) 呼出が
  配線され、越境 angle は silent 受理でなく拒否・クランプ・nil のいずれかで検証層に観測可能に
  なった。すなわち FK guard repair が着手された。
  反証は「`within-limits?` は定義済だが FK 経路から 0 回も呼ばれず、L38 silent zero-fill
  (`angle (or (first angles) 0.0)`) と arm_test L20-22 の緑零埋め assertion が無変更、
  governor 層が arm limit/torque に無接続のまま」のとき。
- 実測 (決定的、純静的読取 — 実行 backend 応答不能 + HOST LOAD 超過のため REPL・test 計数は
  unmeasured、数字捏造ゼロ):
  - **`within-limits?` 定義/呼出分布:** arm.cljc L15-20 定義・docstring L27-29 言及、
    arm_test.cljc L28-30 単体テストのみ。src+test 全 grep で FK 経路
    (`forward-kinematics` 本体 L31-40 loop) からの呼出は **0 回** — NG.Correct。
  - **FK 本体 (arm.cljc L22-41):** loop 内に limit 検査・クランプ・拒否・nil は皆無。
    L38 `angle (or (first angles) 0.0)` silent zero-fill は `[first angles]` → `0.0` の
    形で **不変**。docstring L27-29 が「an angle outside a joint's declared limit still
    produces a pose. Check `within-limits?` first if that matters」と自白継続。
  - **end-effector (L43-46):** `(last (forward-kinematics arm angles))` のみ、guard なし不変。
  - **arm_test.cljc L20-22:** "missing angles default to 0.0" が
    `(= (fk two-joint-arm [0.0 0.0]) (fk two-joint-arm []))` で緑固定 — silent zero-fill
    を期待値として固定する assertion **無変更**。
  - **governor 接続:** governor.cljc は src 中の arm/limit/torque/within-limits 参照 **0**
    (grep 実測 total_count 0) — arm limit/torque に無接続のまま。
  - HEAD: terminal backend 応答不能のため git 直接確認不能。ただし src/ test/ の全該当箇所が
    falsify-046 記載の行番号・内容と完全一致し、tracked diff 無しの前提に整合 (sim-loop/ 未追跡のみ)。
  - 測定時 HOST LOAD: pre-run 15min 46.71 (ucpu=10 の約 4.7×)。Load gate (15min ≥ 2×ncpu=20)
    を大幅超過 + terminal backend 応答不能 — 重い test 実行は省略し unmeasured (honest 据え置き)。
- verdict: **refuted** — FK guard repair は依然未着手。`within-limits?` は定義・単体テスト済みだが
  FK 経路 (forward-kinematics L22-41 / end-effector L43-46) 内部から呼出 **0 回**、L38 silent
  zero-fill (`angle (or (first angles) 0.0)`) 不変、arm_test L20-22 が零埋め緑固定、governor.cljc
  は arm limit/torque に無接続のまま — 越境 angles を silent 受理で pose 返却 (docstring L27-29
  自白)。falsify-034/036/039/040/041/042/043/044/045/046 と同根 (12 連続同一結論、HEAD 系列不変)。
- 再現手順 (全て静的読取、実行不要):
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  grep -rn 'within-limits?' src/ test/        # → arm.cljc L15(定義)/L27-29(doc)/arm_test.cljc L28-30(テストのみ、FK 内呼出 0
  read src/kotoba/giemon/arm.cljc L22-41      # forward-kinematics loop、L38 `angle (or (first angles) 0.0)`、limit 検査なし
  read test/kotoba/giemon/arm_test.cljc L20-22# zero-fill 緑 assertion 無変更: (= (fk [0.0 0.0]) (fk []))
  grep -n 'arm\|limit\|torque\|within-limits' src/kotoba/giemon/governor.cljc  # → 0 (無接続)
  ```
- 検証内訳 (1 仮説・1 実測判定): 1 仮説 (H48) / 測定 1 (純静的読取 — within-limits? 定義 vs FK 呼出 0 回
  + L38 zero-fill 不変 + arm_test L20-22 緑固定 + governor 接続 0 の 4 観測点) / 判定 refuted (未着手)。
- コアへの 1 行: FK guard repair は 12 連続で未着手のまま (`within-limits?` は定義済だが FK 内呼出 0 回、
  L38 silent zero-fill と arm_test L20-22 緑零埋め assertion は無変更、governor は arm に無接続 — 越境
  angles を silent 受理継続)、本 bot は実装・変更なし。
