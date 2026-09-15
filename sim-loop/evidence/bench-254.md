# bench-254

## Judgement: measured (silent-zero 継続 — 既知の test-runner 不具合)

- robotics `kbb -M:test`: Ran 0 tests containing 0 assertions. 0 failures, 0 errors. RC=0 (0/0/0)
- giemon `kbb -M:test`: Ran 0 tests containing 0 assertions. 0 failures, 0 errors. RC=0 (0/0/0)
- 基準値 robotics 23/558/0・giemon 46/115/0 に対し両プロジェクトとも 0/0/0。
  maturity.md NEXT 記載の「cljk rename 後の silent-zero (RC=0 のまま 0/0/0)」と
  完全に同じ症状であり、本 bench の主要な既知状態を確認した。新規回帰ではないが
  実測緑は現れていない。test-runner 修復が最優先 (falsify-070 の第2測定経路
  kbb --classpath + 明示 require では 21/52/0 緑、参照)。

## Seeded reproduction
- not-applicable (sim-loop は L0、学習ジョブ無し)。silent-zero は決定的に再現
  (同一スクリプト /tmp/gbench.sh、両プロジェクトで同一の 0/0/0 出力)。

## Regression
- test 数 / assertion 数の回帰: 判定不能 (0/0/0 のため)。failures/errors は 0 で
  RC=0。0/0/0 自体は bench 群で既知・記録済みの状態。新規悪化なし。

## Environment (決定的・タイムスタンプ無し)
- robotics HEAD: ad99366bc7bef949e86ee33b7e04d12525dffe46
- giemon HEAD: 00fd23f9d04743323047c8c29c30aa18320daa70
- load: up 9 days, load averages 16.52 16.13 15.89 (ncpu=10、15分帯 >2x だが
  テスト自体は即時完了したため実行済み; 重い実験は本 bench の範囲外)
- 再現コマンド:
  `cd orgs/kotoba-lang/robotics && kbb -M:test` → 0/0/0 RC=0
  `cd orgs/kotoba-lang/giemon && kbb -M:test` → 0/0/0 RC=0

## Falsify status
- falsify-034 (H35 FK guard repair 未実装) 残存、変化なし。
- falsify-070: kbb 経路 21/52/0 緑。46/115 完全回復には deps floor 接続 +
  host interop (`catch Exception`) 修正が別途必要 (変化なし)。

No code change.
