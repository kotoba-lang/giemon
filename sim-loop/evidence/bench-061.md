# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-061。
- ホスト負荷: 中負荷 (16:07 で load 9.43 / 5min 7.92 / 15min 9.20、ncpu=10)。
  bench-059 高負荷 (15min ≈20) → bench-060 中負荷へ漸減 (15min ≈12) → 本回も中負荷
  (15min ≈9.2 に漸減継続)。テスト実行と軽量 seeded 再現は正常終了 (exit 0)。
- 長時間シミュレータ実行・probe (falsify 系) 隔線再実行は **役割外 / 省略**
  (コード・測定の追加を伴う実装側タスクのため本 bot は実施しない。
  bench-059/060 と同じ扱い)。
- 備考: terminal ツールの foreground stdout が空になる障害が継続しているため、
  すべてのコマンド出力を一時ファイル (/tmp/*.txt) 経由で取得した
  (bench-039〜060 と同じ回避策)。

## 1. テスト実行 (clojure -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)
- 根拠: /tmp/robotics_test_b061.txt から直接読み取り。

### orgs/kotoba-lang/giemon
- コマンド: `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)
- 根拠: /tmp/giemon_test_b061.txt から直接読み取り。

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜060 と同一の軽量 seeded 再現のみ実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (成熟記録 sim-loop/status/maturity.md の「既存決定関数の
  2 回実行一致に限る」減点事由は解消されず)。本回も git log 直近 d0d3cb4 は
  bench-055〜060 と同一、git grep で src/**/*.clj* と test/**/*.clj* の
  seed/learn/train 該当は 0 件、git status は未追跡の in-flight ファイル
  (diag.txt / sim-loop/ / simloop_files_list.txt / statout.txt) のみ。
  L1 昇格条件は未達 → L0 据え置き。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture —
    fixtures/giemon_arm6/giemon_arm6.edn を unblob + reconstitute-arm で再構成、
    q=[0.0 0.2 -0.3 0.0 0.5 0.0])。
  - コマンド: `clojure -M -i /tmp/seed_parity_bench061.clj`
    (bench-060 の seed スクリプトを複製、内容は bench-002〜060 と同一)。
  - 結果: **SEED-PARITY true** (exit 0)。
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]、:xf/rot も同一。
    bench-002〜060 の :xf/pos 数値と同一 (決定的再現を 60 点確認)。
  - 根拠: /tmp/seed_b061.txt から直接読み取り。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. 回帰の有無
- **回帰なし**。bench-001 → … → bench-061 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜061 は高負荷ホスト (load 5〜184) でも同一結果 —
  負荷条件下での同一性を 59 点確認。本回 bench-061 はテスト時 load
  9.43 / 5min 7.92 / 15min 9.20 で同一性を維持。
- evidence の差分: 本回以降の追加は bench-061.md のみ (probe/falsify 再実行なし)。

## 4. 役割外 / 省略
- 長時間シミュレータ実行・probe (falsify 系列) の再実行は **省略**
  (コード・測定追加を伴う実装側タスク。bench-059/060 と同じ扱い。
  現負荷 15min ≈9.2 は ncpu 10 を下回る水準で、テスト・軽量再現は正常完了)。
- OPEN の赤 (URDF parse parity 自動検証不在、gate↔arm torque 照合未接続、
  H19/H20/H21 潜在修理点、NEXT H23 velocity 欠落面 probe) はいずれも測定コード
  追加または fixture/コア修正を伴い、本 bot はコードを修正しないため本回も省略。
  実装側タスクとして継続。
- caterpillar URDF 修正 (XML コメント内 `--`、line 9) は fixture コード修正を伴うため
  本 bot は実施しない (修正は実装側タスク。修正後に parity probe の再実行で検証可能)。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && clojure -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M -i /tmp/seed_parity_bench061.clj
# (arm_edn_test.clj の unblob + reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true, exit 0)
```

## 補足
- コード修正なし (ベンチ・記録のみ)。
- 決定的記述のみ、タイムスタンプ非依存。
- terminal ツールの stdout が空になる障害が継続しており、コマンド出力を
  一時ファイル (/tmp/giemon_test_b061.txt, /tmp/robotics_test_b061.txt,
  /tmp/seed_b061.txt) 経由で取得して検証した。テスト結果の数字は
  ファイルから直接読み取ったものである。
- /tmp/seed_parity_bench060.clj (bench-060 由来) を /tmp/seed_parity_bench061.clj に
  複製して使用 (内容は bench-002〜060 と同一 — unblob + reconstitute-arm +
  end-effector 2 回照合)。