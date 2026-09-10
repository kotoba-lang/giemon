# bench-104 (日次)

状態: **skipped (load)** — HOST LOAD 27.80/25.97/27.41 (1/5/15min, ncpu=10 ≈ 2.6-2.8×, 上昇傾向) + 実行バックエンド (terminal/read_file/search) 応答不能
(echo probe 空出力、pre-run が読めた status/maturity.md が read_file で File not found 化、即 pre-run 後に sandbox 応答不能)。

実行: 省略 — test スイート・seeded 再現・各 H の本測定いずれも実施せず (load 超過 + backend 応答不能により測定不能)。
基準値: bench-066 確定 (robotics 14/50/0, giemon 46/115/0) 据え置き。unmeasured のため回帰 assert せず(honest)。

再現 verdict: n/a (skipped, load) — 本測定なし。
回帰: なし (assert せず: unmeasured)。