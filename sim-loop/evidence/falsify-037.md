# falsify-037 — H38 (監査ツール陳腐化の真因: falsify-035 の「二重バックスラッシュ片側畳み」帰属は正しいか)

- 連続番号: 037 (falsify-036 の後続)
- 日次: 260908
- 採択元: status/maturity.md NEXT (b) — falsify-035 付随の監査ツール陳腐化
  (probe_parity_arm6.py の escape 畳み) を深掘りする probe。
- 仮説 (H38, 反証対象「監査ツール陳腐化の真因」): falsify-035 が記録した
  「shipped probe_parity_arm6.py は現行 EDN blob の**二重バックスラッシュ** `\\"`
  エスケープに片側 (`\"` のみ) しか畳んでおらず PARSE-ERR → exit 1」という帰属が
  正しい — つまり escape 畳み不足がクラッシュの真因である。
- 実測 (決定的、純計算。terminal foreground stdout 応答不能のため `/tmp` redirect →
  read_file で回収、捏造なし):
  - **escape 実態 (byte 計数)**: `:arm/chain` blob 中、`\"` (backslash-quote) は
    **82 件**、`\\"` (backslash-backslash-quote) は **0 件**、リテラル `\\` は
    **存在しない** (`has_literal_dbl_backslash = False`)。→ 現行 blob は
    **二重バックスラッシュ escape を含まない**。
  - **単一 fold の十分性**: shipped probe と同じ単一 fold
    `.replace('\\"','"')` 後、`:joint/name` 6 件・`{:joint/axis` 6 件が全て
    復元 (SINGLE fold: joint/name after=6, axis-objs=6)。→ **escape 畳みは
    単一 fold で完全に足りる** (falsify-035 の「片側しか畳んでいない」は不成立)。
  - **真因 (slice anchor)**: shipped probe の join 正規表現は
    `:joint/name "(j\d)"(.{0,1200}?)\}\} (?=\{:joint/axis|\Z)` で **name の後**を
    body として捕捉するが、EDN map 内のキー並びは
    `{:joint/axis ... , :joint/type ..., :joint/name ...}` と **`:joint/axis` が
    `:joint/name` より前に現れる**。従って捕捉 body に `:joint/axis` が含まれず、
    `re.search(r':joint/axis \[([^\]]+)\]', body)` が None → line 42
    `AttributeError: 'NoneType' object has no attribute 'group'` → exit 1。
    - SHIPPED slice (single-fold): `[('j1', None), ('j2', None), ('j3', None),
      ('j4', None), ('j5', None)]` — **6 joint 中 5 件が axis=None** (j6 は
      `\Z` 側で別途捕捉されるが同様に body に axis なし)。
    - SHIPPED slice (double-fold でも): 全く同じ `None` — **escape 畳みレベルは
      結果に無関係** (真因は slice anchor のみ)。
  - 再現実行: `python3 sim-loop/evidence/probe_parity_arm6.py` → exit 1、line 42
    AttributeError (falsify-035 と同じ PARSE-ERR が現行 blob で再現)。
  - 測定時 HOST LOAD: 開始前 6.99 / 8.73 / 10.75 (ncpu=10 の約 0.7-1.1 倍、軽負荷)。
    軽量 python 2 本 (shipped probe 再現 + 独立 anchor probe) を EXIT 0 で完遂
    (`/tmp` redirect workaround)。
- verdict: **refuted** — 仮説 (「falsify-035 の escape 帰属が正しい」) は不成立。
  監査ツールの陳腐化自体は**再現確認された** (exit 1 で完走不能) が、その真因は
  falsify-035 が記録した「二重バックスラッシュ escape の片側畳み」**ではない**。
  現行 blob は二重バックスラッシュを一切含まず、単一 fold で escape は完全復元される。
  真因は **slice anchor** — `:joint/name` 起点の body 捕捉が、map 内で name より
  前に現れる `:joint/axis` を除外するため、axis 取得が常に None になる構造的バグ。
  (falsify-035 の本丸結論「URDF↔EDN パリティは無破れ」は falsify-035_parity_probe.py
  の独立パーサで実測済みで、本 walk はそれを覆さない。)
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  python3 sim-loop/evidence/probe_parity_arm6.py > /tmp/o.txt 2>&1; echo $?
  # → exit 1, line 42 AttributeError (PARSE-ERR 再現)
  python3 /tmp/probe_anchor.py > /tmp/o2.txt 2>&1   # 独立 anchor probe
  # → escape 実態: backslash_quote=82, backslash_backslash_quote=0
  ```
- 検証内訳 (本 walk の 1 仮説・1 実測判定): 1 仮説 (H38) / 測定 1 (escape 実態
  byte 計数 + slice anchor 捕捉結果の決定的比較) / 判定 refuted (escape 帰属は
  不成立、真因は slice anchor)。
- コアへの 1 行: probe_parity_arm6.py の陳腐化は再現 (exit 1) だが真因は escape
  畳み不足ではなく **slice anchor バグ** (`:joint/name` 起点捕捉が map 内で先行する
  `:joint/axis` を除外、現行 blob は二重バックスラッシュを一切含まず単一 fold で
  十分) — 監査修復時は name 起点 slice を `:joint/axis` 起点に変更すべき
  (本 bot は実装・コード変更なし)。