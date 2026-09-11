# falsify-055 (H56) — FK guard repair 依然未配線 (pure static read)

仮説 (H56, NEXT 再発行継続 — falsify-034/036/039/040/041/042/043/044/045/046/047/048/049/050/051/052/053/054 の 19 連続 refuted を受けた再検証):
  kotoba.giemon.arm/forward-kinematics (arm.cljc L22-41) 本体に `within-limits?` (L15-20)
  呼出が配線され、越境 angle を silent 受理でなく拒否・クランプ・nil のいずれかで検証層に
  観測可能になった (FK guard repair 着手)。

実測 (決定的、純静的読取 — HOST LOAD 22:18 実測 15min ≈76.39 は Load gate (15min ≥ 2×ncpu=20)
  大幅超過帯。terminal backend が素の stdout を吞むため git 出力は /tmp redirect workaround で
  実測取得。重い test 実行は省略し test 計数は unmeasured (honest 据え置き)、数字捏造ゼロ):
  - `within-limits?` 定義/呼出分布 (search_files 実測): arm.cljc L15 定義・arm.cljc L28
    docstring 言及・arm_test.cljc L28-30 単体テストのみの計 3 箇所。FK 経路
    (forward-kinematics 本体 L22-41 loop / end-effector L43-46) からの呼出は **0 回**。
  - FK 本体 (arm.cljc L31-41 loop、read 実測): ループ内に limit 検査・クランプ・拒否・nil 皆無。
    L38 `angle (or (first angles) 0.0)` silent zero-fill は **不変**。docstring L27-29「an angle
    outside a joint's declared limit still produces a pose. Check `within-limits?` first if
    that matters」自白継続。
  - end-effector (L43-46): `(last (forward-kinematics arm angles))` のみ guard なし不変。
  - governor 接続: governor.cljc を `within-limits|within_limits|joint.*limit|torque` で
    grep 実測 **0 行** — arm limit/torque に無接続のまま。
  - HEAD / tracked diff (git 実測、/tmp redirect で取得): giemon HEAD =
    d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe (d0d3cb4)、`git status --short` は **`?? sim-loop/`
    のみ** (tracked diff 空、コード変更なし)。
  - 測定時 HOST LOAD: 本 walk 冒頭 22:18 up 3 days 15:58、6 users、
    1min/5min/15min = 76.39/59.41/58.48 (15min ≈7.6× ncpu=10)。Load gate (15min ≥ 2×ncpu=20)
    を大幅超過の非応答域で重い test 実行は省略し unmeasured (honest 据え置き)。search_files/
    read_file / git redirect のみで実測。

verdict: **refuted** — FK guard repair は依然未着手 (20 連続)。`within-limits?` は定義 L15-20・
  docstring L28・単体テスト arm_test L28-30 のみで FK 経路 (forward-kinematics L22-41 /
  end-effector L43-46) 内部から呼出 **0 回**、L38 silent zero-fill (`angle (or (first angles) 0.0)`)
  不変、arm_test L20-22 が零埋め緑固定、governor.cljc (全 68 行) に arm limit/torque 参照 0 行 —
  越境 angles を silent 受理で pose 返却 (docstring L27-29 自白)。falsify-034/036/039/040/041/042/043/
  044/045/046/047/048/049/050/051/052/053/054 と同根 (HEAD d0d3cb4 系列・tracked diff 空で不変)。

再現手順 (全て静的読取・git redirect、実行不要):
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  git rev-parse HEAD > /tmp/h && cat /tmp/h        # d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe (不変)
  git status --short > /tmp/s && cat /tmp/s        # ?? sim-loop/ のみ (tracked diff 空)
  grep -rn 'within-limits' src/ test/              # arm.cljc L15(def)/L28(doc)/arm_test L28-30(単体) 計 3 箇所のみ、FK 内呼出 0
  read src/kotoba/giemon/arm.cljk L22-41           # forward-kinematics loop、L38 `angle (or (first angles) 0.0)`、limit 検査なし
  read src/kotoba/giemon/arm.cljk L43-46           # end-effector は (last (forward-kinematics arm angles)) のみ guard なし
  grep -c 'within-limits\|within_limits\|joint.*limit\|torque' src/kotoba/giemon/governor.cljk  # → 0
  ```

検証内訳 (1 仮説・1 実測判定): 1 仮説 (H56) / 測定 1 (純静的読取 — `within-limits?` grep 分布
  (FK 内呼出 0) + L38 zero-fill 不変 + end-effector guard なし + governor 接続 0 + HEAD/tracked
  diff の 5 観測点) / 判定 refuted (未着手、20 連続)。

コアへの 1 行: FK guard repair は 20 連続で未着手のまま (`within-limits?` (L15-20) は定義・docstring・
  単体テストのみで FK 内 (L22-41 loop / L43-46 end-effector) 呼出 0 回、L38 silent zero-fill 無変更、
  governor.cljc は arm limit/torque に無接続、HEAD d0d3cb4 不変・tracked diff 空 — 越境 angles を
  silent 受理継続)。本 bot は実装・変更なし (HOST LOAD 15min ≈76.39 は Load gate 大幅超過帯で重い
  test 実行を省略し unmeasured 明記)。