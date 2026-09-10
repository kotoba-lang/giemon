# bench-216 (日次)

状態: **skipped (load)** — HOST LOAD 84.05/89.30/73.79 (1/5/15min, ncpu=10 ≈ 7.4-8.9×, load gate 2× を大幅超過)。

実行: 省略 — test スイート・seeded 再現・各 H の本測定いずれも実施せず (load 超過により測定不能)。
基準値: bench-066 確定 (robotics 14/50/0, giemon 46/115/0) 据え置き。unmeasured のため回帰 assert せず (honest)。

再現 verdict: n/a (skipped, load) — 本測定なし。sim-loop は L0 で seeded job 対象外。
回帰: なし (assert せず: unmeasured)。

測定帯: giemon HEAD d0d3cb4 (基準一致), robotics HEAD 9459ca0 (基準一致) — HEAD は不変だが load 指すで test 未測定。
sim-loop/evidence は untracked (`??`)、probe /evidence 削除なし (参照 grep 実施せず、本 run は生成 probe なし)。