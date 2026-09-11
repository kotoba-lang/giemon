# falsify-057 (H58) — giemon src に governor gate を迂回する LLM-to-actuator shortcut 経路が存在するか

- 連続番号: 057 (falsify-056 の後続)
- 日次: 260909
- 仮説 (H58, falsify 領域 4 — governor gate 迂回 / no-LLM-to-actuator-shortcut 検査):
  `src/kotoba/giemon/` 配下 (8 ファイル) に、`kotoba.robotics/gate` (`rob/action` 経由契約)
  を迂回して hardware / actuator を直接駆動する dispatch 経路 ( process/spawn/socket/http/
   Thread/future/sh/外部実行) が存在する。すなわち LLM 生成アクションが gate を経ずに
  実機に届く shortcut が src 内に配線されている。
  反証は「README/docstring の「never drives hardware」「No network, no I/O」宣言が
  src 本体の実装と一致し、action 構築が全て `rob/action` 経由で robotics の gate 契約に
  流れ込む」のとき。

- 実測 (決定的、純静的読取 — HOST LOAD pre-run 1/5/15min = 32.43/28.46/33.71
  (15min ≈33.7 = ≈3.4× ncpu=10) は Load gate (15min ≥ 2×ncpu=20) 超過帯、
  terminal backend が素の stdout を吞むため git 出力は /tmp redirect workaround で実測、
  重い test 実行は省略し test 計数は unmeasured (honest 据え置き)、数字捏造ゼロ):
  - **src 全 8 ファイル (search_files target=files 実測):** `kotoba.giemon` / `kotoba.giemon.arm` /
    `kotoba.giemon.kinematics` / `kotoba.giemon.chassis` / `kotoba.giemon.governor` /
    `kotoba.giemon.export` / `kotoba.giemon.ui` / `kotoba.giemon.viewer`。
  - **外部実行/プロセス/ネット呼出 grep (src/ 全走査、search_files 実測):** `process|spawn|
    socket|http|Thread|future|sh/|Runtime|System/|dispatch|shutdown|bang` の
    実 match は **0** 実行呼出 (hit 4 行は全て docstring/UI ラベルの「never dispatches」
    「governor-gated・never dispatches」「before any dispatch」「sign-off before any
    dispatch」の物語文のみ、呼出・関数参照ゼロ)。
  - **駆動系 grep (src/ 全走査):** `drive|actuat|execute|transmit|publish|send-|emit!|
    move!` の実 match は actuator **BOM データ記述専用** (`:joint/actuator`、
    `arm/chain-actuators`、`torque-headroom`、track-drive kinematics の
    「drive」命名) + governor の「never drives hardware」宣言 — 実行 dispatch / 実機
    駆動呼出は **0**。
  - **action 構築経路 (governor.cljc L16-68 全読):** Giemon 側 action 構築は全て
    `kaigo-action` / `ops-action` (L24-27, L57-60) → `rob/action`
    ( `kotoba.robotics` 契約、L7 :require) 経由のみ。`:emit` エスカレーション
    (`fall-detected-alert` L34-35 / `chemical-dispense-alert` L67-68) も
    `rob/action :safety-critical` で gate の human sign-off 経路に流れる。
    `rob/action` を迂回する dispatch / gate 迂回呼出は **0**。
  - **トップ契約 (giemon.cljc L1-13 全読):** docstring「This library never drives
    hardware... Physical execution and safety gating are kotoba-lang/robotics' concern
    ... No network, no I/O」— 実装と一致。
  - **HEAD / tracked diff (git 実測、/tmp redirect で取得):** giemon HEAD =
    d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe (d0d3cb4)、robotics HEAD =
    9459ca0d5b3126472e23de6a77f725a9a3480770 (9459ca0)、`git status --short` は
    **`?? sim-loop/` のみ** (tracked diff 空、コード変更なし)。

- verdict: **refuted** — giemon src 内に governor gate を迂回する LLM-to-actuator
  shortcut 経路は存在しない。全ての Giemon 側 action 構築 (`kaigo-action` / `ops-action` /
  `:emit` エスカレーション) は `rob/action` 経由のみで robotics の gate 契約に流れ、
  src には process / spawn / socket / http / Thread 等の外部実行・実機駆動呼出が
  **0** (hit は全て「never dispatches」系の物語文のみ)。docstring「never drives
  hardware ... No network, no I/O」は実装と一致。強いて言えば gate の実体 ( `rob/gate`
  本体) は kotoba-lang/robotics 側 repo にあり Giemon src の静的走査範囲外 —
  本測定の射程は「Giemon src 内に gate 迂回 shortcut なし」に限定。

- 再現手順 (全て静的読取・git redirect、実行不要):
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  git rev-parse HEAD > /tmp/h && cat /tmp/h                  # d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe
  git -C .../kotoba-lang/robotics rev-parse HEAD > /tmp/h2 && cat /tmp/h2   # 9459ca0
  git status --short > /tmp/s && cat /tmp/s                  # ?? sim-loop/ のみ (tracked diff 空)
  grep -rn 'process\|spawn\|socket\|http\|Thread\|future\|sh/\|Runtime\|System/\|dispatch\|bang' src/   # → 実行呼出 0 (hit は doc/ラベルの物語文のみ)
  grep -rn 'drive\|actuat\|execute\|transmit\|publish\|send-\|emit!\|move!' src/    # → BOM 記述専用、実行駆動呼出 0
  read src/kotoba/giemon/governor.cljk L16-68          # action 構築は全て rob/action 経由、gate 迂回なし
  read src/kotoba/giemon.cljk L1-13                    # docstring「never drives hardware ... No network, no I/O」
  ```

- 検証内訳 (1 仮説・1 実測判定): 1 仮説 (H58「governor gate 迂回 shortcut 存在」) / 測定 1
  (純静的読取 — src 全 8 ファイル の外部実行/駆動系 grep 分布 =0 + action 構築の
   `rob/action` 経由確認 + `:emit` エスカレーション も gate 契約 + docstring 一致 +
   両 HEAD/tracked diff の 5 観測点) / 判定 refuted ( gate 迂回 shortcut なし)。

- コアへの 1 行: Giemon src は `rob/action` 経由のみで robotics の gate 契約に流れ、process/
  spawn/socket/http 等の外部実行・実機駆動呼出が **0** (hit は「never dispatches」物語文のみ)、
  docstring「No network, no I/O」と一致 — LLM-to-actuator gate 迂回 shortcut は
   src 内に存在せず (H58 refuted)。本 bot は実装・変更なし (HOST LOAD 15min ≈33.7
   は Load gate 超過帯で重い test 実行を省略し unmeasured 明記)。