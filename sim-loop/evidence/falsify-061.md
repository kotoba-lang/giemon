# falsify-061 — H62 (URDF↔EDN parity 監査を独立な修正 parser で再測したら、陳腐化した監査ツールの代わりに parity 無破れを再確認でき、全 6 joint × 7 link の全数値が 1e-12 内で一致するか)

- 連続番号: 061 (falsify-060 の後続。FK guard repair は 060 まで 23 連続 refuted・HEAD d0d3cb4 不変・tracked diff 空で code 無変更が確定済みのため、今回 1 件は監査ツール陳腐化の赤 (falsify-035/037) に挑む異系仮説に充てる)
- 日次: 260909
- 採択元: status/maturity.md OPEN 赤字「監査ツール陳腐化 (falsy-037 真因 = slice anchor バグ)」+ Oracle/parity 項目「生存 (measured)」— 但し従来の parity 判定は陳腐化工具 probe_parity_arm6.py が PARSE-ERR -> exit 1 で依然機械実行不能 (falsify-035)。そのため、**動作する修正 parser で独立性の高い再監査**を行い「parity 無破れ」を再確定/反証する。
- 仮説 (H62, 反証対象「陳腐化工具の背後にある parity 無破れ結論が、正しく動作する独立 parser でも成立するか」): 陳腐化した slice-anchor 監査脚本を廃し、`:joint/axis [` 起点・次起点までの文字列分割で **axi/origin を除外せず**捕捉する修正 parser で URDF↔EDN 全数値を照合すると、全 6 joint (axis/origin/damping/lower/upper/effort/velocity) × 7 link (inertial origin/mass/inertia、base_link は off-diag ixy/ixz/iyz 含む) が 1e-12 内で皆一致し、parity 破れは 0 件である。
- 実測 (決定的、純文字解析で sim 実行なし。HOST LOAD 15min ≈18.35 (≈1.8× ncpu=10) は Load gate (15min ≥ 2×ncpu=20) 未満、且つ本測は計算皆無のテキスト照合のため負荷影響ゼロ。/tmp redirect で実測取得):
  - **新規 probe 追加**: `sim-loop/evidence/probe_parity_arm6_fixed.py` (陳腐化 probe_parity_arm6.py を置換する独立修正版)。EDN 側は正規表現のスライスanchorを使わず、join 区切りリテラル `:joint/axis [` で各 joint を先頭アンカー分割 (axis/origin 除外バグ non-occurrence)。
  - **本測定 (実物)**: `python3 sim-loop/evidence/probe_parity_arm6_fixed.py` → `joints compared: 6 URDF / 6 EDN` · `links compared: 7 URDF (incl base_link)` · **`mismatches: 0`** · exit 0。
  - **測定品質検証 (mutation test, 実物改変なし)**: 実 EDN の j1 `:effort 40` を一時コピーで 41 に変え、同一 parser で照合 → `mismatches: 1` / `MISMATCH: j1.effort: urdf=40.0 edn=41.0` / **exit 1**。→ probe は空振り false-pass でなく、実際の数値差を確実に捕捉する (verdict の測定根拠が健全)。
  - **OFF-diag は base_link で照合済** (URDF base ixy/ixz/iyz=0 ↔ EDN base ixy/ixz/iyz=0)。child link の OFF-diag は EDN child_inert に記載自体が無く ixx/iyy/izz のみ照合 (falsify-035 と同じ数値範囲) — この点は honest に注記。
  - **cat/fixtures 不変**: `git status --porcelain` は `?? sim-loop/` のみ → **tracked diff 空** (giemon src/ test/ fixtures/ は無変更。HEAD giemon **d0d3cb45fcc8…** 不変)。
- verdict: **survived** — parity 破れ 0 件、全 6 joint × 7 link の全数値 (base off-diag 含む) が 1e-12 内で一致。falsify-035 (parity 無破れ)・falsify-038 (damping 面 1 対 1) の結論は、陳腐化を排した independent parser で再確定。本 iteration は FK guard repair (未着手→未知のまま) とは別系で、赤「監査ツール陳腐化」を**動作する修正探査器で解消**(FALSE ではなく、oracle は健全)。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  python3 sim-loop/evidence/probe_parity_arm6_fixed.py   # -> mismatch 0, exit 0
  git rev-parse HEAD; git status --porcelain              # -> d0d3cb45fcc8..., `?? sim-loop/` のみ
  # mutation quality-check (本測は常に未改変実物で実行):
  #   実 EDN を一時コピーし j1 :effort 40->41 に変更 -> 同 parser は exit 1 / j1.effort 差を検出
  ```
- 検証内訳 (本 walk の 1 仮説・1 実測判定): 1 仮説 (H62) / 測定 1 (独立修正 probe による URDF↔EDN 全数値照合 + 空振り防止 mutation 検証 + git HEAD/status) / 判定 survived (parity 0 破れ)。
- コアへの 1 行: H62 survived — 陳腐化した slice-anchor 監査 (PARSE-ERR exit 1) を廃し、`:joint/axis [` 起点の独立修正 parser (probe_parity_arm6_fixed.py, mutation で差検出を検証済) で再監査した結果、全 6 joint × 7 link の全数値が 1e-12 内で一致、mismatches 0 / exit 0 — parity は健全、赤「監査ツール陳腐化」は解消 (本 bot は src 変更なし、probed のみ追加)。