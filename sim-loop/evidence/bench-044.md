# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-044
- ホスト負荷: 開始時 load averages 18.67 (1min) / 13.19 (5min) (ncpu=10)、
  実行終了時 89.67 / 42.36 / 22.92 (高負荷帯)。テスト実行と軽量 seeded 再現、
  H16 probe (falsify-014 系) の再実行を実施。
- 備考: terminal ツールの foreground stdout が空になる障害が継続しており、
  すべてのコマンド出力を一時ファイル経由で取得した (bench-039〜043 と同じ回避策)。

## 1. テスト実行 (clojure -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && clojure -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && clojure -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜043 と同一の軽量 seeded 再現を実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (status/maturity.md L0 記載どおり。本回も src/ + test/ への
  seed / learn / train grep 該当 0 件を機械再確認 — grep exit 1 / 該当行数 0)。
  L1 昇格条件は未達、L0 定着を継続。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture —
    fixtures/giemon_arm6/giemon_arm6.edn を unblob + reconstitute-arm で再構成、
    q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: **SEED-PARITY true** (exit 0)、
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]
    (:xf/rot [[0.921060994002885 0.0 0.3894183423086505] [0.0 1.0 0.0]
              [-0.3894183423086505 0.0 0.921060994002885]])
    bench-002〜043 の :xf/pos 数値と同一 (決定的再現を 42 点確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. 回帰の有無
- **回帰なし**。bench-001 → … → bench-044 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜044 は高負荷ホスト (load 5〜184) でも同一結果 — 負荷条件下での同一性を 42 点確認
  (本回 bench-044 は load 13.19 (5min) 開始・42.36 終了。bench-013 の 184.45 が過去最高)。
- evidence の差分: 本回は bench-044.md の追加のみ。uncommitted は sim-loop/ ほか
  (diag.txt, simloop_files_list.txt, statout.txt) のまま変化なし。テスト結果に影響なし。

## 4. H16 probe 再実行 (falsify-014 系)
- probe: `probe_gate_input_space_widening.py` (bench-040〜043 と同一、差し替えなし)。
  gate 呼び出し経路 (`rob/gate`) で 14 ケース列挙、2 回実行:
  - A: 文字列化 torque / 5 層深入れ / vector 包み / as-keyword (5 ケース) —
    すべて :permit、clean baseline と同一、payload-carried true
  - B: 別名キー torque / Nm / effort / トップレベル (4 ケース) — すべて :permit
  - C: mission メタデータ (:metadata {:tau 1e6}) — mission 契約に保持されず
    (mission-differs: false)、同 mission-id action は :permit
  - D: バッチ 3 アクションの中央に極端 torque — 3 件すべて :permit、
    neighbors との差分なし (false)
  - E: safety-critical :emit にエッジ payload (str-1e6 / effort / numeric) —
    すべて :deny (安全側維持)
- 決定性: 2 回実行 diff **0 行** (EXIT ラベル行を除いて diff exit 0)、
  GATE-WIDENING-DETERMINISM-FAILS 0。
  bench-040〜043 の実測結果と同一 (verdict survived — H16 は未反証のまま残存)。

## 5. skipped (load) / 役割外
- skipped (load) なし (テスト・軽量 seeded 再現・probe 再実行は完了)。
  ただし学習ジョブ自体が未実装 (L0) のため実施項目は軽量範囲のみ。
- コード修正なし (ベンチ・記録のみ)。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && clojure -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M -i /tmp/seed_parity_bench044.clj
# (arm_edn_test.clj の unblob + reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true, exit 0)
# H16 probe:
python3 sim-loop/evidence/probe_gate_input_space_widening.py > /tmp/b44_h16.clj
clojure -M -e "$(cat /tmp/b44_h16.clj)" > /tmp/b44_h16_r1.txt 2>&1
clojure -M -e "$(cat /tmp/b44_h16.clj)" > /tmp/b44_h16_r2.txt 2>&1
diff /tmp/b44_h16_r1.txt /tmp/b44_h16_r2.txt   # EXIT ラベル行を除き 0 行差 (決定的)
```

## 補足
- 決定的記述のみ、タイムスタンプ非依存。
- /tmp/seed_parity_bench043.clj を /tmp/seed_parity_bench044.clj に複製して使用
  (内容は bench-002〜043 と同一)。
