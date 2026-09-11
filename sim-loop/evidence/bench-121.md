# bench-121 — giemon sim-loop bench (日次)

判定: **unmeasured (skipped: load)** — HOST LOAD が ncpu=10 の ~2.5× (15min ~25.11) で Load gate (15min ≥ 2×ncpu≈20) 超過。重い kbb -M:test 実行・seeded 再現を省略。回帰 assert せず、基準値 (bench-066 確定 / bench-120 最新) を据え置き。(bench-099～101・bench-120 と同方針の honest 記録。)

## 実行環境
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-066 確定) と不変 (IN-FLIGHT は未追跡 sim-loop/・simloop_files_list.txt・statout.txt・tmp_probe_write.md のみ、コード変更なし)。
- 測定は load 超過で未実施のため HEAD は據え置き前提 (git diff 空の前提、コード変更なし)。
- HOST LOAD: 3:04 時点 20.20 / 25.24 / 25.11 (15min = ncpu=10 の ~2.5×) — 2× gate (≈20) 超過で skip。
- 実行バックエンド: terminal 直接 stdout は空 (/tmp redirect workaround)。execute_code は cron mode で BLOCKED。

## テスト (kbb -M:test)
- **skipped (load)** — Load gate 超過 (15min 25.11 ≥ 2×ncpu=10≈20)。重い両 suite 実行を省略し honest に未測定記録。回帰 assert せず基準値据え置き (robotics 14/50/0、giemon 46/115/0、exit 0 前提)。

## Seeded 再現 verdict
**N/A (対象外) + skipped (load)** — sim-loop 学習ジョブは L0 未実装 (再現対象の学習ジョブ 0 件)。加えて Load gate 超過で重い seeded 再現実行も省略 (honest、unmeasured)。

##回帰
**なし (assert せず)** — 本 run は load gate 超過で未測定 (unmeasured)。回帰 を assert せず、基準値 (robotics 14/50/0、giemon 46/115/0、HEAD d0d3cb4/9459ca0) を据え置き。git diff 空 (コード変更なし)。

##反証 (falsify)
新規 falsify はなし。最新 falsify-039 (H40: 監査ツール probe_parity_arm6.py 陳腐化) は refuted 済。maturity.md の NEXT は none で新規 H の判定なし (code 無変更のため)。

##再現コマンド
- 実行: 未実行 (**skipped: load**) — HOST LOAD 15min ~25.11 ≥ 2×ncpu=10≈20 で Load gate 超過。重い kbb -M:test (robotics/giemon) を省略。基準値据え置き (honest、unmeasured)。(実行コマンドは bench-119 / bench-118 参照:`cd <repo> && kbb -M:test > /tmp/b_*.txt 2>&1`。頃 3:04。
- seeded 再現:対象なし (sim-loop L0、学習ジョブ未実装) + skipped (load)。未実行。