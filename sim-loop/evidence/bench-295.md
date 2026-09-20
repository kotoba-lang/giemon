# bench-295

- date-context: 2026-09-19 JST 13:05 (cron, determinstic record)
- load gate: 15-min 17.14 / ncpu 10 = ~1.7x → gate 未満 (threshold ~2x), test suite 実行した
- HEAD: robotics ad99366 / giemon 41ac173 (いずれも前回 bench-294 から不変)

## test suite (clojure -M:test, /tmp redirect 経由)

- robotics: **Ran 0 tests containing 0 assertions. 0 failures, 0 errors. ROB_RC=0**
- giemon: **Ran 0 tests containing 0 assertions. 0 failures, 0 errors. GIE_RC=0**
- 両 suite とも silent-zero 持続。bench-244〜295 で **38 連続** (bench-290/291/293/294 は load skip で非実測)。runner 修復未了 — 根因は falsify-069 確定 (JVM require が .cljk をロード不能)。test 拡張子を戻すか loader 登録で clojure / kbb 両 runner 緑化が最優先修理。
- 基準値: robotics 23/558/0 (待ち、skill 側の bench-240 測定を正とする)、giemon 46/115/0。**本実行 0/0/0 は基準値と比較不能 (未測定相当)** — silent-zero は regression でも green でもなく「測れていない」状態。

## seeded reproduction

- sim-loop は L0 (学習ジョブ無し) → not-applicable。

## verdict

- judgement: **measured (両 suite 実行完走) だが silent-zero のため実測値は unmeasured 相当**
- regression: 不明 (基準値比較不能)。regression assert しない、honest。
- HEAD 変化: なし (ad99366 / 41ac173)
- falsify status: falsify-034 (FK guard repair) 未着手のまま残存 — runner 修復後の再検証。

## 再現コマンド

```
bash /tmp/b295_run.sh
# cd robotics && git rev-parse --short HEAD && clojure -M:test > /tmp/b295_rob_out.txt 2>&1; echo RC
# cd giemon   && git rev-parse --short HEAD && clojure -M:test > /tmp/b295_gie_out.txt 2>&1; echo RC
```

no code change.
