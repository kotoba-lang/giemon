# falsify-009 — caterpillar URDF の well-formedness 赤はコメントのみか (falsify-008 赤の反証)

## 仮説 (1 iteration = 1 hypothesis)
H11: 「falsify-008 の ParseError (line 9 コメント内 `--`) は唯一の well-formedness
障害であり、コメントを除いた本体 XML は well-formed かつ EDN boom chain と
数値整合する」 — 反証対象は falsify-008 の記録
「caterpillar 側 parity oracle は fixture 修正しない限り成立不能」。
コメント除去後も parse 不成立 / 数値不一致が残れば H11 は破れる。

## 測定 (probe_caterpillar_wf.py — fixture は一切修正しない)
```
STEP1 raw_parse=ParseError: not well-formed (invalid token): line 9, column 25
STEP2 comment_stripped_parse=ok links=5 joints=4
STEP3 urdf_inertia_links=5 missing_attr=none
STEP4 edn_named_links=['base_link', 'boom_link1', 'boom_link2', 'boom_mast_link', 'nozzle_link'] blocks_total=5
STEP5 mismatch=0 (0-default 読みで全一致)
SUMMARY raw=wf_fail stripped=wf_ok links=5 joints=4 urdf_in=5 edn_in=5 mismatch=0
```
- 2 回実行して出力同一 (決定的、cmp 一致)。EXIT=0。
- 測定内容:
  1. falsify-008 の赤を再現: 生 URDF は line 9 col 25 (コメント内 `--`) で
     ParseError — falsify-008 の記録と同一。
  2. XML コメント全体を除去したのみのテキストは **well-formed**
     (links=5 / joints=4、要素構造は無傷)。つまり ill-formed の原因は
     コメント 1 箇所のみで、本体 XML に別の障害はない。
  3. URDF 5 link の inertia は 6 成分すべて明示 (missing_attr なし)。
  4. EDN (正本) の pr-str blob から 5 link 名を抽出し、各 :inertia block と対応。
  5. 0-default 読み (EDN で省略された off-diagonal = 0) で URDF と照合:
     **mismatch=0** — 5 link × 6 成分すべて数値一致
     (caterpillar の offdiag 省略 link 4 本も URDF 値 0 と整合、falsify-008 の
     EDN 側観察と一致)。
- probe 実装メモ: EDN pr-str blob 内の `:name \"X\"` はリテラル
  backslash+quote のため、正規表現は `:name\s*\\"([A-Za-z0-9_]+)\\"` 形
  (backslash を `\.` ではなく `\\` で受ける)。初版 3 つの naive パターンは
  0 match / 隣接 link 誤対応となり却下 (試行過程は本 probe の履歴参照)。

## verdict
- H11: **refuted の方向で survived 判定の弱体化 — 判定: survived (部分的)**。
  正確には:
  - 「caterpillar URDF は本体的にも壊れている」仮定は **refuted**:
    ill-formedness は XML コメント内 `--` の 1 箇所のみで、コメント除去後は
    well-formed かつ EDN と数値完全一致 (mismatch=0)。
  - しかし falsify-008 の主記録「fixture 修正しない限り parity oracle は
    成立不能」は **survived**: 標準 XML parser はコメントをスキップせず
    ParseError で落ちるため、fixture テキストを変更しない限り
    parse_urdf ベースの oracle は caterpillar で成立しないまま。
    修正は 1 行 (コメント内 `--` を `:` 等に置換) で済むが、fixture 修正は
    コア (giemon-sim) の仕事であり本 bot は実施しない。

## コアへの 1 行メッセージ
giemon-sim へ: caterpillar URDF の well-formedness 赤はコメント内 `--` の
1 箇所のみ (本体 XML と EDN 照合はコメント除去後 well-formed・mismatch=0 で
完全成立)。fixture のコメント 1 行修正 (例: `--` → `:`) だけで
caterpillar 側 parity oracle は成立可能になる — 最小修正で赤を消せる。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_caterpillar_wf.py   # 2 回実行して出力同一を確認
```

## 補足
- コード修正なし (probe 追加と記録のみ。fixture は未変更)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD 高負荷 (load averages 221.21 226.14 187.26) — 軽量 XML/数値照合
  probe のため falsify cheaply 基準で実施可と判断。深いシミュレーションは省略。
- ツール環境メモ: 本 iteration では terminal stdout が空で返る障害があり
  出力はファイルリダイレクト + read_file で取得、execute_code は cron で
  block、rm は Tirith security scan で block のため debug 用 tmp_*.py
  (evidence/tmp_dbg.py 等 4 ファイル) が evidence に残っている (実験本体
  probe_caterpillar_wf.py には影響なし)。
