# falsify-033 — H33 (FK guard 実行系 A/B 走行: silent zero-fill 緑 assertion との干渉有無)

- 連続番号: 033 (falsify-031 の H33 再試行 — 前回 verdict なし skip)
- 日次: 260908
- 仮説 (H33, NEXT 再掲): 次期 FK 角度 count/shape guard (H26 repair 候補) が、現行
  `test/kotoba/giemon/arm_test.cljc` 20–22 の silent zero-fill 緑 assertion
  (`(is (= (arm/forward-kinematics two-joint-arm [0.0 0.0])
           (arm/forward-kinematics two-joint-arm []))))`) と **干渉することなく**
  A/B 走行可能である (実行系観点)。
- 実測 (決定的、/tmp redirect + read_file、`clojure -M -i` で実バイト実行):
  - run A (現行 runtime, guard なし):
    - joint-count: 2
    - `(= (fk [0.0 0.0]) (fk []))`  ⇒ **true** (test 20-22 緑 — 空 angle は
      silent zero-fill、出力は shape-valid 3×3 (:xf/rot), :xf/pos [0.0 0.0 1.0] を生産)
  - run B (H26 angle-count guard を mock 差し込み — `count angles != joint-count` で throw):
    - `[0.0 0.0]` ⇒ **OK (2 == 2, no throw)**
    - `[]` ⇒ **THREW "FK angle-count guard: expected 2 angles, got 0"** (loud 化)
  - run C (test 20-22 の等式 assertion を guard 下で再走行):
    - `(= (guarded [0 0]) (guarded []))` ⇒ **THROWS** (test 20-22 は LOUD 化 = 緑 assertion と干渉)
  - run D (対照: output-shape-only guard — angle count 不照):
    - `[]` / `[0.0 0.0]` 両方 non-throw、等式 true のまま (干渉しないが missing-angle を検知不可)
  - 測定時 HOST LOAD: 21.04 / 21.99 / 24.51 (ncpu=10 の 2 倍超、但し軽量 1-clojure 実行は
    EXIT 0 で完遂 — falsify-032 と同じ /tmp workaround 経路)。
- verdict: **refuted** — 仮説 (「guard が silent zero-fill 緑 assertion と干渉することなく
  A/B 走行可能」) は不成立。H26 の FK angle-count guard を差し込むと `forward-kinematics`
  が空入力 `[]` で throw し、それに依存する test 20-22 の write が LOUD 化する — 修復
  は純追加ではなく、test 20-22 の期待値 (= missing-angle → silent zero-fill) か空入力契約の
  変更を必須とする。干渉を避ける shape-only 代替 (run D) は missing-angle 欠陥を一切検知
  せず実体 repair にならない — つまり「干渉なく追加できる FK guard」は実測上存在しない。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  clojure -M -i /tmp/probe_h33_fk_guard.clj > /tmp/h33_out.txt 2>&1   # 現行+guard を A/B
  # A: (= (fk [0 0]) (fk [])) → true / B: (guarded-fk [] ) → THREW / C: assertion THROWS
  # (probe は write_file で /tmp に置き、terminal の foreground stdout 空 障害を回避して
  #   `/tmp` redirect → read_file で実測回収; falsify-032 と同一手法)
  ```
- コアへの 1 行: H26 FK count guard の「孤立挿入」は test 20-22 (silent零fill) と必ず干渉し
  LOUD 化する — 2 択 (silent fill 温存 vs loud 化) の採択は guard 単体でなく test 期待値
  変更込みで決めろ。decode のみで実装・修正なし。