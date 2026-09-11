# falsify-015

## 仮説
H17 — gate の下流消費面 (gate 返却レコードそのものと `action-permitted?`
boolean) は、payload (torque) にも mission 境界
(:mission/boundaries, :mission/max-steps) にも無相関である。
すなわち :permit が下流に渡すレコードには tau / velocity / boundary の
いずれも現れず、permit 判定後の payload 検査はどこにも存在しない。

maturity NEXT の残り深掘り候補のうち
「governor/robotics の action-permitted? 経路の payload 伝播
(gate :permit が下流でどう消費されるかの不在測定)」を担当。

## 実測
probe: probe_gate_permit_surface.py (新規・実測 probe)。
kotoba.robotics の gate / action-permitted? を直接列挙し、
返却レコードの key 集合・文字列内容・boolean を 2 回実行で照合。

結果 (kbb -M -e、exit 0):
- A gate 返却レコード (5 payload バリアント: clean / tau 1e6 / tau -1e6 /
  str "1e6" / effort 1e6): すべて `#:gate{:decision :permit, :action "pA"}` —
  key 集合は [:gate/action :gate/decision] で全バリアント同一
  (key-sets-identical-across-payloads: true)、
  レコード文字列に "tau" は 1 件も現れない (5/5 false)
- B mission 境界無相関: tight 境界 (max-velocity 0.1, geo-fence :home,
  max-steps 3) と loose 境界 (max-velocity 1e6, geo-fence :none,
  max-steps 1e6) で同一 params (velocity 1e6) の action →
  両者とも `:permit`、decision 差分なし、
  gate 返却レコードに "boundar" / "step" の語は 1 件も現れない。
  rob/action は mission-id (文字列) のみを受け取り mission レコード自体は
  gate に渡らないため、境界は構造的に gate に届かない
- C action-permitted?: clean / tau 1e6 / velocity 1e6 / :actuate + tau 1e6
  の 4 バリアントすべて true (permitted-all-equal: true)
- D require-sign-off 経路 (:actuate :high): 3 バリアントすべて
  `#:gate{:decision :require-sign-off, :safety :high}`、
  レコードに "1e6" は現れない (3/3 false)
- E invalid 経路: nil → `:invalid/:not-an-action`、
  {} → `:deny/:safety-class-not-allowed` (payload 無関係で決定的)
- SUMMARY: PERMIT-SURFACE-CASES 11、
  PERMIT-SURFACE-DETERMINISM-FAILS 0、
  2 回実行 diff 0 行 (clojure 出力本体。diff の差分 1 行は
  初回実行に付加した rc 記録行のみ)

## verdict
**survived** — H17 は破れず。gate :permit の下流消費面は
payload にも mission 境界にも無相関・決定的。:permit レコードは
action id と decision のみを運び、tau/velocity/boundary は
permit 判定後のどこにも現れない。action-permitted? boolean も
4 payload バリアントで不変。これで「gate :permit が下流でどう
消費されるか」の不在も決定的に記録された — gate の下流に
payload を検査する消費者はそもそも存在しない。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_gate_permit_surface.py > /tmp/h17.clj
kbb -M -e "$(cat /tmp/h17.clj)" > /tmp/h17.txt 2>&1
kbb -M -e "$(cat /tmp/h17.clj)" > /tmp/h17b.txt 2>&1
diff /tmp/h17.txt /tmp/h17b.txt   # clojure 出力本体 0 行差 (決定的)
```

## コア (giemon-sim) への 1 行メッセージ
falsify-015: H17 survived — gate :permit の下流面 (返却レコード +
action-permitted?) は payload (tau/velocity 1e6) にも mission 境界
にも無相関・決定的 (11 ケース、レコードに tau/boundary 語 0 件、
2 回実行 diff 0 行)。payload を検査する下流消費者は存在せず、
gate↔arm の torque 照合は gate 上流・下流の両面で未接続のまま。
