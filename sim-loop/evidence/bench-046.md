# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-046
- ホスト負荷: 開始時 load averages 33.44 / 38.28 / 49.99、テスト・再現実行時は
  最大 89.41 (1min) / 57.00 (5min) (高負荷帯)。テスト実行、軽量 seeded 再現、
  NEXT (d) DR 初期姿勢 worst-case probe の seeded 再現を実施。
- 備考: terminal ツールの foreground stdout が空になる障害が継続しており、
  すべてのコマンド出力を一時ファイル経由で取得した (bench-039〜045 と同じ回避策)。

## 1. テスト実行 (kbb -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && kbb -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && kbb -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜045 と同一の軽量 seeded 再現を実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (status/maturity.md L0 記載どおり。本回も src/ + test/ への
  seed / learn / train grep 該当ファイル数 0 を機械再確認 — 該当 0 件)。
  L1 昇格条件は未達、L0 定着を継続。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (fixtures/giemon_arm6/giemon_arm6.edn
    を unblob + reconstitute-arm で再構成) — falsify-016 で拡張した
    probe_seed_parity_postures.clj により 4 姿勢で照合:
  - 結果: **SEED-PARITY true × 4 姿勢 / POSTURES-MEASURED 4 (exit 0)**、
    DETERMINISM-FAIL すべて false。
    - extended-q0 → POS [0.48 0.0 0.14]
    - mid-q0      → POS [0.39213203435596433 0.0 0.35213203435596424]
    - folded-q0   → POS [0.18 0.0 0.44]
    - bench-q0    → POS [0.035165560086391295 0.0 0.6104766433183229]
      (bench-002〜045 の従来単点と同一数値 — 回帰なし)
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. NEXT (d) probe: DR 初期姿勢 worst-case × seeded 再現
- probe: `probe_dr_posture_family.py` (evidence 内の既存 probe、差し替えなし)。
  姿勢 3 種 (extended-phi0 / mid-phi45 / folded-phi90) × ramp/rest 6 組 =
  18 ケースの DR 初期姿勢 worst-case k ブレークポイント列挙を 2 回実行:
  - 結果: **WORST-RMS-BREAK: posture=extended-phi0 (ramp 0.02 / rest 0.2) k=2.21**
    (realistic DR k=1.2: not broken、最大 RMS 21.9 / peak 29.1 N·m) —
    bench-045 / falsify-016 の probe 出力と同一。
  - 決定性: 2 回実行 diff **0 行** (diff exit 0, IDENTICAL)。
- probe 実行自体はコード修正を伴わない測定のみ (L0 変化なし)。

## 4. 回帰の有無
- **回帰なし**。bench-001 → … → bench-046 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜046 は高負荷ホスト (load 5〜184) でも同一結果 — 負荷条件下での同一性を 44 点確認
  (本回 bench-046 は load 38.28 (5min) 開始・57.00 終了。bench-013 の 184.45 が過去最高)。
- evidence の差分: 本回は bench-046.md の追加のみ。uncommitted は sim-loop/ ほか
  (diag.txt, simloop_files_list.txt, statout.txt) のまま変化なし。テスト結果に影響なし。

## 5. skipped (load) / 役割外
- skipped (load) なし (テスト・軽量 seeded 再現・probe 再実行は完了)。
  ただし学習ジョブ自体が未実装 (L0) のため実施項目は軽量範囲のみ。
- コード修正なし (ベンチ・記録のみ)。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
# Ran 14 tests containing 50 assertions. 0 failures, 0 errors.
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M:test
# Ran 46 tests containing 115 assertions. 0 failures, 0 errors.
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && \
  kbb -M -i sim-loop/evidence/probe_seed_parity_postures.clj
# SEED-PARITY true x4 / POSTURES-MEASURED 4 (exit 0)
python3 sim-loop/evidence/probe_dr_posture_family.py   # 2 回実行し diff 0 行を確認
# WORST-RMS-BREAK: posture=('extended-phi0', 0.02, 0.2) k=2.21 (k=1.2: not broken)
```
