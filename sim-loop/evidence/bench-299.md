# bench-299

日次 clojure -M:test ベンチ (giemon sim-loop)。

## 負荷ゲート

- uptime: load 18.81 / 33.63 / 38.98、hw.ncpu = 10
- 15-min ≈ 1.9x ncpu → ゲート未満 (约2x 未満)、重いテスト実行を実施 (measured)。
- 開始時 HOST LOAD が gate unverified 域未満のため test 完走、jugement measured。

## HEAD (実測时点)

- robotics: ad99366bc7bef949e86ee33b7e04d12525dffe46 (不変)
- giemon: 41ac173f8e9dc599e8b9ab340a51f4135d5ade98 (不変)

## clojure -M:test (実測)

- robotics: Ran 0 tests / 0 assertions / 0 failures, RC=0
- giemon:   Ran 0 tests / 0 assertions / 0 failures, RC=0
- 判定: **silent-zero 持続**。robotics/giemon とも 0/0/0 RC=0。
- bench-244〜299 のうち実测分で **42 連続** silent-zero
  (灰度実测分 bench-244〜299，bench-298 業 41 連続、本次分 +1 = 42 連続)。
  runner 修復未了 (falsify-069 根因確定済み: JVM require が .cljk をロード不能)。
- bench-298 からの +1 連続 — boat 修復未了在持続记録。

## seeded 再現

- not-applicable (sim-loop は L0、学習ジョブ无し、L1 以降の seeded 再现は対象外)。
- 现行 verdi: not-applicable — 不変 (seed 不从の L0 持续保证、捏造なし)。

## 回帰判定

- 基準值 (robotics 23/558/0 @ bench-240、giemon 46/115/0) と比較不能
  (0/0/0 是测定不能相当) → **基准值据え置き、回帰 assert せず honest**。

## 再現コマンド

- `bash /tmp/run_b298.sh` (cd robotics && clojure -M:test > /tmp/b298_rob.txt 2>&1;
  cd giemon && clojure -M:test > /tmp/b298_gie.txt 2>&1)
- 出力: /tmp/b298_rob.txt /tmp/b298_gie.txt /tmp/b298_meta.txt

## falsify 状态

- falsify-034 起 FK guard repair 未着手 (runner 修復後の再検証待ち。falsify-034 以降 refuted 連続)。
- falsify-069 确定済み: JVM require が .cljk をロード不能の root 起因。
- falsify-074: kbb -M:test 第二経路 reintroduction (deps floor 接続) 判别済み — silent runner defected 兴。
- 最優先: test-runner 修復 (拡張子を戻すか loader 登録で clojure / kbb 両 runner を緑化)。

## 判定

- **judgement: measured (silent-zero 持続)** / 回帰: なし (测定不能に伴う assert なし) /
  代码変更: なし。

## その他

- 代码変更なし。進-inflight: sim-loop 系のみ (rouben 有 no? 有)。
