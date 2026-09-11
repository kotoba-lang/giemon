# falsify-2 — chain 埋め込み文字列は 2 段階 read-string で回収可能か (falsify-1 の範囲検証)

## 仮説

falsify-1 の記述「EDN リーダの結果には joint/link の EDN 構造が 1 つも存在しない」から、
「chain の文字列リテラルは何らの EDN リーダでも joint データとして回収できない」ことが
導かれるはず。これを反証する: 埋め込み文字列自体が妥当な EDN であり、2 段階 read-string で
joint 6 個が数値パリティ付きで回収できるなら、falsify-1 の主張は過広となる。

## 実測

- `clojure.edn/read-string` 1 段階目: `:arm/chain` -> java.lang.String (falsify-1 どおり)。
- その文字列に対し `clojure.edn/read-string` 2 段階目: **成功**。vector, count 6。
- 回収された 6 joint の数値を URDF (xml パース) と突き合わせ、**全項目一致**:
  - j1 axis [0 0 1], origin [0 0 0.08], limit lower -3.0 / upper 3.0 / effort 40 / velocity 3
  - j2 axis [0 1 0], origin [0 0 0.06], limit -2.2/2.2/40/3
  - j3 axis [0 1 0], origin [0 0 0.18], limit -2.5/2.5/30/3
  - j4 axis [0 0 1], origin [0 0 0.14], limit -3.0/3.0/14/4
  - j5 axis [0 1 0], origin [0 0 0.10], limit -2.0/2.0/10/4
  - j6 axis [0 0 1], origin [0 0 0.06], limit -3.0/3.0/6/5
  - URDF 側 joint axis/origin/limit (lower, upper, effort, velocity) は上記と全て一致。
  - origin xyz は URDF 側 `0 0 0.08` 形式、EDN 側 `[0 0 0.08]` で一致。rpy は両側 0。
- `:arm/realization` 文字列も 2 段階 read-string で map に回収可能
  (keys: [:status :default :torque-rule :key-finding :single-source :variants
  :encoder-comms-ok :unresolved], :status :gate0-resolved)。
- ただし 1 段階目の EDN top-level 構造に joint/link データが無い事実は不変 (falsify-1 再確認:
  `:arm/chain` の型は依然 java.lang.String)。URDF 側は joint 6 / link 7 で変化なし。

## verdict

**survived (falsify-1 の核心は維持) / ただし範囲修正** —
「EDN top-level に joint/link が EDN データとして存在せず、1 段階の from_edn では
パリティオラクルにならない」主張は破れなかった (survived)。
一方、「joint データを一切回収できない」解釈は refuted: 埋め込み文字列は妥当 EDN で、
2 段階 read-string により joint 6 個が URDF と数値一致で回収できる。
データの損失は無く、問題は純粋に入れ子構造 (ダブルエンコード) のみ。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb -M -e "(require '[clojure.edn]) \
  (def m (first (clojure.edn/read-string (slurp \"fixtures/giemon_arm6/giemon_arm6.edn\")))) \
  (def inner (clojure.edn/read-string (:arm/chain m))) \
  (prn (count inner)) (doseq [j inner] (prn (select-keys j [:joint/name :joint/axis :joint/origin :joint/limit])))"
# => 6 / 上表の数値
python3 -c "import xml.etree.ElementTree as ET; r=ET.parse('fixtures/giemon_arm6/giemon_arm6.urdf').getroot(); \
  [print(j.get('name'), j.find('axis').get('xyz'), j.find('origin').get('xyz'), \
   j.find('limit').attrib) for j in r.findall('joint')]"
# => 同じ数値 (突き合わせ)
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-2 実測 — chain 文字列は妥当 EDN で 2 段階 read-string すれば joint 6 個が
URDF と数値完全一致で回収できる (データ損失なし)。修理は展開し直すだけでよく、
1 段階の EDN として joint/link が出てくる形にすれば L0 パリティの材料は全て揃っている。
