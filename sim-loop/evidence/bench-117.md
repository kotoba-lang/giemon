# bench-117 — giemon sim-loop bench (日次)

判定: **measured (完走)** — HOST LOAD が ncpu=10 の ~1.5× (15min 14.96) で kbb -M:test 実測完走。robotics・giemon とも基準値一致、回帰なし。



## 実行環境
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-114) と不変。git diff 両方とも空 (追跡変更なし)。IN-FLIGHT は未追跡 sim-loop/・simloop_files_list.txt・statout.txt・tmp_probe_write.md のみ、コード変更なし。
- HOST LOAD:実行時 (2:05) 8.31 /  ̄8.32 / 14.96 (15min = ncpu=1 0の約約約 1.5×) — ~2× gate 未満で実測可。(NOT skipped)。
- 実行バックエンド: terminal 直接 stdout は空 (/tmp redirect workaround で echo 実測)。execute_code は cron mode で BLOCKED。

##テスト (kbb -M:test)
- **robotics**: `Ran 14 tests containing 50 assertions. 0 failures,  ̄0 errors.` RC=0 — 基準値 (14/50/0) と一致。
- **giemon**: `Ran 46 tests containing	̄115 assertions. 0 failures,	 0 errors.` RC=0 — 基準値 (46/115/0) と一致。
- 判定: **measured、回帰なし** (両 suite とも exit 0、基準値と数字一致、git diff 空)。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (再現対象の学習ジョブ 0 件、git diff  ̄空)。seeded 再現は対象なし (bench-116 と同方針)。

##回帰
**なし (measured)** — robotics 14/50/0、giemon 46/115/0 を実測完走、exit 0、基準値 (bench-066 確定 / bench-114 最新) と両 suite とも一致。回帰なし。



git HEAD は不変 (コード変更なし)。IN-FLIGHT は未追跡のみ。



##反証 (falsify)
新規 falsify はなし。最新 falsify-038 (H39: damping/摩擦 はコアで消費され DR worst-case を検証できるか) は refuted 済 (コア実装は `:joint/damping` を一切読まず、純キネマティクス契約で摩擦面の検証面なし)。git diff 空 (追跡変更なし)・code 無変更のため新規 H の判定なし (新仮説なし)。

##再現コマンド
- 実行: `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test > /tmp/b_rob.txt 2>&1`; `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M:test > /tmp/b_gie.txt 2>&1` —許 完走 (measured,回帰なし)。/tmp/b_rob.txt / /tmp/b_gie.txt に実測保存。
- seeded 再現:対象なし (sim-loop L0、学習ジョブ未実装)。未実行。