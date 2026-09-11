# bench-132 — 実測完走 (measured)

状態: HOST LOAD 15min ~19.78→19.41 が ncpu=10 の ~2.0× を僅かに下回る負荷帯で test スイート実測完走。

- uptime (6:04 実測):  15min ≈ 19.78 ( ncpu=10 に対し 約 2.0×,  bench-129 の ~1.9× と同水準)。1min 18.24, 5min 20.17 直後の実測で完走 ( bead 判定)。完走時刻も 15min ≈19.41 — Load gate (15min ≥ 2×ncpu=20) 未満帯で計測可能。

- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 ( bench-066 確定) と不変。



- git status: giemon porcelain = 1 未追跡のみ: sim-loop/ ( tracked 変更なし)。robotics status 空 — コード変更なし。





- test スイート実測完走 ( `kbb -M:test` ):
  - **robotics**: Ran 14 tests、50 assertions、0 failures、0 errors、exit RC=0 — 基準値 14/50/0 と完全一致;
  - **giemon**: Ran 46 tests、115 assertions、0 failures、0 errors、exit RC=0 — 基準値 46/115/0 と完全一致;

- seeded 再現 ( L1+):  対象なし ( sim-loop は L0、学習ジョブ未実装)。not-applicable;



- 回帰 assert: **なし** ( measured) — 基準値 ( bench-066 確定 / bench-129 最新実測) と完全一致、回帰なし。新規 falsy なし ( H25～H41 全決着・未決残存なし、code 無変更で新仮説判定なし)。verdict: measured / no regression

再現コマンド: `kbb -M:test` ( robotics + giemon) — 両者 exit RC=0 で完走。seeded 再現は L0 で N/A。