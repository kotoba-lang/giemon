# falsify-5 — torque 余裕違反シナリオ: 実コード torque-headroom が fixture で underrated を返すか

## 仮説

`kotoba.giemon.arm/torque-headroom` (実装済みの実コード) に fixtures/giemon_arm6 の
arm 仕様を渡すと、どこかの joint で actuator の連続トルクが設計要求 (`:joint/limit :effort`)
を下回り (`:torque/headroom` < 0)、`:arm/realization` の主張
(「:all-qdd 構成で肩40N·m律速・全 joint 可」「j5 余裕僅少」) が **欺ける**。

## 実測 (2026-09-03, JST)

- 前提確認: fixture は未修理 (`grep -c '\\"j1\\"'` -> **1**、`:arm/chain` / `:arm/base` /
  `:arm/realization` すべて java.lang.String のまま)。
  そのため 1段階 EDN では arm データが出ず、falsify-2/3 と同じ 2段階 read
  (外側 clojure.edn -> `:arm/chain` 文字列を再度 read) で joint 6 のベクタを復元し、
  `{:arm/chain <2段階read結果>}` として実コードへ渡した (全 fixture そのまま、加工なし)。
- `arm/torque-headroom` 実測 (joint / required / rated / headroom, N·m):

| joint | required (effort) | rated (cont-nm) | headroom |
|---|---|---|---|
| j1 | 40 | 40 | 0 |
| j2 | 40 | 40 | 0 |
| j3 | 30 | 40 | +10 |
| j4 | 14 | 20 | +6 |
| j5 | 10 | 10 | 0 |
| j6 | 6 | 8.3 | +2.3 |

- `arm/underrated-joints` -> **0 件** (negative headroom なし)。
- `:arm/realization` の記述と照合: 「j5 余裕僅少」= headroom 0、「肩40N·m律速」= j1/j2 headroom 0 —
  数値は主張と完全に整合し、矛盾 (欺ける入力) は検出されなかった。
- 付帯観察: `:arm/realization` 自体も二重エンコード文字列 (java.lang.String) であり、
  1段階 EDN では actuator/variant データが出ない。修理対象リストは
  :arm/chain + :arm/base + :arm/realization の 3 キーとなる。

## verdict

**survived** — 実コード torque-headroom でも underrated joint は 0 件、
`:arm/realization` の主張と数値整合。torque 検証経路の欺きは見つからなかった。
falsify-1 (refuted) のパリティ構造破れは引き続き OPEN (実コードに渡す前に
2段階 read が必要という形でのみ影響が残存)。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
grep -c '\\"j1\\"' fixtures/giemon_arm6/giemon_arm6.edn   # => 1 (未修理)
kbb -M -e "
(require '[clojure.edn] '[kotoba.giemon.arm :as arm])
(def m (first (clojure.edn/read-string (slurp \"fixtures/giemon_arm6/giemon_arm6.edn\"))))
(def arm-spec {:arm/chain (clojure.edn/read-string (:arm/chain m))})
(doseq [t (arm/torque-headroom arm-spec)]
  (prn (:joint/name t) (:torque/required t) (:torque/rated t) (:torque/headroom t)))
(prn 'underrated= (count (arm/underrated-joints arm-spec)))"
# => j1 40 40 0 / j2 40 40 0 / j3 30 40 10 / j4 14 20 6 / j5 10 10 0 / j6 6 8.3 2.3 / underrated= 0
```

## コアへの 1 行メッセージ

giemon-sim へ: torque 経路の数値は反証されなかった (underrated 0、j1/j2/j5 headroom 0)。
fixture 修理の対象は `:arm/chain` / `:arm/base` に加えて **`:arm/realization` も二重エンコード文字列**
なので、3 キーを 1段階 EDN データに展開すること。
