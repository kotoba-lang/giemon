# bench-328 (2026-09-27, cron giemon-sim-bench)

## judgement: measured (load 超過 notwithstanding — robotics test tree 前進による override)

- HOST LOAD: 開始時 16:13 `91.20 86.51 69.89` / ncpu 10 (15-min ≈ 9.1x)。終了時 16:15
  `99.70 90.13 73.55` (≈ 10x)。gate (≈2x) を大幅に超過したが、robotics が
  f5efd49 → a1af59c と src/test ツリーを大きく前進させた (process physics 一式、
  material/process/thermal/transport .cljk + process_test.cljk、deps.edn/nbb.edn)
  ため bench-327 同様の measured-reason override で全経路を実行した。
  実行は background bash + /tmp redirect で完走 (backend 応答正常)。

## HEADs (実測)

- robotics: a1af59c "Merge agent/robotics-fit-window" (f5efd49 から src/test 前進:
  8d7f0cc coll migration, 49d24d7 process physics, 241c256 quasi-static yield,
  3c943f2 slope/cooling, 21692e4 elastic-fit 等の merge)
- giemon: cd05afb "Merge repo-bot :landed — sim-loop evidence bench-327 + maturity.md"
  (fe217f0 から evidence-only 前進・src/test/deps.edn 不変)

## test 結果 (実測)

| suite | 経路 | 結果 | RC |
|---|---|---|---|
| robotics | clojure -M:test | 0 tests / 0 assertions / 0 failures (silent-zero 持続, bench-244〜328 実測分 56 連続・runner 修復未了 falsify-069) | 0 |
| robotics | kbb -M:test | **57 tests / 624 assertions / 0 failures, 0 errors** (新規: process 系 namespace 追加により 23/558/0 から前進 — 旧基準値からの回帰ではなく test ツリー前進による増加) | 0 |
| giemon | clojure -M:test | 0 tests / 0 assertions / 0 failures (silent-zero 持続, 同 56 連続) | 0 |
| giemon | kbb -M:test | **46 tests / 115 assertions / 0 failures, 0 errors — RC=1 が RC=0 に復活** (falsify-074 同値の「2 dep(s) not on classpath + clojure.java.io 未解決」警告ヘッダは出るが実行・緑完走。tools.namespace/tools.cli は runner substitution で迂回され test には不要になった状態) | 0 |

## seeded 再現 (同一コマンド 2 回実行)

- robotics kbb -M:test: pass1 57/624/0 RC=0 == pass2 57/624/0 RC=0 → **verdict: matched (決定的)**
- giemon kbb -M:test: pass1 46/115/0 RC=0 == pass2 46/115/0 RC=0 → **verdict: matched (決定的)**
- clojure -M:test 両 suite: pass1 のみ実施 (0/0/0 RC=0、seeded 再現の対象は kbb 経路)。

## 回帰

- なし。robotics kbb 23/558/0 → 57/624/0 は test ツリー前進 (f5efd49..a1af59c の
  process 系追加) による正の増加、failures/errors とも 0。giemon 46/115/0 で基準値一致。
- silent-zero (clojure -M:test 両 suite 0/0/0 RC=0) は bench-244〜328 で 56 連続持続
  (runner 修復未了・falsify-069 根因確定済み)。新規回帰ではない。
- giemon kbb RC=1 → RC=0 は **正の変化** (deps floor 接続効果と整合)。警告ヘッダ自体は残存。

## falsify 状態

- FK guard repair (falsify-034 起): giemon HEAD 今回 evidence-only 前進で src blob 不変 → 未着手のまま据え置き。
- governor rejected レコード化 + 負テスト: 同様に据え置き。
- sim-loop/status/probe.txt: 本回未確認 (giemon HEAD 詳査せず)。

## 再現コマンド

```
cd /Users/junkawasaki/github/kotoba-lang/robotics && kbb -M:test   # 57/624/0 RC=0
cd /Users/junkawasaki/github/kotoba-lang/giemon && kbb -M:test     # 46/115/0 RC=0
cd /Users/junkawasaki/github/kotoba-lang/robotics && clojure -M:test  # 0/0/0 RC=0 silent-zero
cd /Users/junkawasaki/github/kotoba-lang/giemon && clojure -M:test    # 0/0/0 RC=0 silent-zero
```

決定的記録・タイムスタンプなし。コード変更なし。
