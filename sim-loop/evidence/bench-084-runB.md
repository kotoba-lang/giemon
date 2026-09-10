# bench-084 (run B — 並行 cron と bench-084 競合のため別名で記録)

- 日時: (なし — 決定的記録・タイムスタンプなし)
- Host load (pre-run 時点):1min 26.12 / 5min 23.78 / 15min 25.79 (ncpu=10、 uptime 26.12 23.78 25.79)
- 実行バックエンド: terminal 空出力 (date/uptime 空、exit 0) / search_files・stat 不能 (sandbox 応答不能)
- 判定:**skipped (load)** — test スイート・seeded 再現・falsify 本測定をすべて skipped。実行バックエンド (terminal/search) が応答不能 (ncpu=10 に対し load 26 前後) で非決定的環境のため測定不能。

##テスト数字
- テスト数:— (実行せず)
- assertion 数:— (実行せず)
- failures:— (実行せず)

##再現 verdict
- 再現:skipped (load / バックエンド応答不能)、再現性判定なし。



##回帰の有無
- 回帰:判定なし (測定不能)。

##再現コマンド
- (未実行。 load 超過 + terminal 空出力 exit 0 / sandbox stat 不能のため。