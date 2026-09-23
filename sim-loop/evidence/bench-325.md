# bench-325

- date-anchor: cron run, JST (no timestamp dependency; deterministic)
- HOST: main-2.local, user junkawasaki (terminal backend 実測 whoami/hostname — full checkout 側)
- HOST LOAD at gate check (measured, live, `uptime` order is 1/5/15-min): 15-min 35.95 (1-min 36.99, 5-min 37.57) / ncpu 10 → **≈3.6x** ≥ 2x gate
- 記録確定時 15-min 35.43 ≈3.5x (下降傾向だが gate 超過持続・pre-run script snapshot 15-min 36.05 ≈3.6x 同帯域)
- gate verdict: **load exceeded → heavy runs skipped (load)**
- terminal backend stdout swallow 再燃 (本走: `uptime`/`echo` 直接呼び出しが空出力 — bench-225/226/227/278/298/313 同症状・falsify-086 に文書化済みの既知 tool 挙動)。全 live 測定は scratch redirect + read_file で実施 (決定的取得)

## Tests
- robotics `clojure -M:test`: skipped (load) — unmeasured
- giemon `clojure -M:test`: skipped (load) — unmeasured
- kbb 暫定経路・seeded 再現: skipped (load) — unmeasured
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0, 暫定 kbb 27/67/0 (回帰 assert なし — runner が 0 tests を返す既知 defect の再確認は負荷収束後の次回)

## Git HEADs (measured, live rev-parse — file redirect 取得)
- robotics: ad99366bc7bef949e86ee33b7e04d12525dffe46 (git rev-parse 実測・不変・tree 59b12b8c2582308d71d9c0e0d2fb43a95feecf6e 実測 — bench-322〜324 と同一)
- giemon: 69878b970103e44ce11cef4ddc6208a5754a4fe0 (git rev-parse 実測・不変・tree 1fae9e4cde24cadf53202e3e6cfdb9805998ee89 実測 — bench-317〜324 / falsify-084/085 と同一)
- in-flight (未コミット, git status --porcelain 実測): giemon `M sim-loop/status/maturity.md` + `?? sim-loop/evidence/bench-316〜324.md` + `?? falsify-085.md / falsify-086.md / falsify-088.md` + `?? .hermes-tmp.Ytfzs4` (pre-run snapshot から bench-324.md / falsify-088.md が追加 — いずれも前走の着地済み新規 evidence、消失なし)。robotics は clean。src/test 不変 (tree hash 不変で裏付け)。

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job — seed / L1+ 学習ジョブ 0 件) — unmeasured (load-skip)

## Judgement
- unmeasured (load) — 基準値据え置き、回帰の assert なし
- regression: none observable (nothing ran; silent-zero runner issue persists unresolved per NEXT)
- runner status: clojure runner silent-zero 実測分 54 連続 (bench-244〜322) は本 run 未検証 (bench-290/291/293/294/307〜314・323/324 同型の load-skip)。test-runner 修復が最優先のまま変化なし。
- falsify 新規なし (H1〜H88 全決着・falsify-087 欠番・falsify-088 は前走で refuted・未決残存なし)
- NEXT は runner repair + re-baseline を HEAD 参照 69878b9 で再発行 (継続)

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min >= 2x ncpu -> skip (本 run は gate 時 ≈3.6x で全経路 skip)
cd orgs/kotoba-lang/robotics && clojure -M:test   # run when load < 2x ncpu
cd orgs/kotoba-lang/giemon && clojure -M:test     # run when load < 2x ncpu
git -C orgs/kotoba-lang/robotics rev-parse HEAD^{tree}   # 59b12b8 実測
git -C orgs/kotoba-lang/giemon rev-parse HEAD^{tree}     # 1fae9e4 実測
```

No code change.
