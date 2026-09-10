# falsify-038 — H39 (damping/摩擦 はコア検証層で消費され DR worst-case を検証できるか)

- 連続番号: 038 (falsify-037 の後続)
- 日次: 260908
- 仮説 (H39, 反証対象「DR (ドメインランダム化) パラメータの worst-case 振り」):
  コア計算 (FK / torque-headroom) が `:joint/damping` (粘性摩擦) を **消費する** —
  すなわち damping 値の違いが FK pose か torque 判定の少なくとも一方を変える、だから DR の
  damping ランダム化が検証層に観測可能である。反証は「damping が両 fixture に存在するが
  計算層で一切読まれない」のとき。
- 実測 (決定的、静的読取 + grep 実測数、実行 backend 不要のため REPL は走らせず — 捏造なし):
  - **EDN fixture**: `:joint/damping` は `fixtures/giemon_arm6/giemon_arm6.edn` に **6 件**。
    falsify-035 の測定値 0.06/0.08/0.06/0.04/0.03/0.02 (j1..j6) と整合
    (6 joint 全てに粘性係数あり)。
  - **URDF fixture**: `damping` 属性は `giemon_arm6.urdf` に **6 件**
    (0.02/0.03/0.04/0.06×2/0.08) — EDN と 1 対 1 で同値、パリティは無破れ
    (damping 面でも URDF↔EDN は一致)。
  - **コア消費 (src + test)**: `damping\|friction` の言及は `src/` `test/` 通算 **1 件のみ**、
    しかもそれは `src/kotoba/giemon/chassis.cljc` L14 のドキュメントコメント文中
    「ground friction」であり、計算コードの読取ではない。 `:joint/damping` を
    読む式は src/test に **0 件** (grep `:joint\damping` は src/test でゼロ)。
    FK (`forward-kinematics`) は origin/axis/angle のみ、torque-headroom は
    `:joint/limit :effort` / `:joint/actuator :cont-nm` のみ — damping はどの検証面も触れない。
  - 測定時 HOST LOAD: 開始前 30.07 / 30.58 / 33.00 (ncpu=10 の約3倍)。
    静的読取 (grep 実測 7 本) のみのため実行 backend 不要で完遂。
- verdict: **refuted** — 仮説 (「damping/摩擦 はコア検証層で消費され DR worst-case を
  検証できる」) は不成立。damping は EDN/URDF 両 fixture に 6 件ずつ同値で存在
  (パリティ面の破れは無し) が、コア実装 (src) は `:joint/damping` を
  一切読まない (言及は chassis コメントの "ground friction" 1 件のみ)。
  従って DR の damping ランダム化は FK にも torque-headroom にも観測不能 — 摩擦・粘性の
  worst-case 振りを検証できる動力学面は現コアに存在しない (純キネマティクス契約)。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  grep -o ':joint/damping' fixtures/giemon_arm6/giemon_arm6.edn | wc -l   # → 6
  grep -o 'damping'     fixtures/giemon_arm6/giemon_arm6.urdf | wc -l   # → 6 (0.06..0.02)
  grep -rn ':joint\damping' src/ test/ | wc -l                 # → 0 (消費なし)
  grep -rni 'damping\|friction' src/ test/                       # → 1 (chassis.cljc L14 コメントのみ)
  ```
- 検証内訳 (本 walk の 1 仮説・1 実測判定): 1 仮説 (H39) / 測定 1 (静的読取
  EDN/URDF 各 6 件 + src/test 消費 grep 3 本) / 判定 refuted (消費面なし)。
- コアへの 1 行: damping/摩擦 は両 fixture (EDN 6 / URDF 0.02-0.08 6) で
  parity 無破れに存在するが、コア計算 (FK/torque-headroom) は 1 つも消費しない
  (言及は chassis.cljc L14 コメントの "ground friction" のみ) — DR の damping
  worst-case を検証したければ動力学 (粘性項) の実装が前提、本 bot は実装・変更なし。