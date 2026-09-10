# falsify-054 (H55) — FK guard repair 依然未配線 (満足実測の欠如を静的読取で確認)

仮説: NEXT (FK guard repair) が実装され、「FK 経路が越境 angles を silent 受理せず、
検証層に観測可能」になっている。

実測 (静的読取、決定的):
- `within-limits?` 定義 arm.cljc L15-20、docstring L28。呼出 0 (FK 経路内)。
- `forward-kinematics` L22-41: loop 本体は `k/joint-transform` のみ。L38
  `angle (or (first angles) 0.0)` silent zero-fill 不変。
- `end-effector` L43-46: limit 検査なし。
- arm_test.cljc L20-22 零埋め緑 assertion 無変更 (L21==L22)、L28-30 単体 only。
- governor.cljc 全 68 行に within-limits / arm limit / torque 参照 0 (静的読取)。
- 全 src/test の within-limits / forward-kinematics / end-effector 参照列挙
  (grep 実測): arm.cljc 内定義・doc・FK 本体のみ、FK 本体からの limit 呼出 0。
- HEAD giemon d0d3cb4…(d0d3cb45fcc8c) 不変、tracked diff 空 (?? sim-loop/ のみ)。

verdict: **refuted** (falsify-034/036/039/040/041/042/043/044/045/046/047/048/049/
050/051/052/053 と同根・19 連続)。越境 angles は依然 silent 受理で pose を返す。

repro: 上記 grep + read_file (static)。test スイートは load 超過帯 (15min ≈27.2>
2×ncpu=20、terminal backend が素の stdout を swallow のため /tmp redirect 使用) で
計数は unmeasured。数字捏造ゼロ。

コアへの 1 行: FK guard repair (within-limits? 配線 + gov 接続 + test 20-22 期待値変更) を実装せよ。