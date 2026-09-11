# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-023
- ホスト負荷: load averages 115.03 (1min) / 99.45 (5min) / 81.18 (15min) 開始
  (ncpu=10 → **極度高負荷**。bench-013 の過去最高 184.45 には及ばないが高水準)。
  テスト実行と軽量 seeded 再現は完了 (いずれも正常終了)。
  長時間シミュレータ実行・probe 再実行は **skipped (load)**。
  NEXT 項目 (giemon_caterpillar_facade.urdf の XML コメント内 `--` 修正) は
  fixture 編集 (コード修正) を伴うため本 bot の役割外として未実施。

## 1. テスト実行 (kbb -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && kbb -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && kbb -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜022 と同一の軽量 seeded 再現のみ実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (src + test の .clj* への seed/learn/train grep で該当 0 件 —
  本回機械再確認、grep 出力 COUNT= 0)。L1 昇格条件は未達、OPEN の赤は解消されず。
  L0 定着を継続。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture —
    fixtures/giemon_arm6/giemon_arm6.edn を unblob + reconstitute-arm で再構成、
    q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: 2 回の結果が**完全一致** → `SEED-PARITY true` (exit 0)、
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]
    bench-002〜022 の :xf/pos 数値と同一 (決定的再現を 21 点確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. 回帰の有無
- **回帰なし**。bench-001 → … → bench-023 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜023 は高負荷ホスト (load 5〜184) でも同一結果 — 負荷条件下での同一性を 21 点追加確認
  (本回 bench-023 は load 99.45 (5min)。bench-013 の 184.45 に次ぐ高水準でも同一結果)。
- evidence の差分: 前回 (bench-022) 以降、evidence ファイルの追加・変更なし。
  uncommitted は sim-loop/ ほか (diag.txt, simloop_files_list.txt) のまま。テスト結果には影響なし。

## 4. skipped (load) / 役割外
- 長時間シミュレータ実行・probe (falsify 系列) の再実行は **skipped (load)**
  (load 99.45 (5min) は重い実験を省略する水準)。
- NEXT の caterpillar URDF 修正 (XML コメント内 `--`、line 9) は fixture コード修正を伴うため
  本 bot は実施しない (修正は実装側タスク。修正後に parity probe の再実行で検証可能)。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M -i /tmp/seed_parity_bench023.clj
# (arm_edn_test.clj の unblob + reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true, exit 0)
```

## 補足
- コード修正なし (ベンチ・記録のみ)。
