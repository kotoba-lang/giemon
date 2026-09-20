# falsify-082 (H83) — test-runner 修復 (loader 登録 / .cljk 拡張子復帰 / nbb.edn deps floor) は HEAD 41ac173 で着地しているか

## 仮説
NEXT が runner repair を 43 連続発行している以上、core 側に修復 commit が着地している可能性を捨ててはいけない。
H83: HEAD 41ac173 で .cljk loader 登録 / test 拡張子復帰 / nbb.edn deps floor 接続のいずれかが実施済み。

## 実測 (純静的読取 + リダイレクト実測、/tmp redirect + read_file、cron 実行時間予算内)
- HOST LOAD (11:09 JST 実測): 1-min 8.63 / 5-min 11.67 / **15-min 12.46**, ncpu=10 → ≈1.25×。
  Load gate (15-min ≥ 2×ncpu=20) **未満の負荷帯** — 本走は load skip の言い訳が成立しない帯。
- HEAD: giemon `41ac173f8e9dc599e8b9ab340a51f4135d5ade98` (2026-09-16 08:21 +0900, "Merge agent/repo-bot-landed: land sim-loop bench-244〜269 / falsify-069〜073 and maturity.md")。
  tracked diff 空 (M = sim-loop/status/maturity.md のみ、?? は sim-loop evidence / probe)。
- `find . -name '*.cljk'` 実測 31 件: **test 側 10 ns 全件が `*_test.cljk` のまま**
  (giemon_test / viewer_test / kinematics_test / chassis_edn_test / chassis_test / ui_test /
  governor_test / arm_edn_test / export_test / arm_test — いずれも .cljk、.clj 復帰なし)。
- `deps.edn` 実測: `:test` alias は cognitect-labs/test-runner のまま
  (`:extra-deps {io.github.cognitect-labs/test-runner ...}`, `:main-opts ["-m" "cognitect.test-runner"]`,
  `:exec-fn cognitect.test-runner.api/test`)。**loader 登録 / カスタム test ns / 拡張子設定の追記なし**。
- repo root listing 実測: **`nbb.edn` が giemon に存在しない** (bb.edn も無し、deps.edn のみ)。
  falsify-074 (H75) の asymmetry (robotics は nbb.edn 在 / giemon 無) を HEAD 41ac173 で再実測。

## 判定: **refuted** (H83)
runner 修復は HEAD 41ac173 で未着地 — 44 連続目の refuted (falsify-034 起の FK guard と同型の滞留)。
silent-zero (clojure/kbb -M:test 0 tests RC=0) の根因 (falsify-069: JVM require が .cljk を
ロード不能) は不変で、本走は静的読取のみで確定。実行系 suite 実測は cron 予算切れで未完 →
test 計数は unmeasured (honest、捏造なし)。

## 再現手順
```
cd orgs/kotoba-lang/giemon
git rev-parse --short HEAD                      # -> 41ac173
find . -name '*_test.cljk' | wc -l              # -> 10 (test .cljk 復帰なし)
grep -n 'cognitect.test-runner' deps.edn        # -> alias 無変更、loader 登録なし
ls nbb.edn                                      # -> 無い
uptime                                          # 15-min < 2x ncpu で実測帯を確認
```

## コアへの 1 行メッセージ
runner repair は依然 0 commit — 15-min load 12.46 (< gate 20) の実測可能帯でも未着手が
44 連続確定。loader 登録 1 件 or test 拡張子復帰 1 commit が全 bench/falsify の前提。
