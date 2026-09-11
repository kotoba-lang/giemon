# bench-109 — giemon sim-loop bench (日次)

判定: **measured** — test スイート実測は完走、基準値 (bench-066 確定 / bench-102・105・107・108 最新実測) と完全一致。回帰なし。

## 実行環境
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 前回 (bench-108) と不変。
- git diff: 追跡ファイル変更なし (robotics / giemon とも porcelain 空)。IN-FLIGHT は未追跡 sim-loop/ ・simloop_files_list.txt・
  statout.txt・tmp_probe_write.md のみ (bench-108 と同構成、コード変更なし)。
- HOST LOAD: 開始前 (22:14) 20.65 / 25.73 / 28.21 (15min = ncpu=10 の約 2.8×、1min は約 2.1×)。
  bench-108 (前回 measured) と同程度の負荷帯 (~1.5-3×) — suite 実測はこの帯域で確実に成立。
.
  (bench-107 を skip した 1min 60.x ≈ 6× とは異なり、今回は省略しない。)
- 実行バックエンド: terminal 直接 stdout は空のまま (echo 空、search_files は "could not stat"
  応答不能) だが、`/tmp` write + read_file workaround は成立 (falsify-031→033・bench-105/107/108 と同手)。
  本 walk もこの手で test 出力を実測取得。execute_code は cron mode で BLOCKED。

## テスト（kbb -M:test 実測、/tmp redirect + read_file）
- **kotoba-lang/robotics**: `Ran 14 tests containing  ̂50 assertions. ̂0 failures,̊ 0 errors.` exit rc=0
- **kotoba-lang/giemon**:   `Ran 46 tests containing ̊115 assertions.̊ 0 failures,̊  ̂0 errors.` exit rc=0

集計: robotics 14/50/0、giemon 46/115/0。基準値 (bench-066 確定・bench-102/105/107/108 最新実測) と完全一致。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (sim-loop トップに evidence/manual/status のみ。
  seed/L1+ 学習ジョブ 0 件、git diff 空)。再現対象の学習ジョブが存在しないため、
 seeded 再現の本測定は行わない (bench-102〜108 と同方針)。

## 回帰
**なし** — robotics 14/50/0・giemon 46/115/0 が基準値と一致、両者 exit rc=0。measured で assert。並
 (bench-108 に続く実測完走。)

## 反証 (falsify)
新規 falsify はなし。falsify-034 (H35: FK angle-count guard repair 実装済みか) は前 walk で
静的読取 refuted (修復未実施)。本 walk でも git diff 空・test 20-22 無変更のため残存なしのまま。
未決 falsify 残存なし (H25〜H35 全決着)。

## 再現コマンド
- 実行: `kbb -M:test` (workdir: orgs/kotoba-lang/robotics → 14/50/0 rc=0;
  orgs/kotoba-lang/giemon → 46/115/0 rc=0)
- seeded 再現: 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。