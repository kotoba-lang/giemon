# falsify-21 — `torque-headroom` / `bom` が同名 joint 重複を検知せず、weak actuator の underrated 判定が無音消滅

日時: cron iteration (JST 2026-09-04, host load avg 23-39 → 軽量 in-memory REPL 測定のみ、fixture 読み込みなし)

## 仮説

falsify-6/10/11 は nil-BOM / 件数不一致 / 非有限の面を潰した。未反証の隣接面は
`arm.cljc` の **joint-name キー結合**:`torque-headroom` は
`(into {} (map (juxt :joint identity)) actuators)` で BOM を
`:joint` 名キーの map に潰してから `(:arm/chain arm)` 側の
`:joint/name` で引いている。`bom` の variant override も
`(keep-indexed #(when (= (:joint %2) joint-name) %1))` で**最初の同名 joint
1 件だけ**を置換する。よって:

- `:arm/chain` に同名 joint が 2 件 (DR 撹拌や fixture 編集ミスで
  `:joint/name` が重複) あると、`torque-headroom` は **chain の 2 番目の
  joint の required に 1 番目の joint の actuator の rated を対応付けてしまう**
  (positional 結合が name 結合に置き換わる)。weak actuator の
  underrated (負 headroom) が無音に消滅しないか。

## 実測

コード: `src/kotoba/giemon/arm.cljk` (chain-actuators L43-56, bom L60-84,
torque-headroom L86-106)。実行: `kbb -M /tmp/f21.clj`
(同名 "j1" × 2 joint: joint1 effort 5.0 + actuator A-weak cont 3.0、
joint2 effort 10.0 + actuator B-strong cont 12.0)。

```
:chain-actuators [{:joint "j1", :model "A-weak",   :cont-nm 3.0,  :peak-nm 6.0}
                  {:joint "j1", :model "B-strong", :cont-nm 12.0, :peak-nm 20.0}]
  (BOM 自体は位置どおり 2 件 — 破れはここではない)
:torque-headroom ({:joint/name "j1", :torque/required 5.0,  :torque/rated 12.0, :torque/headroom 7.0}
                  {:joint/name "j1", :torque/required 10.0, :torque/rated 12.0, :torque/headroom 2.0})
  ← 正しい位置対応なら joint1 は rated 3.0 / headroom -2.0 (underrated)
    であるべきが、name 結合で B-strong の 12.0 が joint1 に転用され
    headroom +7.0 の「余裕あり」に無音変換
:underrated ()   ← 本来 1 件あるはずの underrated 判定が無音に空
  (正しい対応での期待値: joint1 headroom -2.0 / joint2 headroom +2.0)
:bom-heavy       [{:joint "j1", :model "C", :cont-nm 30.0, ...} {:joint "j1", :model "B-strong", ...}]
  (variant override "j1" は最初の同名 joint しか置換しない — 2 件目は無音放置)
:headroom-heavy  ({... required 5.0 rated 12.0 headroom 7.0} {... required 10.0 rated 12.0 headroom 2.0})
  (C-30.0 が BOM に入っているのに torque-headroom には一切現れない —
   name 結合で同じ "j1" スロットに潰され、検証経路から無音脱落)
```

読み取り:

- 同名 joint 重複 1 文字の破損で、**underrated-joints が負判定を無音に
  消す** (torque 安全検証の偽陰性)。falsify-6 の「未割当 joint 無音
  スキップ」と同型だが、こちらは truthy な割当があっても **別 joint の
  actuator で上書き検証される**点が新しい破れ。
- `bom` の variant override も同名 2 件目に届かず、override した
  actuator が検証経路 (`torque-headroom` の by-joint map) から無音脱落 —
  variant 検証が見かけ上通過する。
- `underrated-joints` / `torque-headroom` は重複名を一切警告しない
  (例外・返却値のどちらにも痕跡なし)。

## verdict: **refuted** (同名 joint 重複で required↔rated の位置対応が無音破れ、underrated 判定消滅 + variant override の無音脱落を実測)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb -M -e '(require (quote [kotoba.giemon.arm :as arm]))
(def spec {:arm/chain
           [{:joint/name "j1" :joint/limit {:effort 5.0}
             :joint/actuator {:model "A-weak" :cont-nm 3.0 :peak-nm 6.0}}
            {:joint/name "j1" :joint/limit {:effort 10.0}
             :joint/actuator {:model "B-strong" :cont-nm 12.0 :peak-nm 20.0}}]})
(prn (arm/underrated-joints spec))'
;; => ()   (本来は joint1 の headroom -2.0 が 1 件返るべき)
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-21 実測 — `arm/torque-headroom` は BOM を `:joint`
名キーの map に潰すため同名 joint 重複で required↔rated の位置対応が無音破れ
(weak actuator の underrated -2.0 が +7.0 に変換され `underrated-joints` が
無音空)、`bom` の variant override も同名 2 件目に届かず検証経路から無音脱落。
修理: `chain-actuators` (または torque-headroom 入口) で
`(count (distinct (map :joint actuators))) == (count actuators)` と
chain 側 `:joint/name` の distinct 一致検査 (重複は例外化) —
falsify-6/10/11 の BOM 件数検査と同一箇所に追加可能。
