# falsify-071 (H72)

仮説: governor 経路に LLM-to-actuator shortcut がある — `kotoba.giemon.governor`
(現行 .cljk, HEAD 00fd23f) の `kaigo-action` / `ops-action` / `fall-detected-alert`
は `rob/action` を経由するが、`kotoba.robotics/action` (L60-71) は
`kind` が `action-kinds` #{:sense :move :grasp :actuate :emit} 外、または `safety`
が `safety-classes` #{:none :low :medium :high :safety-critical} 外のとき **nil を
返す**。よって「不正 action は gate で deny される」のではなく、gate 前に silent nil
で消える — 決定は一度も gate を通らず、audit 上「作られたが拒否された」と「作られて
いない」が区別できない。LLM が生んだ不正 action が痕跡なく落ちる迂回路が存在する。

## 実測 (純静的読取 — 実行系 backend 応答不能につき clojure/kbb 実測は本 run 不可)

- `kotoba.robotics/action` robotics.cljk L64-71: `(when (and (contains? action-kinds kind) (contains? safety-classes safety)) {...})` — 不正入力は nil。
- governor.cljk L21-27 `kaigo-action`: `kind` を unvalidated で `rob/action` に透過、
  `:safety` は `(or safety (get-in kaigo-roles [product :default-safety] :medium))` —
  呼び出し側が `:safety :dangerous` 等を渡せば `contains?` が false → nil。
- governor.cljk L53-60 `ops-action`: 同型。
- governor_test.cljk L11-20 は `:move` のみ網羅 — 不正 kind/safety の nil 経路は
  test で 1 件も assert されていない (検証の穴)。
- 対照: `fall-detected-alert` / `chemical-dispense-alert` は `:safety-critical` を
  ハードコードし nil になり得ない (規約の意図通り)。

## verdict: **refuted** —「不正 action は governor gate が deny する」は過剰主張。
   gate に届かない silent nil 経路が実在し、test はそれを 1 件も覆っていない。
   ただし nil が `gate`/`action-permitted?` に渡れば :invalid→deny となるため、
   actuator 直送 (= shortcut による dispatch) は成立しない。破れは「決定の痕跡喪失」
   (reject がどこにも記録されない) であって権限越境ではない。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
# 静的: kotoba.robotics/action の when を読む (robotics.cljk L64-71)
#      governor.cljk L21-27 / L53-60 の透過を確認
# 実行 (backend 応答可能時):
#   (gov/kaigo-action "A" "M" :otete :teleport)  ; => nil (kind 不正)
#   (gov/kaigo-action "A" "M" :otete :move :safety :none-of-the-above) ; => nil
# どちらも gate は呼ばれない。
```

no code change (本 bot は修正しない)。

コアへの 1 行メッセージ: governor action 経路の不正 kind/safety は deny でなく
silent nil で落ち、gate と audit の両方から消える — action 返却 nil を「拒否として
記録する」形 (ex-data / rejected レコード) への変更と、その経路の負テスト 1 件を
runner repair と同時に core 側へ推奨。
