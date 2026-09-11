# falsify-062 (H63) refuted — FK guard repair 依然未配線

## 仮説 (H63)
FK guard repair が実装された — `arm.cljc` `forward-kinematics` 本体 (loop L31-41) が
`within-limits?` を呼び、越境 angle を silent 受理でなく拒否/クランプ/nil で検証層に
観測可能にする (maturity NEXT の repair 指示)。あわせて arm_test 20-22 の
silent zero-fill 緑 assertion が期待値変更される。

## 実測 (純静的読取、負荷 ~15.5× ncpu=10 で gate 大幅超過のため重い test は省略、数字捏造ゼロ)
- `within-limits?` 呼出箇所 (src 全体): **2 箇所のみ** — arm.cljc L15 (defn 定義) と
  L28 (docstring 言及)。FK 経路 (`forward-kinematics` L22-41 本体 L31-41 /
  `end-effector` L43-46) 内部からの呼出 **0 回**。
- arm.cljc L38 silent zero-fill `angle (or (first angles) 0.0)` **不変** — 越境/欠損
  angles を 0.0 で silent 受理し pose を返す。docstring L27-29 が自白
  ("not the safety gate ... still produces a pose")。
- arm_test L20-22 (silent zero-fill 緑固定 assertion) は期待値変更なし (本 walk では
  test 実行していないが、HEAD 不変・tracked diff 空で編集痕なし)。
- governor.cljc の arm / limit / torque / joint 参照行: **0 行** (gate 迂回 shortcut
  は falsify-057 で src 内不存在確定、FK 層 limit 検査欠落のみ残存)。
- HEAD giemon d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe 不変 (d0d3cb4 系列)、
  tracked diff 空 (`?? sim-loop/` 未追跡のみ)。git HEAD/status は /tmp redirect
  workaround で実測取得。

## verdict: refuted
FK 経路は越境 angles を silent 受理のまま — guard repair 未着手。
falsify-034/036/039/040/041/042/043/044/045/046/047/048/049/050/051/052/053/054/055/056/058/059/060
と同根 (falsify-057 は FK shortcut 仮説で別系) ・**24 連続 refuted**。

## 再現手順
```
grep -rn "within-limits?" src/            # L15 def / L28 doc の計 2 箇所のみ
sed -n '22,46p' src/kotoba/giemon/arm.cljk # L38 silent zero-fill 不変, FK 内呼出 0
grep -nE "arm|limit|torque|joint" src/kotoba/giemon/governor.cljk  # 0 行
git rev-parse HEAD                         # d0d3cb45fcc8... (不変)
git status --porcelain                     # ?? sim-loop/ のみ
```
END