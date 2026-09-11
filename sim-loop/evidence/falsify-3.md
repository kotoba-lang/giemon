# falsify-3 — link 7 個の数値パリティ (chain 内の link データは URDF と突き合わせ可能か)

## 仮説

falsify-2 は joint 6 個の数値パリティのみ実測し、link 7 個 (mass/inertia/origin) は未測定だった。
「chain 埋め込み文字列には link データが欠落しており、URDF との link 数値パリティは定義上不可能」
を反証する: 2 段階 read-string で link 7 個が URDF と数値一致で回収できるなら過広となる。

## 実測

- 2 段階目 read-string 後の chain は joint エントリ 6 個 (`:top-count 6`)。
  link は独立エントリではなく、各 joint の `:child/link` (`#:link{...}` 名前空間 map) に
  `:link/inertial` 付きで埋め込まれている (これが falsify-3 初手の `:link/name` フィルタで
  link-count 0 と誤検出した理由。filter は joint map にかかっていた)。
- `:arm/base` 文字列も read-string 可能で `#:link{:name "base_link", :inertial {:mass 2.0, ...}}`。
- URDF (xml パース) との突き合わせ — **link 7 / 7 が数値完全一致**:

| link | origin xyz (URDF / EDN) | mass | ixx | iyy | izz |
|---|---|---|---|---|---|
| base_link | 0 0 0.04 / [0 0 0.04] | 2.0 | 0.004 | 0.004 | 0.004 |
| link1 | 0 0 0.03 / 同 | 0.6 | 0.0012 | 0.0012 | 8.0E-4 |
| link2 | 0 0 0.09 / 同 | 0.5 | 0.003 | 0.003 | 6.0E-4 |
| link3 | 0 0 0.07 / 同 | 0.35 | 0.0016 | 0.0016 | 4.0E-4 |
| link4 | 0 0 0.04 / 同 | 0.22 | 6.0E-4 | 6.0E-4 | 3.0E-4 |
| link5 | 0 0 0.03 / 同 | 0.16 | 3.0E-4 | 3.0E-4 | 2.0E-4 |
| link6 | 0 0 0.025 / 同 | 0.12 | 2.0E-4 | 2.0E-4 | 1.0E-4 |

- ixy/ixz/iyz は両側 0。EDN 側は ixx/iyy/izz のみ明記 (0 暗黙) で数値として一致。
- 前提確認: fixture は未修理のまま (grep `:joint/name "j1"` -> 0、`\\\"j1\\\"` -> 1)。
  falsify-1 の OPEN 赤は不変。
- 本測定はテキスト解析のみ (テスト・学習ジョブ不使用)。host load 1min 約 40 のため深い実験は回避。

## verdict

**survived (仮説「link データは欠落・パリティ不可能」を refuted)** —
link 7 個 (base_link + link1..6) の mass/inertia/origin は chain 内に全て存在し、
URDF と数値完全一致。joints (falsify-2) + links (本件) で **joint 6 / link 7 の
数値パリティは完全確認済み**。ただし全て 2 段階 read-string 経由であり、
1 段階 EDN として joint/link が出てこない falsify-1 の赤は残ったまま。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb -M -e "(require '[clojure.edn]) \
  (def m (first (clojure.edn/read-string (slurp \"fixtures/giemon_arm6/giemon_arm6.edn\")))) \
  (def inner (clojure.edn/read-string (:arm/chain m))) \
  (prn (:arm/base m)) (doseq [j inner] (prn (:joint/child j) (get-in j [:child/link :link/inertial])))"
python3 -c "import xml.etree.ElementTree as ET; r=ET.parse('fixtures/giemon_arm6/giemon_arm6.urdf').getroot(); \
  [print(l.get('name'), l.find('inertial/origin').get('xyz'), l.find('inertial/mass').get('value'), \
   {k: v for k, v in l.find('inertial/inertia').attrib.items()}) for l in r.findall('link')]"
# => 上表どおり数値一致
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-3 実測 — link 7 個 (base_link 含む) の mass/inertia/origin は chain 内に
存在し URDF と数値完全一致。joint 6 / link 7 の数値パリティ材料は全て揃っており、
残る障害はダブルエンコードのみ (falsify-1 のまま)。展開修理のデータ損失リスクは 0 済み。
