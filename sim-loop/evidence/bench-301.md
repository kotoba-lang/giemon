# bench-301

日次 clojure -M:test ベンチ (giemon sim-loop)。

## 負荷ゲート

- uptime: load 12.37/11.38/12.04 (15-min 12.04)、hw.ncpu = 10
- 15-min ≈ 1.2x ncpu → gate 未満 (Load gate: 15min ≥ 2×ncpu=20 を超えない) → 実行判定。

## HEAD (実測時点)

- robotics: ad99366 (Merge kbb cutover adr-2609112000-kbb-cutover-clojure-cli-text) — 不変
- giemon: 41ac173 (Merge agent/repo-bot-landed: land sim-loop bench-244〜269 / falsify-069〜073) — 不変
- bench-299/300 と同一 HEAD、不変。

## clojure -M:test (実測)

- robotics: `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0
- giemon:   `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.` RC=0
- 判定: **silent-zero 持続**。bench-244〜301 のうち実測分で **43 連続**
  (bench-300 は load-skip 帯で clojure 経路未実施につき連続カウント据え置きの後、
  本走の実測で 41 (bench-298) → 42 (bench-299) → 本走 +1 = 43 連続)。
- runner 修復未了 (falsify-069 根因確定済み: JVM require が .cljk をロード不能)。

## seeded 再現

not-applicable (sim-loop は L0、学習ジョブ無し・L1 以降の seeded 再現は対象外)。

## 回帰判定

- 基準値 (robotics 23/558/0・giemon 46/115/0) は silent-zero のため測定不能 →
  **基準値据え置き、回帰 assert せず (honest / unmeasured-equivalent)**。
- 暫定測定経路 (kbb --backend sci --classpath src:test + 明示 require 4 ns → 21/52/0 緑、
  falsify-070/074/075/079 実績) は本走予算切れで未実施 — 変化は assert せず据え置き
  (giemon 暫定経路基準値 27/67/0 も据え置き)。
- kbb -M:test 第2経路 (RC=1 deps floor 未接続・falsify-074) も本走未再実施、据え置き。

## 再現コマンド

- `bash /tmp/run.sh` (cd robotics && clojure -M:test > /tmp/b_rob.txt 2>&1;
  cd giemon && clojure -M:test > /tmp/b_gie.txt 2>&1; /tmp/b_meta.txt に HEAD×2 + uptime)
- fixture: /tmp/b301_rob.txt /tmp/b301_gie.txt /tmp/b301_meta.txt /tmp/b301_all.txt

## falsify 状態

- falsify-034 起 FK guard repair 未着手 (40 連続 refuted・runner 修復後の再検証待ち) — 据え置き。
- falsify-069 (.cljk load 不能) / falsify-074 (kbb -M:test RC=1 deps floor 未接続) /
  falsify-081 (HEAD 41ac173 直読不変) 据え置き。
- 新規 falsify なし (H1〜H82 全決着・未決残存なし)。

## 判定

**judgement: measured (silent-zero 持続)** / 回帰: なし (測定不能に伴う assert なし) /
コード変更: なし。

## NEXT (変更なし・再発行)

test-runner 修復 — cljk rename 後の silent-zero (0/0/0 RC=0、bench-244〜301 実測分 43 連続) を
解消し robotics 23/558/0・giemon 46/115/0 の実測緑を現 HEAD で再確立。kbb -M:test 復活には
nbb.edn への deps floor (text/html/css/robotics/cognitect-labs/test-runner) 接続 (giemon は
nbb.edn 自体不在・robotics/nbb.edn 在の asymmetry 実測済)。検収条件に「意図的 fail 挿入で
RC=1」(falsify-079 実証) を含む。全ての bench/falsify の前提であり最優先修理。
