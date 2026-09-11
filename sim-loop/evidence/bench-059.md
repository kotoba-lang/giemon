# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-059
- ホスト負荷: 高負荷継続だが bench-057/058 から低下傾向継続 (テスト中 load
  10.20 / 11.65 / 20.04、ncpu=10。15min 負荷は bench-057〜059 で 37→21→20 と漸減)。
  テスト実行と軽量 seeded 再現は正常終了 (exit 0)。
- 長時間シミュレータ実行・probe (falsify 系) 再実行は **skipped (load)**
  (15min load ≈20 = ncpu の約 2 倍が継続。テスト・軽量再現以外の重い実験は省略)。
- 備考: terminal ツールの foreground stdout が空になる障害が継続しているため、
  すべてのコマンド出力を一時ファイル (/tmp/*.txt) 経由で取得した
  (bench-039〜058 と同じ回避策)。

## 1. テスト実行 (kbb -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜058 と同一の軽量 seeded 再現のみ実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (成熟記録 sim-loop/status/maturity.md の「既存決定関数の
  2 回実行一致に限る」減点事由は解消されず)。本回も git log 直近 d0d3cb4 は
  bench-055〜058 と同一、src/test への seed/learn/train 系変更は確認されず
  (git status は未追跡の in-flight ファイル diag.txt / sim-loop/ /
  simloop_files_list.txt / statout.txt のみ)。L1 昇格条件は未達 → L0 据え置き。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture —
    fixtures/giemon_arm6/giemon_arm6.edn を unblob + reconstitute-arm で再構成、
    q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: 2 回の結果が**完全一致** → `SEED-PARITY true` (exit 0)、
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]
    (:xf/rot [[0.921060994002885 0.0 0.3894183423086505] [0.0 1.0 0.0]
              [-0.3894183423086505 0.0 0.921060994002885]])
    bench-002〜058 の :xf/pos 数値と同一 (決定的再現を 58 点確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. 回帰の有無
- **回帰なし**。bench-001 → … → bench-059 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜059 は高負荷ホスト (load 5〜184) でも同一結果 —
  負荷条件下での同一性を 57 点確認。本回 bench-059 はテスト中 load
  10.20〜10.27 / 5min 11.6 / 15min 19.9〜20.0 で同一性を維持。
- evidence の差分: 本回以降の追加は bench-059.md のみ (probe/falsify 再実行なし)。

## 4. skipped (load) / 役割外
- 長時間シミュレータ実行・probe (falsify 系列) の再実行は **skipped (load)**
  (ホスト 15min load ≈20 = ncpu 10 の約 2 倍の高負荷継続。テスト・軽量再現以外の
  重い実験は省略)。
- OPEN の赤 (URDF parse parity 自動検証不在、gate↔arm torque 照合未接続、
  H19/H20/H21 潜在修理点、NEXT H23 velocity 欠落面 probe) はいずれも測定コード
  追加または fixture/コア修正を伴い、本 bot はコードを修正しないため本回も
  skipped (load)。実装側タスクとして継続。
- caterpillar URDF 修正 (XML コメント内 `--`、line 9) は fixture コード修正を伴うため
  本 bot は実施しない (修正は実装側タスク。修正後に parity probe の再実行で検証可能)。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M -i /tmp/seed_parity_bench059.clj
# (arm_edn_test.clj の unblob + reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true, exit 0)
```

## 補足
- コード修正なし (ベンチ・記録のみ)。
- 決定的記述のみ、タイムスタンプ非依存。
- terminal ツールの stdout が空になる障害が継続しており、コマンド出力を
  一時ファイル (/tmp/giemon_test_b059.txt, /tmp/robotics_test_b059.txt,
  /tmp/seed_b059.txt) 経由で取得して検証した。テスト結果の数字は
  ファイルから直接読み取ったものである。
- /tmp/seed_parity_bench058.clj (bench-058 由来) を /tmp/seed_parity_bench059.clj に
  複製して使用 (内容は bench-002〜058 と同一 — unblob + reconstitute-arm +
  end-effector 2 回照合)。