# bench-218 (日次)

状態: **skipped (load)** — HOST LOAD 82.55/106.47/109.01 (1/5/15min, ncpu=10 ≈ 8-11×, load gate 2× を大幅超過)。

実行: 省略 — test スイート・seeded 再現・各 H の本測定いずれも実施せず (load 超過により測定不能)。
基準値: bench-066 確定 (robotics 14/50/0, giemon 46/115/0) 据え置き。unmeasured のため回帰 assert せず (honest)。

再現 verdict: n/a (skipped, load) — 本測定なし。sim-loop は L0 で seeded job 対象外。
回帰: なし (assert せず: unmeasured)。

giemon HEAD d0d3cb4 (基準一致)。
robotics HEAD 396fc33 (基準 9459ca0 と DIFF — bench-217 と同一 HEAD、移動は bench-217 前から継続。load 超過で test 未測定のため回帰判定せず、実測検証は負荷収束後の次回に必要)。
sim-loop/evidence は untracked (`??`)、probe 削除なし (本 run は probe 生成なし)。

再現コマンド (負荷収束後):
  cd orgs/kotoba-lang/robotics && kbb -M:test
  cd orgs/kotoba-lang/giemon   && kbb -M:test
