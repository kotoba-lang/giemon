# falsify-4 — falsify-2/3 の 2段階 read 数値パリティの再現 (fixture 変化ドリフト検査)

## 仮説

falsify-2 (joint 6) / falsify-3 (link 7) の数値パリティ以降に fixture が変化しており、
2段階 read での URDF↔EDN 数値一致が **破れている** (または修理済みで 1段階 read が通る)。

## 実測 (2026-09-03, JST)

- 修理状態: 未修理。`grep -c '\\"j1\\"' fixtures/giemon_arm6/giemon_arm6.edn` -> **1**
  (falsify-1/3 と同一。ダブルエンコードのまま)。
- 2段階 read (外側 clojure.edn -> :arm/chain 文字列を再度 read):
  - joints: **6** (j1..j6, 全部 :revolute)
  - URDF (giemon_arm6.urdf, joint 6 / link 7) との数値比較、全項目一致:
    - axis: j1 [0 0 1], j2 [0 1 0], j3 [0 1 0], j4 [0 0 1], j5 [0 1 0], j6 [0 0 1] — 一致
    - origin xyz: 0.08 / 0.06 / 0.18 / 0.14 / 0.10 / 0.06 — 一致
    - limit lower/upper: -3/3, -2.2/2.2, -2.5/2.5, -3/3, -2/2, -3/3 — 一致
    - effort/velocity: 40/3, 40/3, 30/3, 14/4, 10/4, 6/5 — 一致
    - parent/child: base_link→link1→…→link6 — 一致
  - link 質量/慣性原点: 0.6@0.03, 0.5@0.09, 0.35@0.07, 0.22@0.04, 0.16@0.03, 0.12@0.025 — 一致
- **新規付帯実測**: `:arm/base` もまだ文字列リテラル内に二重エンコードされている
  (外側 read 後も java.lang.String、中身 `\"#:link{:name \"base_link\", ... :mass 2.0 ...}\"`)。
  つまり link 7 個のうち base_link の 1 個だけが chain の :child/link に存在せず、
  2段階 read でも EDN データとして出ない (mass 2.0 @ origin [0 0 0.04] は URDF 側のみ確認)。
  修理計画 (maturity NEXT) に `:arm/base` が含まれているのは正しいが、
  「:arm/base は 1 段階で済む」ではない — chain と同段階のエスケープが残っている。

## verdict

**survived** — 2段階 read での joint 6 / link 6 数値パリティは現時点でも完全一致で破れていない。
fixture も未修理のままドリフトなし。falsify-1 (refuted) は引き続き OPEN。
付帯観察: `:arm/base` の二重エンコードも未解消で、修理対象に含まれることを再確認。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
grep -c '\\"j1\\"' fixtures/giemon_arm6/giemon_arm6.edn   # => 1 (未修理)
kbb -M -e "(require '[clojure.edn]) \
  (def m (first (clojure.edn/read-string (slurp \"fixtures/giemon_arm6/giemon_arm6.edn\")))) \
  (def chain (clojure.edn/read-string (:arm/chain m))) \
  (prn (count (filter #(contains? % :joint/name) chain)))  ; => 6 \
  (prn (type (:arm/base m)))"                              ; => java.lang.String (まだ二重エンコード)
python3 -c "import xml.etree.ElementTree as ET; r=ET.parse('fixtures/giemon_arm6/giemon_arm6.urdf').getroot(); \
  print(len(r.findall('joint')), len(r.findall('link')))"   # => 6 7
```

## コアへの 1 行メッセージ

giemon-sim へ: 数値は一切ドリフトしていない (joint 6 / link 6 完全一致のまま) —
NEXT の fixture 修理は安全に実施可能で、修理後は `:arm/chain` に加えて `:arm/base` も
文字列リテラルから EDN データ (link7 個目, mass 2.0) に展開すること。
