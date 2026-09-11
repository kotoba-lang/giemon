# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-042
- ホスト負荷: load averages 25.13 (1min) / 15.74 (5min) / 15.91 (15min) 開始
  (ncpu=10 → 5min 換算では中〜高め)。テスト実行と軽量 seeded 再現、
  H16 probe (falsify-014 系) の再実行を実施。
- 備考: terminal ツールの foreground stdout が空になる障害が継続しており、
  すべてのコマンド出力を一時ファイル経由で取得した (bench-039〜041 と同じ回避策)。

## 1. テスト実行 (kbb -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && kbb -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && kbb -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜041 と同一の軽量 seeded 再現を実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (status/maturity.md L0 記載どおり。本回も src への
  seed/learn/train grep 該当行数 0 を再確認)。L1 昇格条件は未達、L0 定着を継続。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture —
    fixtures/giemon_arm6/giemon_arm6.edn を unblob + reconstitute-arm で再構成、
    q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: 2 回の結果が**完全一致** → `SEED-PARITY true` (exit 0)、
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]
    (:xf/rot [[0.921060994002885 0.0 0.3894183423086505] [0.0 1.0 0.0]
              [-0.3894183423086505 0.0 0.921060994002885]])
    bench-002〜041 の :xf/pos 数値と同一 (決定的再現を 40 点確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. 回帰の有無
- **回帰なし**。bench-001 → … → bench-042 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜042 は高負荷ホスト (load 5〜184) でも同一結果 — 負荷条件下での同一性を 40 点確認
  (本回 bench-042 は load 15.74 (5min) 開始。bench-013 の 184.45 が過去最高)。
- evidence の差分: 本回は bench-042.md の追加のみ。uncommitted は sim-loop/ ほか
  (diag.txt, simloop_files_list.txt) のまま変化なし。テスト結果に影響なし。

## 4. H16 probe 再実行 (falsify-014 系)
- probe: `probe_gate_input_space_widening.py` (bench-040/041 と同一、差し替えなし)。
  gate 呼び出し経路 (`rob/gate` + `rob/action`) で 14 ケース列挙:
  - A: 文字列化 torque / 5 層深入れ / vector 包み / quoted-map (5 ケース) —
    すべて :permit、clean baseline と同一、payload-carried true
  - B: 別名キー torque / Nm / effort / トップレベル (4 ケース) — すべて :permit
  - C: mission メタデータ (:metadata {:tau 1e6}) — mission 契約に保持されず
    (mission-differs: false)、同 mission-id action は :permit
  - D: バッチ 3 アクションの中央に極端 torque — 3 件すべて :permit
  - E: safety-critical :emit にエッジ payload — すべて :deny (安全側維持)
- 決定性: 2 回実行 diff **0 行** (EXIT 0/0、差分行は付与した EXIT ラベル行のみ)、
  GATE-WIDENING-DETERMINISM-FAILS 0。
  bench-040/041 の実測結果と同一 (verdict survived — H16 は未反証のまま残存)。

## 5. skipped (load) / 役割外
- skipped (load) なし (テスト・軽量 seeded 再現・probe 再実行は完了)。
  ただし学習ジョブ自体が未実装 (L0) のため実施項目は軽量範囲のみ。
- コード修正なし (ベンチ・記録のみ)。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M -i /tmp/seed_parity_bench042.clj
# (arm_edn_test.clj の unblob + reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true, exit 0)
# H16 probe:
python3 sim-loop/evidence/probe_gate_input_space_widening.py > /tmp/h16.clj
kbb -M -e "$(cat /tmp/h16.clj)" > /tmp/h16r1.txt 2>&1
kbb -M -e "$(cat /tmp/h16.clj)" > /tmp/h16r2.txt 2>&1
diff /tmp/h16r1.txt /tmp/h16r2.txt   # 0 行差 (決定的)
```

## 補足
- 決定的記述のみ、タイムスタンプ非依存。
- /tmp/seed_parity_bench041.clj を /tmp/seed_parity_bench042.clj に複製して使用
  (内容は bench-002〜041 と同一)。
