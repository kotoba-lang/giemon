# falsify-035 — H36 (giemon_arm6 URDF↔EDN パリティに破れがあるか)

- 連続番号: 035 (falsify-034 の後続)
- 日次: 260907
- 仮説 (H36, 反証対象「URDF↔EDN パリティ」): `fixtures/giemon_arm6/` の
  `giemon_arm6.urdf` (parity oracle) と `giemon_arm6.edn` (:arm/chain 正本) の間で
  `from_edn(edn) == parse_urdf(urdf)` に破れがある — 幾何/limit/velocity/damping/
  inertial の少なくとも一要素が両者で不一致。
- 実測 (決定的、純計算。実行 backend の foreground stdout 応答不能のため
  `/tmp` redirect → read_file で回収、捏造なし):
  - 新規 Python パーサで両ファイルを独立に構文解析し、全数値要素を誤差 1e-12 で比較:
    - 6 revolute joint 各: `axis [3]`, `origin [3]`, `limit {lower, upper, effort,
      velocity}`, `damping` — EDN の `:joint/axis/:joint/origin/:joint/limit/
      :joint/damping` と対照。
    - 7 link (base_link + link1..6) 各: `mass`, `inertial {ixx, iyy, izz}` —
      EDN の `:arm/base` と各 `:child/link #:link{:inertial ...}` と対照。
  - 結果 (run): **joints=6 links=7 mismatches=0, exit 0** — 全 6 joint × 全 7 link の
    全数値要素が完全一致 (j1..j6 の axis z/y/y/z/y/z、origin z
    0.08/0.06/0.18/0.14/0.10/0.06、limit lower/upper/effort/velocity、damping
    0.06/0.08/0.06/0.04/0.03/0.02、link mass 2.0/0.6/0.5/0.35/0.22/0.16/0.12 と
    inertia ixx/iyy/izz も含め 1e-12 内一致)。
  - 付随発見 (sim-loop 監査ツール陳腐化 — パリティ破れではない): shipped
    `sim-loop/evidence/probe_parity_arm6.py` は現行 EDN blob に対し
    **PARSE-ERR (joint name 起点 slice で axis 取得不可) → exit 1 クラッシュ**。
    現行 blob の二重バックスラッシュ `\\"` エスケープに片側(`\"` のみ)しか畳んで
    おらず、対照を完走できない。新規パーサは `\\"` と `\"` の両レベルを畳んで
    全要素走破した。
  - 測定時 HOST LOAD: 24.99 / 30.17 / 29.50 (ncpu=10 の 2.5-3 倍)。軽量 python 1
    本の実行は EXIT 0 で完遂 (falsify-032/033 と同じ `/tmp` redirect workaround)。
- verdict: **refuted** — 仮説 (「URDF↔EDN パリティに破れがある」) は不成立。
  全 6 joint・全 7 link の幾何/limit/velocity/damping/inertial は URDF oracle と
  EDN 正本で完全一致、パリティは生き残り (破れなし)。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  python3 sim-loop/evidence/falsify-035_parity_probe.py > /tmp/o.txt 2>&1
  cat /tmp/o.txt   # → "joints=6 links=7 mismatches=0" exit 0
  # (terminal foreground stdout 空 障害を回避して /tmp redirect → read_file で回収)
  ```
- 検証内訳 (本 walk の 1 仮説・1 実測判定): 1 仮説 (H36) / 測定 1 (パリティ比較
  6 joint × 7 link 全数値要素) / 判定 refuted (仮説不成立 = パリティ生き残り)。
- コアへの 1 行: giemon_arm6 の URDF↔EDN パリティは無破れで生存 (6J/7L 全一致)
  — ただし sim-loop の旧 parity 監査 probe_parity_arm6.py が現行 blob で
  PARSE-ERR クラッシュする (監査ツール陳腐化) — 本 bot は実装・コード変更なし。