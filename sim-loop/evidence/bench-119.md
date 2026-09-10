# bench-119 — giemon sim-loop bench (日次)

判定: **measured (完走)** — HOST LOAD が ncpu=10 の ~1.1× (15min ~10.98) で clojure -M:test 実測完走。robotics・giemon とも基準値一致、回帰なし。（実行後 uptime は 15.17/11.22/11.30 まで上昇したが完走後に計測。）

## 実行環境
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-066 確定) と不変。IN-FLIGHT は未追跡 sim-loop/・simloop_files_list.txt・statout.txt・tmp_probe_write.md のみ、コード変更なし。
- HOST LOAD: 実行開始時 (2:35) 9.70 / 10.20 / 10.98 (15min = ncpu=10 の約 1.1×) — 2× gate 未満で実測可。(NOT skipped)。
- 実行バックエンド: terminal 直接 stdout は空 (/tmp redirect workaround で echo 実測)。execute_code は cron mode で BLOCKED。

## テスト (clojure -M:test)
- **robotics**: `Ran 14 tests containing  ̄50 assertions. 0 failures, 0 errors.` RC=0 — 基準値 (14/50/0) と一致。

- **giemon**: `Ran 46 tests containing  ̄115 assertions.  ̄0 failures,  ̄0 errors.` RC=0 — 基準値 (46/115/0) と一致。
- 判定: **measured、回帰なし** (両 suite とも exit 0、基準値と数字一致、git diff 空)。(実行後 uptime 15.17/11.22/11.30 は完走後計測の参考値。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (再現対象の学習ジョブ 0 件、git diff 空)。seeded 再現は対象なし (bench-118 と同方針)。

##回帰
**なし (measured)** — robotics 14/50/0、giemon 46/115/0 を実測完走、exit 0、基準値 (bench-066 確定 / bench-118 最新) と両 suite とも一致。回帰なし。。

 git HEAD は不変 (コード変更なし)。IN-FLIGHT は未追跡のみ。

。

 git diff 空 (追跡変更なし)。

##反証 (falsify)
新規 falsify はなし。。 最新 falsify-039 (H40: 監査ツール probe_parity_arm6.py 陳腐化) は refuted 済 (現行 blob は PARSE-ERR -> exit 1 で陳腐化。falsify-037 が真因 slice anchor バグ を特定)。maturity.md の NEXT は none で新規 H の判定なし (code 無変更のため)。

##再現コマンド
- 実行: `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test > /tmp/b_rob.txt 2>&1`; `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M:test > /tmp/b_gie.txt 2>&1` —完走 (measured,回帰なし)。/tmp/b_rob.txt / /tmp/b_gie.txt に実測保存。頃 2:35。
- seeded 再現:対象なし (sim-loop L0、学習ジョブ未実装)。未実行。