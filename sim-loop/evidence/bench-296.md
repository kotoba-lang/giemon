# bench-296

- run: cron bench iteration (bench-295 の次 / evidence 連番 296)
- load gate: 15-min 17.44 / ncpu 10 ≈ 1.7x → gate 未満、実行。
- git HEAD: robotics ad99366 / giemon 41ac173 (bench-295 と不変)
- measured / unmeasured: **measured** (両 suite 実測)

## test 実行結果 (clojure -M:test)

| suite | tests | assertions | failures/errors | RC |
|---|---|---|---|---|
| robotics | 0 | 0 | 0 | 0 |
| giemon | 0 | 0 | 0 | 0 |

- silent-zero 持続: bench-244〜296 の実測分で **39 連続** (0/0/0 RC=0)。runner 修復未了。
- 根因確定済: falsify-069 — JVM require が .cljk をロード不能 (cljk rename)。loader 登録か拡張子復帰で解消の必要あり。負帰属なし・falsify-074 実証の RC=1 probe は暫定 kbb 経路で別途実績あり。

## seeded 再現

- not-applicable: sim-loop は L0 (seeded 学習ジョブなし)。

## 回帰判定

- 基準値 (robotics 23/558/0, giemon 46/115/0) 据え置き。silent-zero は測定不能であり、基準値との比較は不成立 → 回帰の有無は判定不能 (honest: regression unknown, runner 修復待ち)。
- HEAD 不変 → コード差分による回帰の可能性なし。

## NEXT 引継ぎ

- NEXT: test-runner 修復 (.cljk loader) — 全 bench/falsify の前提・最優先。詳細は status/maturity.md NEXT 欄 (falsify-069/070/074/075/079 参照)。

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon  && clojure -M:test
```

- コード変更: なし。
