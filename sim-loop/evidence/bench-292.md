# bench-292

## Judgement
- verdict: measured (silent-zero 持続) — runner 修復未了のため基準値確証は不能
- regression: 無断定 (silent-zero 経路は既知 test-runner 根因 / cljk rename、falsify-069 確定済み)

## Test run
- robotics `clojure -M:test`: 0 tests / 0 assertions / 0 failures, RC=0 → silent-zero (実測 37 連続、bench-244〜292)
- giemon `clojure -M:test`: 0 tests / 0 assertions / 0 failures, RC=0 → silent-zero (同上)
- 基準値 (据え置き): robotics 23/558/0 (ad99366)、giemon 46/115/0 (41ac173)

## HEADs (本走実測)
- robotics: ad99366bc7bef949e86ee33b7e04d12525dffe46 (不変)
- giemon: 41ac173f8e9dc599e8b9ab340a51f4135d5ade98 (不変)

## Load
- 開始: load averages 9.74 15.90 19.19, ncpu=10 (15-min ≈ 1.9× < 2× gate → 重い実験は省略せず clojure test 実行)
- 終了直後: 18.89 17.45 19.63

## Seeded reproduction
- not-applicable (sim-loop L0, 学習ジョブなし)

## Repro commands
```
bash /tmp/bench_run.sh   # cd robotics → clojure -M:test > /tmp/b_rob.txt; cd giemon → /tmp/b_gie.txt
```
測定出力: /tmp/b_rob.txt, /tmp/b_gie.txt

## Notes
- 負荷が gate 未満のため実行を試みたが、JVM runner は .cljk をロードできず silent-zero (falsify-069)。runner 修復 (test 拡張子復帰 / loader 登録) が全 bench/falsify の前提のまま。
- falsify-034 起 FK guard repair 未着手 (39 連続 refuted 記録)。本走はコード変更なし。
