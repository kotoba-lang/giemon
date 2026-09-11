# falsify-26 — caterpillar_facade URDF は XML として読めない (パリティオラクルの不成立) + boom 4-joint 数値パリティ

日付: cron (2026-09-04, bench-34 以降, load 31-45/10 なので軽量実験)
対象: fixtures/giemon_caterpillar_facade/ — falsify-2/3/4 が giemon_arm6 に対して実施した
URDF↔EDN パリティ検査が facade fixture では一度も行われていなかったため埋める。

## 仮説

facade fixture は「URDF を :chassis/boom 部分の parity oracle として
from_edn(edn) == parse_urdf(urdf) を検証する」とファイル先頭で宣言しているが、
この URDF は標準 XML パーサで読めないため、オラクルとして機能していない。
(直接の前例: falsify-1 — giemon_arm6.edn の二重エンコードで oracle 機能せず、
同型の「宣言された oracle が道具として壊れている」を facade URDF 側で探す)

## 実測

### (a) URDF の XML well-formedness — FAIL

- 標準 Python ElementTree:
  `ParseError: not well-formed (invalid token): line 9, column 25`
- JVM (javax.xml.parsers.DocumentBuilderFactory, doctype 禁止設定):
  `[Fatal Error] giemon_caterpillar_facade.urdf:9:26: コメント内では文字列"--"は使用できません。`
- 原因: 9 行目の XML コメント内に裸の `--` (`で自然に表現できないためEDN専用 -- 詳細は…`)。
  XML 仕様 (§2.5) はコメント内の `--` を禁止する。2 行目の em-dash (`—`) は問題ない。
- 対照: fixtures/giemon_arm6/giemon_arm6.urdf は同一確認方法で parse OK
  (コメント内に裸 `--` 無し)。
- 影響: どの準拠 XML パーサでも `parse_urdf(urdf)` が例外で落ちるため、
  fixture が宣言する `from_edn(edn) == parse_urdf(urdf)` 検証は現状のまま
  実行不可能 (boilerplate コメントを消せば初めて読める)。EDN 側の読み取りも
  2 段階 unblob 前提であり、オラクルの両足が道具として壊れている。

### (b) boom 4-joint 数値パリティ (コメント剥がし URDF vs 2 段階 read EDN) — 完全一致

コメント剥がし (正規表現で `<!--.*?-->`除去) 後にパースした URDF の数値と、
EDN を unblob 2 段階 read した :chassis/boom :arm/chain を比較:

- joint 4 件 / 4 件、joint 名・type (:revolute)・parent/child link 名 一致
- origin xyz: j_boom_yaw [-0.150,0,0.10] / j_boom_lift [0,0,0.05] /
  j_boom_reach [0,0,0.35] / j_nozzle_wrist [0,0,0.30] — 全一致
  (0 と 0.0、-0.15 と -0.150 は数値として同値)
- axis: [0,0,1] / [0,1,0] / [0,1,0] / [1,0,0] — 一致
- limit lower/upper/effort/velocity: (-2.0,2.0,8,2.5) / (-0.2,1.6,25,1.5) /
  (-2.0,0.3,15,1.5) / (-1.6,1.6,3,3.0) — 全一致
- damping: 0.05 / 0.08 / 0.06 / 0.02 — 全一致
- link 5 件 (base_link + boom 4) の inertial origin / mass / inertia
  ixx,iyy,izz,ixy,ixz,iyz — 全一致 (base_link 9.5kg 含む)

つまり内容のドリフトは無し (falsify-4 の arm6 ドリフト検査の facade 版に相当)。
壊れているのはオラクルファイルの XML 自体の読み可能性のみ。

## Verdict: **refuted** (facade URDF はコメント内の裸 `--` (9 行目) により
標準 XML パーサ (Python ElementTree / JVM DocumentBuilderFactory 両方) で
パース不可 — fixture 先頭が宣言する「URDF parity oracle」として機能しない。
内容面の boom 4-joint / 5-link 数値パリティ自体はコメント剥がし後に完全一致)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
# (a) oracle が読めない実測
clojure -M -e '(require (quote [clojure.java.io :as io]))
(import (quote javax.xml.parsers.DocumentBuilderFactory))
(let [f (javax.xml.parsers.DocumentBuilderFactory/newInstance) b (.newDocumentBuilder f)]
  (.parse b (io/file "fixtures/giemon_caterpillar_facade/giemon_caterpillar_facade.urdf")))'
;; => Fatal Error 9:26 コメント内では文字列"--"は使用できません
python3 -c "import xml.etree.ElementTree as ET; ET.parse('fixtures/giemon_caterpillar_facade/giemon_caterpillar_facade.urdf')"
# => ParseError: not well-formed (invalid token): line 9, column 25
# 対照: fixtures/giemon_arm6/giemon_arm6.urdf は両パーサで OK
# (b) パリティ本体: コメント剥がし URDF vs test/kotoba/giemon/chassis_edn_test.cljk
#     の unblob/reconstitute-chassis 2 段階 read — 上記実測欄の通り 4 joint / 5 link 全一致
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-26 実測 — `fixtures/giemon_caterpillar_facade/giemon_caterpillar_facade.urdf`
は 9 行目 XML コメント内の裸 `--` により標準 XML パーサ (Python/JVM 両方) で
パース不可で、fixture 先頭が宣言する parity oracle として機能しない
(falsify-1 の EDN 二重エンコードの URDF 版・facade 版)。修理: コメント内の
`--` を `—` 等に書き換えるのみ (データ損失 0、内容面のパリティは
boom 4-joint/5-link 全一致で本日実測済みのため書き換え後の数値リスクなし)。
副: EDN 側の二重エンコード (:chassis/base / :chassis/realization / :chassis/boom
等 7 キーが pr-str blob) は falsify-1 と同型の未修理事項として残る
(chassis_edn_test.clj の unblob が迂回コードとして常駐している)。
