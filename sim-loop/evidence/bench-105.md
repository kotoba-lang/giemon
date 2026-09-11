# bench-105 — giemon sim-loop bench (日次)

判定: **measured** — test スイート実測は完走、基準値 (bench-066 確定) と完全一致、回帰なし。



## 実行環境
- git HEAD: giemon `d0d3cb4` (robotics `9459ca0`) — 前回と不変、git diff 空 (追跡変更なし)。
- HOST LOAD: 負荷帯 ~2.6-3.0× ncpu (開始前 uptime 15min 26.13、実行後 15min 30.25) —
  suite 実測はこの帯域で完走。
- 実行バックエンド: terminal 直接 stdout は空のまま (echo 空) だが、`/tmp` redirect workaround は成立
  (falsify-031→033 と同手)。read_file で test 出力を実測取得。

## テスト（kbb -M:test 実測、/tmp redirect + read_file）
- **kotoba-lang/robotics**: `Ran 14 tests containing  ̂50 assertions. ̂0 failures,̂ 0 errors.` exit 0
- **kotoba-lang/giemon**:   `Ran 46 tests containing 115 assertions.̂ 0 failures,̂ 0 errors.` exit  ̂0

集計: robotics 14/50/0、giemon 46/115/0。基準値 (bench-066 確定) と完全一致。

## Seeded 再現 verdict
**N/A (対象外)** — sim-loop 学習ジョブは L0 未実装 (seed/L1+ 0 件、git diff 空)。再現対象の学習ジョブが存在しないため、本測定は行わない。



## 回帰
**なし** — robotics 14/50/0・giemon 46/115/0 が基準値と一致、両者 exit 0。measured で assert。



## 反証 (falsify)
新規 falsify はなし。未決 falsify 残存なし。



## 再現コマンド
- 実行: `kbb -M:test` (workdir: orgs/kotoba-lang/robotics → 14/50/0 exit 0; orgs/kotoba-lang/giemon →  ̂46/115/0 exit 0)
- seeded 再現: 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。