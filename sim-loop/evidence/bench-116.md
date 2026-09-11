# bench-116 — giemon sim-loop bench (日次)

判定: **unmeasured (skipped: load)** — HOST LOAD が ncpu=10 の ~3.6× (15min 35.65) と超過、test スイート実測は省略。回帰 assert せず (基準値据え置き、honest)。

tests: **未実行** (load 超過により skip)。基準値は据え置き: robotics 14/50/0、giemon 46/115/0 (bench-066 確定 / bench-114 最新実測)。

## 実行環境
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-114) と不変。git diff 両方とも空 (追跡変更なし)。IN-FLIGHT は未追跡 sim-loop/・simloop_files_list.txt・statout.txt・tmp_probe_write.md のみ、コード変更なし。
- HOST LOAD: 実行時 (1:39) 32.49 / 38.19 /35.65 (15min = ncpu=10 の約約約 3.6×) — ~2× gate を大きく超過のため suite 実測を一律 skipped (負荷緩和時 re-measure 予定)。
- 実行バックエンド: terminal 直接 stdout は空 (/tmp redirect workaround で echo 実測)。execute_code は cron mode で BLOCKED。

##テスト (kbb -M:test)
**skipped (load)** —  ̄15min load 35.65 = ncpu=10 の約約約 3.6× (≥~2× gate)。bench-104〜110・115 と同系の load 超過、実測せず、honest に unmeasured 記録;;基準値据え置き、回帰 assert せず。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (再現対象の学習ジョブ 0 件、git diff 空)。seeded 再現は対象なし (bench-115 と同方針)。

##回帰
**未判定 (unmeasured)** — load 超過で test スイート実測をスキップのため回帰は assert しない;;基準値 (robotics 14/50/0、giemon 46/115/0) は据え置き。



git HEAD は不変 (コード変更なし)。

##反証 (falsify)
新規 falsify はなし。最新 falsify-038 (H39: damping/摩擦 はコアで消費され DR worst-case を検証できるか) は refuted 済 (コア計算は `:joint/damping` を一切読まず、純キネマティクス契約で摩擦面の検証面なし)。git diff 空 (追跡変更なし)・code 無変更のため新規 H の判定なし (新仮説なし)。

##再現コマンド
- 実行: `kbb -M:test` (robotics / giemon) — **skipped (load))**: 15min load 35.65 > ~2× ncpu=10 gate。負荷緩和時に re-measure 予定)。
- seeded 再現: 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。