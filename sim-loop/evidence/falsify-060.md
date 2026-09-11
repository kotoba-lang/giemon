# falsify-060 — H61 (FK guard repair が配線されたか: `within-limits?` が FK 経路内から呼出され越境 angle が観測可能になったか)

- 連続番号: 060 (falsify-059 の後続、NEXT 再発行系)

- 日次: 260909
- 採択元: status/maturity.md NEXT (FK guard repair 再発行継続) — 期限切れ検査:
  repair が為された (単体定義のまま FK 本体へ配線された) という仮説を測定のみで反証/生存決着する。
- 仮説 (H61, 反証対象「FK guard repair の達成」): arm.cljc `forward-kinematics`
  (L22-41) 本体 (loop 本体 L31-41) / `end-effector` (L43-46) 内に `within-limits?` 呼出が
  配線され、越境 angle は silent 受理でなく 拒否・クランプ・nil のいずれかで検証層に観測可能になった。
- 実測 (決定的、純静的読取。HOST LOAD 15min ≈67.99 (≈6.8× ncpu=10) は Load gate
  (15min ≥  ̃2×ncpu=20) を大幅超過 + terminal backend が素の stdout を swallow で重い test は省略し
  test 計数 unmeasured、数字捏造ゼロ。git HEAD/status・read は /tmp redirect workaround で実測取得):
  - **`within-limits?` src ヒット計 3 箇所のみ**: arm.cljc L15-20 def (L27-29
    docstring "not the safety gate" 自白)・arm_test.cljc L28-30 単体専用テスト — **FK 経路
    (forward-kinematics L22-41 / end-effector L43-46) 内部から呼出 0 回** (read_file 実測)。
  - **L38 silent zero-fill 不変**: `angle (or (first angles)  0.0)` — 越境/欠如
    angle は 0.0 に静かに埋められ pose が返る (拒否・クランプ・nil のいずれも観測不可能)。
  - **governor.cljc refs 0** — governor 層は arm limit/torque に依然無接続
    (gate 迂回 shortcut は falsify-057 で src 内不存在 確定済み、FK 層の limit 検査欠落のみ残存)。
  - **HEAD giemon d0d3cb45fcc8… (d0d3cb4 系列) 不変**、 `git status --porcelain`: `?? sim-loop/` のみ
    → **tracked diff 空** (コード変更なし。両 HEAD (giemon d0d3cb4 系列 / robotics 9459ca0) 不変で measured。
- verdict: **refuted** — FK guard repair は依然未配線。`within-limits?` は定義・単体
  テスト・docstring のみで、FK 経路 (forward-kinematics / end-effector) 内部から呼出 0 回、
  越境 angles は silent 受理で pose 返却。falsify-034/036/039/040/041/042/043/044/045/046/
  047/048/049/050/051/052/053/054/055/056/058/059 と同根 (falsify-057 は FK shortcut 仮説で別系)、
  HEAD 不変・tracked diff 空で repair は未着手 — NEXT ( FK guard repair) 再発行継続。;;;
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  grep -n 'within-limits?' src/kotoba/giemon/arm.cljk test/kotoba/giemon/arm_test.cljk src/kotoba/giemon/governor.cljk
  # → arm.cljc L15 def / L28 doc の計 2 箇所のみ (governor 0・FK 本体 0 回呼出)、arm_test L29-30 単体
  sed -n '31,41p' src/kotoba/giemon/arm.cljk   # forward-kinematics loop 本体:L38 silent zero-fill
  git rev-parse HEAD; git status --porcelain    # → d0d3cb45fcc... 不変、`?? sim-loop/` のみ (tracked diff 空)
  ```
- 検証内訳 (本 walk の 1 仮説・1 実測判定): 1 仮説 (H61) / 測定 1 (`within-limits?`
  src 全域 grep + FK 経路 read + git HEAD/status の決定的比較) / 判定 refuted (repair 未配線)。
- コアへの 1 行: H61 も refuted — `within-limits?` は arm.cljc L15-20 定義・
  arm_test.cljc L28-30 単体・docstring のみで、FK 経路 (forward-kinematics L22-41 /
  end-effector L43-46) 内呼出 0 回、L38 silent zero-fill 不変、HEAD d0d3cb4 系列不変・
  tracked diff 空 — FK guard repair は依然未配線、越境 angle を silent 受理で pose 返却
  (本 bot は実装・コード変更なし)。