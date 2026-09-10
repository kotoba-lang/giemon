# bench-131 — measured (load 過 gate 下で実測完走)

状態: HOST LOAD 15min ≈ 19.09 ( 05:54 実測) が ncpu=10 に対し ≈ 1.9× で Load gate ( 15min ≥ 2×ncpu =20) の下側。 bench-102～108 と同水準 ( ~1.5-3×) の負荷帯で実測完走可能と判断し、重い test スイートを実行・測定。

- uptime ( 05:54): 1min 17.97、5min 17.88、15min ≈ 19.13。実行後 ( 05:55): 18.22 / 17.84 / 19.01 — gate 超過なし ( 15min < 20,) で完走成功。



- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 ( bench-066 確定) と不変。code 変更なし ( giemon porcelain は `?? sim-loop/` 未追跡のみ、robotics status 空)。



- test スイート: **measured** — `clojure -M:test` 実測:
  - robotics: **14 tests /  ~~~~50 assertions /  ~~~~0 failures /  ~~~~0 errors**( RC=0)、基準値 14/50/0 と一致。
  - giemon: **46 tests /  ~~~~115 assertions /  ~~~~0 failures /  ~~~~0 errors**( RC=0)、基準値 46/115/0 と一致。両者 exit 0。



- seeded 再現 ( L1+:): 対象なし ( sim-loop は L0、学習ジョブ未実装)。not-applicable。




- 回帰 assert: **なし** ( measured) — テスト数・assertion 数・failures が基準値 ( robotics 14/50/0、giemon 46/115/0) とすべて一致、exit 0、HEAD 不変で回帰信号なし。新規 falsy なし ( H25～H41 全決着・未決残存なし、code 無変更で新仮説判定なし)。verdict: measured / no new regression signal

再現コマンド: `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test`、`cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M:test` ( 両者 exit 0)。seeded 再現は L0 で N/A。