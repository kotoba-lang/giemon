# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-040
- ホスト負荷: load averages 5.31 (1min) / 6.23 (5min) / 9.67 (15min) 開始
  (ncpu=10 → 低〜中負荷)。テスト実行・軽量 seeded 再現に加え、
  **NEXT (c) の入力空間拡大 probe (falsify-014 再試行) を本回実施**。
- 備考: terminal ツールの foreground stdout が空になる障害が継続しており、
  すべてのコマンド出力を一時ファイル経由で取得した (bench-039 と同じ回避策)。

## 1. テスト実行 (clojure -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && clojure -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && clojure -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜039 と同一の軽量 seeded 再現を実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (status/maturity.md L0 記載どおり。本回も src への
  seed/learn/train 系変更は確認されず)。L1 昇格条件は未達、L0 定着を継続。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture —
    fixtures/giemon_arm6/giemon_arm6.edn を unblob + reconstitute-arm で再構成、
    q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: 2 回の結果が**完全一致** → `SEED-PARITY true` (exit 0)、
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]
    (:xf/rot [[0.921060994002885 0.0 0.3894183423086505] [0.0 1.0 0.0]
              [-0.3894183423086505 0.0 0.921060994002885]])
    bench-002〜039 の :xf/pos 数値と同一 (決定的再現を 38 点確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. 回帰の有無
- **回帰なし**。bench-001 → … → bench-040 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜040 は高負荷ホスト (load 5〜184) でも同一結果 — 負荷条件下での同一性を 38 点確認
  (本回 bench-040 は load 6.23 (5min) の低負荷時。bench-013 の 184.45 が過去最高)。
- evidence の差分: 本回は probe_gate_input_space_widening.py の差し替え
  (ENV-BLOCKED プレースホルダ → 実測 probe)、bench-040.md / falsify-014.md / maturity の更新のみ。
  uncommitted は sim-loop/ ほか (diag.txt, simloop_files_list.txt) のまま。テスト結果に影響なし。

## 4. NEXT (c) probe 実施 — falsify-014 再試行 (H16)
- probe: `probe_gate_input_space_widening.py` (ENV-BLOCKED プレースホルダを実測 probe に差し替え)。
  falsify-013 と同一の gate 呼び出し経路 (`rob/gate` + `rob/action`) で
  4 系統の未測定入力空間を 14 ケース列挙:
  - A: 文字列化 torque ("120", "1e6") / 5 層深入れ tau 1e6 / vector 包み /
    quoted-map (5 ケース + clean baseline 照合) — すべて :permit、clean と同一、
    payload-carried true
  - B: 別名キー torque / Nm / effort / トップレベル torque (4 ケース) — すべて :permit
  - C: mission メタデータ経由 (:metadata {:tau 1e6}) — mission 契約に metadata は
    保持されず (mission-differs: false)、同 mission-id action は :permit
  - D: バッチ 3 アクションの中央に極端 torque — 3 件すべて :permit、
    clean 隣接ケースと decision 同一
  - E: safety-critical :emit に上記エッジ payload — すべて :deny (安全側維持)
- 決定性: 2 回実行 diff **0 行** (exit 0)、GATE-WIDENING-DETERMINISM-FAILS 0。
- 詳細は falsify-014.md を参照。

## 5. skipped (load) / 役割外
- skipped (load) なし (低負荷時につき全部門を実施)。
- caterpillar URDF 修正 (XML コメント内 `--`、line 9) は fixture コード修正を伴うため
  本 bot は実施しない (修正は実装側タスク。修正後に parity probe の再実行で検証可能)。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && clojure -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M -i /tmp/seed_parity_bench040.clj
# (arm_edn_test.clj の unblob + reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true, exit 0)
# H16 probe:
python3 sim-loop/evidence/probe_gate_input_space_widening.py > /tmp/h16.clj
clojure -M -e "$(cat /tmp/h16.clj)" > /tmp/h16.txt 2>&1
clojure -M -e "$(cat /tmp/h16.clj)" > /tmp/h16b.txt 2>&1
diff /tmp/h16.txt /tmp/h16b.txt   # 0 行差 (決定的)
```

## 補足
- コード修正なし (ベンチ・記録のみ。probe の差し替えは測定コード)。
- 決定的記述のみ、タイムスタンプ非依存。
- /tmp/seed_parity_bench039.clj を /tmp/seed_parity_bench040.clj に複製して使用
  (内容は bench-002〜039 と同一 — unblob + reconstitute-arm + end-effector 2 回照合)。
