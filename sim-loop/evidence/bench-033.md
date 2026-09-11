# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-033
- ホスト負荷: load averages 41.83 (1min) / 36.52 (5min) / 37.04 (15min) 開始
  (ncpu=10 → **高負荷**)。テスト実行と軽量 seeded 再現は完了 (いずれも正常終了)。
  長時間シミュレータ実行・probe 再実行は **skipped (load)**。
  NEXT 項目 (sim 受付口の torque 照合不在の入力空間を広げる probe) は
  新規 probe の作成・実行 (測定コード追加) となるため本回も skipped (load)。

## 1. テスト実行 (kbb -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && kbb -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && kbb -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜032 と同一の軽量 seeded 再現のみ実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (src + test の .clj* への seed/learn/train grep で該当 0 件 —
  本回機械再確認、grep 該当ファイル数 0)。L1 昇格条件は未達、OPEN の赤は解消されず。
  L0 定着を継続。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture —
    fixtures/giemon_arm6/giemon_arm6.edn を unblob + reconstitute-arm で再構成、
    q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: 2 回の結果が**完全一致** → `SEED-PARITY true` (exit 0)、
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]
    bench-002〜032 の :xf/pos 数値と同一 (決定的再現を 31 点確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. 回帰の有無
- **回帰なし**。bench-001 → … → bench-033 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜033 は高負荷ホスト (load 5〜184) でも同一結果 — 負荷条件下での同一性を 31 点確認
  (本回 bench-033 は load 36.52 (5min)。bench-032 の 53.02、bench-030 の 45.80 より低いが
  依然高負荷水準)。
- evidence の差分: bench-031.md / bench-032.md が先行実行で追加済み。
  本回以降の追加は bench-033.md のみ。
  uncommitted は sim-loop/ ほか (diag.txt, simloop_files_list.txt) のまま。テスト結果には影響なし。

## 4. skipped (load) / 役割外
- 長時間シミュレータ実行・probe (falsify 系列) の再実行は **skipped (load)**
  (load 36.52 (5min) はテスト・軽量再現は可能だが重い実験は省略する水準)。
- NEXT の sim 受付口 torque 照合入力空間拡大 probe は新規測定コードの追加を伴うため
  本回も skipped (load)。次回低負荷時に実施する。
- caterpillar URDF 修正 (XML コメント内 `--`、line 9) は fixture コード修正を伴うため
  本 bot は実施しない (修正は実装側タスク。修正後に parity probe の再実行で検証可能)。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M -i /tmp/seed_parity_bench033.clj
# (arm_edn_test.clj の unblob + reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true, exit 0)
```

## 補足
- コード修正なし (ベンチ・記録のみ)。
- 決定的記述のみ、タイムスタンプ非依存。
- terminal ツールの stdout が空になる障害が継続しており、コマンド出力を
  一時ファイル (/tmp/giemon_test031.txt, /tmp/robotics_test031.txt, /tmp/seed_out033.txt) 経由で
  取得して検証した。テスト結果の数字はファイルから直接読み取ったものである。
- /tmp/seed_parity_bench032.clj (bench-030 由来) を /tmp/seed_parity_bench033.clj に複製して使用
  (内容は bench-002〜032 と同一 — unblob + reconstitute-arm + end-effector 2 回照合)。
