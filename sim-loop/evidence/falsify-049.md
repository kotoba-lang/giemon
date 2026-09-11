# falsify-049 — H50 (FK guard repair が着手され、FK 経路は越境 angles を検査するか)

- 連続番号: 049 (falsify-048 の後続)
- 日次: 260908
- 仮説 (H50, NEXT 継続発行 — falsify-034/036/039/040/041/042/043/044/045/046/047/048 の 13 連続 refuted を受けた再検証):
  `kotoba.giemon.arm/forward-kinematics` (L22-41、loop 本体 L31-41) 本体に `within-limits?`
  (L15-20) 呼出が配線され、越境 angle は silent 受理でなく拒否・クランプ・nil のいずれかで
  検証層に観測可能になった。すなわち FK guard repair が着手された。
  反証は「`within-limits?` は定義済だが FK 経路から 0 回も呼ばれず、L38 silent zero-fill
  (`angle (or (first angles) 0.0)`) と arm_test L20-22 の緑零埋め assertion が無変更、
  governor 層が arm limit/torque に無接続のまま」のとき。
- 実測 (決定的、純静的読取 — HOST LOAD 極超過 + terminal backend が素の stdout を swallow し
  redirect 経由のみ応答のため REPL・test 計数は unmeasured、数字捏造ゼロ):
  - **`within-limits?` 定義/呼出分布 (grep src/ test/ 実測):** arm.cljc L15-20 定義・arm.cljc L28
    docstring 言及・arm_test.cljc L28-30 単体テストのみの計 3 箇所。FK 経路
    (`forward-kinematics` 本体 L22-41 loop / end-effector L43-46) からの呼出は **0 回** —
    定義・doc・単体テスト以外に出現なし。
  - **FK 本体 (arm.cljc L31-41 loop):** ループ内に limit 検査・クランプ・拒否・nil は皆無。
    L38 `angle (or (first angles) 0.0)` silent zero-fill は **不変**。docstring L27-29 が
    「an angle outside a joint's declared limit still produces a pose. Check
    `within-limits?` first if that matters」と自白継続。
  - **end-effector (L43-46):** `(last (forward-kinematics arm angles))` のみ、guard なし不変。
  - **arm_test.cljc L20-22:** "missing angles default to 0.0" が
    `(= (fk two-joint-arm [0.0 0.0]) (fk two-joint-arm []))` で緑固定 — silent zero-fill を
    期待値として固定する assertion **無変更**。
  - **governor 接続:** governor.cljc を grep `within-limits|:joint/limit|forward-kinematics|
    end-effector` 実測は **0 行 (0 bytes)** — arm limit/torque/within-limits に無接続のまま。
  - **HEAD / tracked diff (git direct 実測、redirect workaround で取得):** giemon HEAD =
    **d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe (d0d3cb4)**、`git status --short` は
    **`?? sim-loop/` のみ** (tracked diff 空、コード変更なし)。
  - 測定時 HOST LOAD: 本 walk 冒頭 78.99/63.37/57.46 → 終盤 86.03/70.57/61.14 (≈6–8.6× ncpu=10)。
    Load gate (15min ≥ 2×ncpu=20) を大幅超過 + terminal backend 応答不能 (素のコマンド出力が
    逐次 swallow、redirect 経由で取得) — 重い test 実行は省略し unmeasured (honest 据え置き)。
- verdict: **refuted** — FK guard repair は依然未着手 (14 連続)。`within-limits?` は定義・doc・
  単体テストのみで FK 経路 (forward-kinematics L22-41 / end-effector L43-46) 内部から呼出
  **0 回**、L38 silent zero-fill (`angle (or (first angles) 0.0)`) 不変、arm_test L20-22 が零埋め
  緑固定、governor.cljc は arm limit/torque に無接続のまま — 越境 angles を silent 受理で pose
  返却 (docstring L27-29 自白)。falsify-034/036/039/040/041/042/043/044/045/046/047/048 と
  同根 (HEAD d0d3cb4 系列・tracked diff 空で不変)。
- 再現手順 (全て静的読取、実行不要):
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  git rev-parse HEAD                                      # d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe (不変)
  git status --short                                      # ?? sim-loop/ のみ (tracked diff 空)
  grep -rn 'within-limits' src/ test/                     # arm.cljc L15-20(def)/L28(doc)/arm_test L28-30(単体) の計 3 箇所のみ、FK 内呼出 0
  read src/kotoba/giemon/arm.cljk L31-41                  # forward-kinematics loop、L38 `angle (or (first angles) 0.0)`、limit 検査なし
  read test/kotoba/giemon/arm_test.cljk L20-22            # zero-fill 緑 assertion 無変更: (= (fk [0.0 0.0]) (fk []))
  grep -n 'within-limits\|:joint/limit\|forward-kinematics\|end-effector' src/kotoba/giemon/governor.cljk  # → 0 行 (無接続)
  ```
- 検証内訳 (1 仮説・1 実測判定): 1 仮説 (H50) / 測定 1 (純静的読取 — within-limits? grep 分布
  (FK 内呼出 0) + L38 zero-fill 不変 + arm_test L20-22 緑固定 + governor 接続 0 + HEAD/tracked
  diff の 5 観測点) / 判定 refuted (未着手)。
- コアへの 1 行: FK guard repair は 14 連続で未着手のまま (`within-limits?` は定義・単体テストのみ
  で FK 内呼出 0 回、L38 silent zero-fill と arm_test L20-22 緑零埋め assertion は無変更、
  governor は arm に無接続、HEAD d0d3cb4 不変 — 越境 angles を silent 受理継続)、本 bot は
  実装・変更なし (HOST LOAD 86/70/61 ≈6–8.6× で重い test 実行を省略し unmeasured 明記)。