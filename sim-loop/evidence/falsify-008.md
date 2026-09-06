# falsify-008 — off-diagonal inertia の 0-default 暗黙契約は parity を破るか (falsify-001 破れ候補 No.1)

## 仮説 (1 iteration = 1 hypothesis)
H10: 「EDN fixture の child link `:inertia` は `ixy/ixz/iyz` を省略し、URDF は明示 `0`
(= falsify-001 が記録した 0-default 暗黙契約)。from_edn 相当の loader が 0-default
しない (strict 読み: 6 key 必須) 実装なら URDF↔EDN parity はここで破れる」 —
反証対象は **「0-default の省略があっても parity は成立する」という fixture 冒頭
コメント (parity oracle) の主張**。仮に 0-default でも数値不一致 (省略≠URDF 値) が
1 件でも見つかれば、その逆 (省略=0 でない link がある) で H10 は破れる。

## 測定 (probe_offdiag_inertia.py — evidence 配下の準備済み probe を実行)
```
== giemon_arm6 ==
  urdf links with inertial : 7
  edn :inertia blocks      : 7 (names: ['base_link', 'link1', ..., 'link6'])
  base_link: 一致 (0-default) [明示0] missing=-
  link1〜link6: 一致 (0-default) [offdiag省略] missing=['ixy', 'ixz', 'iyz']
  EDN offdiag 省略 link    : 6/7
  EDN 明示 0 offdiag key   : 3 (base_link の ixy/ixz/iyz)
  strict 読みで落ちる link : 6/7
  0-default でも数値不一致 : 0 link
== giemon_caterpillar_facade ==
  URDF well-formedness: FAILED -- ParseError: not well-formed (invalid token):
    line 9, column 25 <-- RED (parse_urdf 不能)
  (参考) URDF 内 <inertia タグ数: 5; EDN :inertia blocks: 5
== parity oracle 実装個数 (giemon src/test の .clj/.cljc) ==
  parse_urdf/from_edn 系文字列ヒット: 1 ['arm.cljc:from_edn']
  (arm.cljc のヒットは docstring 内の camelize 参照のみ、Clojure 関数実装ではない)
SUMMARY giemon_arm6:missing=6,explicit0=3,strict_fail=6,mismatch=0
        giemon_caterpillar_facade:wf_fail oracle_impl=1
EXIT=0
```
- 2 回実行して diff なし (決定的、cmp 一致)。
- 補足測定 (同日実施、fixture テキスト直接読み):
  - caterpillar URDF の ParseError 原因は **XML コメント内の `--`** (line 9:
    「EDN専用 -- 詳細は …」)。XML 仕様上コメント内の `--` は不正で、
    Python ET / 標準 XML parser は全員 parse に失敗する。fixture 修正は
    コード修正に当たるため本 bot は実施せず、測定結果としてのみ記録。
  - caterpillar EDN の :inertia blocks 5 件のうち offdiag を省略しているのは
    4 link (base_link は明示 0)。arm6 同様 0-default 前提で URDF 値と整合する構成。
  - arm6 URDF 全 link の offdiag 値は **すべて 0** (nonzero offdiag: none) —
    つまり「省略≠URDF 値」の破れは現 fixture には存在しない。

## verdict
- H10 (0-default 省略は parity を破る): **survived (数値不一致は発生せず)** —
  現 fixture の限りでは省略 key の URDF 値はすべて 0 で、0-default 読みなら
  mismatches 0 は維持される (falsify-001 の結果を機械的に再確認)。
- ただし H10 が survived なのは「0-default を前提とする loader のみ」で、
  **strict 読み (6 key 必須) の loader なら 7 link 中 6 link で落ちる**
  (strict_fail=6/7)。0-default は暗黙契約のまま実装されておらず、
  falsify-001 の「破れ候補 No.1」は構造的には未解消。
- 新たな構造的赤 (falsify-001 では未記録):
  (a) **giemon_caterpillar_facade.urdf は XML として well-formed でない**
      (コメント内 `--`)。parse_urdf 前提の parity oracle は arm6 だけでなく
      caterpillar ではそもそも成立不能 (fixture 修正が必要)。
  (b) parity oracle (`from_edn(edn) == parse_urdf(urdf)`) の Clojure 実装は
      引き続き存在しない (falsify-001 の赤を再確認)。

## コアへの 1 行メッセージ
giemon-sim へ: offdiag 0-default は現 fixture では数値一致するが strict 読みでは
6/7 link が落ちる暗黙契約のまま。さらに giemon_caterpillar_facade.urdf は
XML コメント内 `--` (line 9) のため well-formed でなく、標準 XML parser では
parse 不能 — caterpillar 側の parity oracle は fixture 修正しない限り成立不能。
from_edn==parse_urdf の自動検証 (Clojure 実装) も引き続き未実装。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_offdiag_inertia.py   # 2 回実行して diff なしを確認
# (対比) python3 sim-loop/evidence/probe_parity_arm6.py   # falsify-001 (arm6 全体 parity)
```

## 補足
- コード修正なし (probe 実行と記録のみ。caterpillar URDF のコメント内 `--` も
  fixture 修正せず記録のみ)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD 中負荷 (load averages 4.78 12.07 16.75 / ncpu 10) — 軽量数値解析
  probe のため実施可と判断。長時間シミュレーションは省略 (falsify cheaply)。
