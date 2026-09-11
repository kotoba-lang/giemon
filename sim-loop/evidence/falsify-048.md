# falsify-048 — H49 (FK guard repair が着手され、FK 経路は越境 angles を検査するか)

- 連続番号: 048 (falsify-047 の後続)
- 日次: 260908
- 仮説 (H49, NEXT 継続発行 — falsify-034/036/039/040/041/042/043/044/045/046/047 の 12 連続 refuted を受けた再検証):
  `kotoba.giemon.arm/forward-kinematics` (L31-41) 本体に `within-limits?` (L15-20) 呼出が
  配線され、越境 angle は silent 受理でなく拒否・クランプ・nil のいずれかで検証層に観測可能に
  なった。すなわち FK guard repair が着手された。
  反証は「`within-limits?` は定義済だが FK 経路から 0 回も呼ばれず、L38 silent zero-fill
  (`angle (or (first angles) 0.0)`) と arm_test L20-22 の緑零埋め assertion が無変更、
  governor 層が arm limit/torque に無接続のまま」のとき。
- 実測 (決定的、純静的読取 — terminal backend 応答不能 + HOST LOAD 超過のため REPL・test 計数は
  unmeasured、数字捏造ゼロ):
  - **`within-limits?` 定義/呼出分布 (grep src/ test/ 実測 5 行):** arm.cljc L15 定義・
    arm.cljc L28 docstring 言及・arm_test.cljc L28-30 単体テストのみの計 3 箇所。
    FK 経路 (`forward-kinematics` 本体 L31-41 loop / end-effector L43-46) からの呼出は
    **0 回** — 定義・doc・単体テスト以外に出現なし。
  - **FK 本体 (arm.cljc L31-41):** loop 内に limit 検査・クランプ・拒否・nil は皆無。
    L38 `angle (or (first angles) 0.0)` silent zero-fill は **不変**。docstring L27-29 が
    「an angle outside a joint's declared limit still produces a pose. Check
    `within-limits?` first if that matters」と自白継続。
  - **end-effector (L43-46):** `(last (forward-kinematics arm angles))` のみ、guard なし不変。
  - **arm_test.cljc L20-22:** "missing angles default to 0.0" が
    `(= (fk two-joint-arm [0.0 0.0]) (fk two-joint-arm []))` で緑固定 — silent zero-fill
    を期待値として固定する assertion **無変更**。
  - **governor 接続:** governor.cljc (L1-68 全読) は :kaigo/:ops role と :emit エスカレーション
    の安全クラス分類専用。grep `within-limits|:joint/limit|torque` 実測は **0 行 (0 bytes)** —
    arm limit/torque/within-limits に無接続のまま。
  - **HEAD / tracked diff (今回は git 直接実測、redirect workaround で取得):**
    giemon HEAD = **d0d3cb4**、`git status --short` は **`?? sim-loop/` のみ** (tracked diff 空)。
  - 測定時 HOST LOAD: pre-run 1min 28.39 / 5min 37.17 / 15min 31.96 (≈3.2× ncpu=10)。
    Load gate (15min ≥ 2×ncpu=20) を超過 + terminal backend 応答不能 (素のコマンド出力が
    逐次 swallow、redirect 経由で取得) — 重い test 実行は省略し unmeasured (honest 据え置き)。
- verdict: **refuted** — FK guard repair は依然未着手 (13 連続)。`within-limits?` は定義・
  doc・単体テストのみで FK 経路 (forward-kinematics L31-41 / end-effector L43-46) 内部から
  呼出 **0 回**、L38 silent zero-fill (`angle (or (first angles) 0.0)`) 不変、arm_test L20-22
  が零埋め緑固定、governor.cljc は arm limit/torque に無接続のまま — 越境 angles を silent
  受理で pose 返却 (docstring L27-29 自白)。falsify-034/036/039/040/041/042/043/044/045/046/047
  と同根 (HEAD d0d3cb4 系列・tracked diff 空で不変)。
- 再現手順 (全て静的読取、実行不要):
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  git rev-parse --short HEAD                              # f0d3cb4 (不変)
  git status --short                                      # ?? sim-loop/ のみ (tracked diff 空)
  grep -rn 'within-limits' src/ test/                     # arm.cljc L15(def)/L28(doc)/arm_test L28-30(単体) の計 3 箇所のみ、FK 内呼出 0
  read src/kotoba/giemon/arm.cljk L31-41                  # forward-kinematics loop、L38 `angle (or (first angles) 0.0)`、limit 検査なし
  read test/kotoba/giemon/arm_test.cljk L20-22            # zero-fill 緑 assertion 無変更: (= (fk [0.0 0.0]) (fk []))
  grep -n 'within-limits\|:joint/limit\|torque' src/kotoba/giemon/governor.cljk  # → 0 行 (無接続)
  ```
- 検証内訳 (1 仮説・1 実測判定): 1 仮説 (H49) / 測定 1 (純静的読取 — within-limits? grep 分布
  (FK 内呼出 0) + L38 zero-fill 不変 + arm_test L20-22 緑固定 + governor 接続 0 + HEAD/tracked
  diff の 5 観測点) / 判定 refuted (未着手)。
- コアへの 1 行: FK guard repair は 13 連続で未着手のまま (`within-limits?` は定義・単体テストのみ
  で FK 内呼出 0 回、L38 silent zero-fill と arm_test L20-22 緑零埋め assertion は無変更、
  governor は arm に無接続、HEAD d0d3cb4 不変 — 越境 angles を silent 受理継続)、本 bot は
  実装・変更なし。