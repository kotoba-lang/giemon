# bench-297

日次 clojure -M:test ベンチ (giemon sim-loop)。

## 負荷ゲート
- uptime: load 12.25 / 12.66 / 16.73、hw.ncpu = 10
- 15-min ≈ 1.7x ncpu → ゲート未満、重いテスト実行を実施。

## HEAD (実測時点)
- robotics: ad99366bc7bef949e86ee33b7e04d12525dffe46 (不変)
- giemon: 41ac173f8e9dc599e8b9ab340a51f4135d5ade98 (不変)

## clojure -M:test (実測)
- robotics: Ran 0 tests / 0 assertions / 0 failures, RC=0
- giemon:   Ran 0 tests / 0 assertions / 0 failures, RC=0
- 判定: **silent-zero 持続**。robotics/giemon とも 0/0/0 RC=0。
- bench-244〜297 のうち実測分で **40 連続** silent-zero (runner 修復未了、
  falsify-069 根因確定: JVM require が .cljk をロード不能)。

## seeded 再現
- not-applicable (sim-loop は L0、学習ジョブ不在)。

## 回帰判定
- 基準値 (robotics 23/558/0 @ bench-240、giemon 46/115/0) と比較不能
  (0/0/0 は測定不能相当) → **基准値据え置き、回帰 assert せず honest**。

## 再現コマンド
- `bash /tmp/run_b297.sh` (cd robotics && clojure -M:test > /tmp/b297_rob.txt 2>&1; cd giemon && clojure -M:test > /tmp/b297_gie.txt 2>&1)
- 出力: /tmp/b297_rob.txt /tmp/b297_gie.txt /tmp/b297_meta.txt

## falsify 状態
- falsify-034 起 FK guard repair 未着手 (runner 修復後の再検証待ち)。
- 最優先: test-runner 修復 (拡張子を戻すか loader 登録で clojure / kbb 両 runner を緑化)。

## その他
- コード変更なし。
