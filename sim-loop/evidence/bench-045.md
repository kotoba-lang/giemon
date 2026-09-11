# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-045
- ホスト負荷: 開始時 load averages 105.39 (1min) / 76.62 (5min)、
  実行終了時 82.42 / 84.11 / 73.39 (高負荷帯)。テスト実行、軽量 seeded 再現、
  NEXT (d) DR 初期姿勢 worst-case probe の seeded 再現を実施。
- 備考: terminal ツールの foreground stdout が空になる障害が継続しており、
  すべてのコマンド出力を一時ファイル経由で取得した (bench-039〜044 と同じ回避策)。

## 1. テスト実行 (kbb -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && kbb -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && kbb -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜044 と同一の軽量 seeded 再現を実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (status/maturity.md L0 記載どおり。本回も src/ + test/ への
  seed / learn / train grep 該当ファイル数 0 を機械再確認 — 該当 0 件)。
  L1 昇格条件は未達、L0 定着を継続。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture —
    fixtures/giemon_arm6/giemon_arm6.edn を unblob + reconstitute-arm で再構成、
    q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: **SEED-PARITY true** (exit 0)、
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]
    (:xf/rot [[0.921060994002885 0.0 0.3894183423086505] [0.0 1.0 0.0]
              [-0.3894183423086505 0.0 0.921060994002885]])
    bench-002〜044 の :xf/pos 数値と同一 (決定的再現を 43 点確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. NEXT (d) probe: DR 初期姿勢 worst-case × seeded 再現
- probe: `probe_dr_posture_family.py` (evidence 内の既存 probe、差し替えなし)。
  姿勢 3 種 (extended-phi0 / mid-phi45 / folded-phi90) × ramp/rest 6 組 =
  18 ケースの DR 初期姿勢 worst-case k ブレークポイント列挙を 2 回実行:
  - 結果: **WORST-RMS-BREAK: posture=extended-phi0 (ramp 0.02 / rest 0.2) k=2.21**
    (realistic DR k=1.2: not broken) — bench-044 時点の probe 出力と同一。
  - 決定性: 2 回実行 diff **0 行** (diff exit 0, IDENTICAL)。
- probe 実行自体はコード修正を伴わない測定のみ (L0 変化なし)。

## 4. 回帰の有無
- **回帰なし**。bench-001 → … → bench-045 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜045 は高負荷ホスト (load 5〜184) でも同一結果 — 負荷条件下での同一性を 43 点確認
  (本回 bench-045 は load 76.62 (5min) 開始・84.11 終了。bench-013 の 184.45 が過去最高)。
- evidence の差分: 本回は bench-045.md の追加のみ。uncommitted は sim-loop/ ほか
  (diag.txt, simloop_files_list.txt, statout.txt) のまま変化なし。テスト結果に影響なし。

## 5. skipped (load) / 役割外
- skipped (load) なし (テスト・軽量 seeded 再現・probe 再実行は完了)。
  ただし学習ジョブ自体が未実装 (L0) のため実施項目は軽量範囲のみ。
- コード修正なし (ベンチ・記録のみ)。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M -i /tmp/seed_parity_bench045.clj
# (arm_edn_test.clj の unblob + reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true, exit 0)
# NEXT (d) DR 初期姿勢 probe:
cd sim-loop/evidence
python3 probe_dr_posture_family.py > /tmp/probe_run1.log 2>&1
python3 probe_dr_posture_family.py > /tmp/probe_run2.log 2>&1
diff /tmp/probe_run1.log /tmp/probe_run2.log   # 0 行差 (決定的, IDENTICAL)
```

## 補足
- 決定的記述のみ、タイムスタンプ非依存。
- /tmp/seed_parity_bench044.clj を /tmp/seed_parity_bench045.clj に複製して使用
  (内容は bench-002〜044 と同一)。
