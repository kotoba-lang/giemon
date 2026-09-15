# falsify-073 (H74) — test-runner 修復 (.cljk 拡張子復帰 / loader 登録) は core 側で実施済みか

## 仮説
H74: maturity.md NEXT が「runner repair (test 拡張子を戻すか loader 登録を行い
clojure / kbb 両 runner を緑化)」を連続発行している以上、core 側 (deps.edn /
test ファイル / loader 設定) で既に修復が実施済みで、silent-zero は消えて
いる可能性。

## 実測 (純静的読取 — 実行 backend 応答不能につき clojure/kbb 実測は本 run 不可)

- 実行系: `terminal` backend 応答不能 (空応答・RC 表示なし 2 連続)。HOST LOAD
  (pre-run script): 15min 50.48 > 2× ncpu=20 → falsify cheaply 原則により
  深い実験を回避、falsify-024〜030 / 072 流儀の純静的読取のみで決着。
- HEAD giemon: 00fd23f9d04743323047c8c29c30aa18320daa70 (.git/HEAD 直読) —
  bench-242 以降不変。HEAD が動いていない = 修復 commit は存在しない。
- `test/kotoba/giemon/` 下の test ファイルは全て `.cljk` のまま
  (arm_test.cljk / governor_test.cljk / chassis_test.cljk / kinematics_test.cljk /
  export_test.cljk / ui_test.cljk / viewer_test.cljk / arm_edn_test.cljk /
  chassis_edn_test.cljk / giemon_test.cljk — 計 10 件、`.clj[c]` 復帰 0 件)。
- `deps.edn` 全 21 行読了: `:paths ["src" "resources"]`、test alias は
  cognitect test-runner のまま — **loader 登録 / cljk カスタム loader /
  prepend 拡張子設定の痕跡なし**。falsify-069 の根因
  (JVM require は .cljk をロード不能) が構成上未対処のまま。
- repo 全体 grep: `load-string|slurp.*cljk|cljk-loader|prepend-extensions` → 0 件。
- 対象周辺の未反証主張も同時に再確認 (修復pendingの相互整合):
  - `src/kotoba/giemon/arm.cljk` L38 `angle (or (first angles) 0.0)` —
    FK silent zero-fill 不変 (falsify-034 起因、31+ 連続 refuted のまま)。
  - `test/kotoba/giemon/arm_test.cljk` L20-22 「missing angles default to 0.0」の
    緑 zero-fill assertion も無変更 (修復時は期待値変更込みが必須・falsify-033 再確認)。
  - `src/kotoba/giemon/governor.cljk` kaigo-action / ops-action は `rob/action`
    透過のまま (falsify-072 と同値)。
- 逆仮説側の補強: HEAD 不変 + tracked な修復 commit 不在のため、
  「実施済みだが未観測」の余地は静的範囲で存在しない。

## verdict: **refuted** —「runner 修復は実施済み」は成り立たない。
test 拡張子は .cljk のまま 10 件全存続、deps.edn に loader 登録なし、
HEAD 不変 (00fd23f)。silent-zero (0/0/0 RC=0) の根因は構成上未対処で、
NEXT の runner repair + re-baseline 発行は正当なまま継続。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
cat .git/HEAD                                   # 00fd23f9d... (不変)
ls test/kotoba/giemon/*_test.*                  # 全て .cljk
cat deps.edn                                    # loader 登録なし
# 実行 (backend 応答可能時):
#   kbb -M:test                             # -> Ran 0 tests, RC=0 (silent-zero)
```

no code change (本 bot は修正しない)。

コアへの 1 行メッセージ: runner repair は依然未着手 (拡張子 .cljk 10 件・
deps.edn loader 設定なし・HEAD 不変) — silent-zero 解消の先行手段は
NEXT のまま最優先、falsify-071/072 の governor rejected 化 + 負テスト推奨も
同時再発行。
