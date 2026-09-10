# falsify-032 — H34 (高負荷下 cross-run 再現性の破れ)

- 連続番号: 032
- 日次: 260907
- 仮説: giemon_arm6 fixture の `arm/end-effector` は、同一入力 q に対して独立 2 プロセス
  (cross-run) で bit 一致しない (高負荷で再現性が破れる、あるいは
  `fixtures/giemon_arm6/giemon_arm6.edn` の再構成が run 間に揺れる)。— すなわち
  `:xf/:pos` がプロセス間で乖離するという欠陥主張。
  これまでの bench は同一プロセス内 `(= r1 r2)` のみの照合で、cross-run (JVM 2 起動) の
  bit 一致は未検証だった面を攻める。
- 実測 (決定的、/tmp redirect + read_file 実測):
  - run A (`clojure -M -i /tmp/seed_parity_bench066.clj`, timeout 300, EXIT 0):
    ```
    SEED-PARITY true
    R1 #:xf{:rot [[0.921060994002885 0.0 0.3894183423086505] [0.0 1.0 0.0] [-0.3894183423086505 0.0 0.921060994002885]], :pos [0.035165560086391295 0.0 0.6104766433183229]}
    ```
  - run B (同一コマンド再実行, EXIT 0): 上と完全一致 (SEED-PARITY true /
    :rot 3x3 / :pos 同一)。
  - 測定時ホスト: `17:11 up 2 days, 9:54, 12 users, load averages 125.23 88.04 57.74`
    (ncpu 10 を大きく超過する極端負荷で実施)。
  - 基準一致: :xf/:pos [0.035165560086391295 0.0 0.6104766433183229] は bench-066 記録値
    と同一 (cross-run 2 点 + 履歴合わせ 3 点目一致、bench-066 の 62 点目から続けて一致)。
- verdict: **refuted (仮説不成立 — 再現性は生き残った)** — 欠陥 (cross-run 乖離) は
  検出されず。極端負荷 (1min load 125.23) 下でも独立 2 JVM が bit 一致し、
  determinism は破れなかった。本 falsify は仮説の実証に失敗 = コアの決定性主張は
  今回の攻撃面に対して survived。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  clojure -M -i /tmp/seed_parity_bench066.clj > /tmp/seed_X.txt 2>&1   # 2 回実行し
  # 各回の "R1" 行 (:rot / :pos) と SEED-PARITY true / EXIT 0 を照合 (run 間 bit 比較)
  ```
  (seed スクリプトは bench-066 由来、内容は bench-002〜063 と同一。
  terminal の foreground stdout が空になる障害があるため出力は /tmp に redirect して
  read_file で直接読取)
- コアへの 1 行: 決定性は極端負荷でも cross-run bit 一致を維持 (survived) —
  H26〜H32 の静的 repair 着手は別途、本 walk の追加実測は不要。
- 付記: コード修正なし (測定・記録のみ)。backend は /tmp redirect workaround で実測可能
  と判明したため、次回以降 falsify-031 (H33, FK guard A/B) も実行系観点で再試行可能。