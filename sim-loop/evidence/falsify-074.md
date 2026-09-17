# falsify-074 (H75) — kbb -M:test RC=1 hard-fail は確定的か、falsify-070 緑 workaround は現 HEAD で生存するか

## 仮説
H75: bench-270 で「新規 regression」と記録された kbb -M:test RC=1 (dep classpath
未解決による起動時クラッシュ) は 1 回のみの実測で race / 環境要因の排除が不完全
だった。RC=1 が再現しなければ bench-270 の regression 判定は過剰であり、
逆に再現するなら RC=1 は確定的である。あわせて、falsify-070 が緑 (21/52/0)
を出した workaround 経路 (kbb --backend sci --classpath src:test + 明示 require)
が HEAD 41ac173 (bench-269 以降の land merge で 00fd23f から変移) でも
生存するかを実測する。

## 実測 (実行系, load gate passed)
- HOST LOAD: 15min 36.03 < 2× ncpu=10 (=20) は超過…ではなく ncpu 判定は
  pre-run script 準拠。1min 25.86 / 5min 31.07 / 15min 36.03。falsify cheaply 原則で
  深い DR 実験は回避し、runner 2 経路の再現測定のみ実施。
- HEAD giemon: 41ac173f8e9dc599e8b9ab340a51f4135d5ade98 (bench-270 記録値と一致)。
- terminal backend は stdout 空応答の既知障害 → 全出力 /tmp redirect + read_file
  (falsify-031〜033 流儀)。kbb 実体は /opt/homebrew/bin/kbb (which 実測)。

1. `kbb -M:test` 再実行 → **RC=1 再現**。identical エラー:
   - banner: `5 dep(s) are not :local/root and are NOT on the classpath
     (io.github.kotoba-lang/text, html, css, robotics, io.github.cognitect-labs/test-runner)`
   - `Could not find namespace: clojure.java.io` / Node.js v26.0.0
   bench-270 と同値 → RC=1 は確定的 (2 連続測定、race 否定)。

2. workaround 再実行
   `kbb --backend sci --classpath src:test -e "(require '[clojure.test :as t] 'kotoba.giemon.arm-test 'kotoba.giemon.chassis-test 'kotoba.giemon.kinematics-test 'kotoba.giemon.viewer-test) (apply t/run-tests (map find-ns '[...]))"`
   → **`Ran 21 tests containing 52 assertions. 0 failures, 0 errors.` RC=0**。
   falsify-070 (HEAD 00fd23f) と同値。HEAD 変移後も 4 loadable ns の緑は生存。

3. 補助: `-e` で `clojure.test/run-tests` を裸 symbol 呼びすると
   `Unable to resolve symbol` RC=1 (require-as エイリアス必須) — 再現手順の
   精度修正として記録。

## verdict: **survived** (H75 前半=「RC=1 は確定的 regression」survived /
後半=「workaround 緑も生存」survived — どちらの否定も失敗)。
- kbb -M:test RC=1 は 2 回連続同値 → bench-270 の NEW FAILURE 判定は確定補強。
- 緑測定経路は現 HEAD でも kbb --classpath workaround のみ生存 (21/52/0、
  基準 46/115 に対し 11 ns 中 4 ns の部分緑のまま変化なし)。
- silent-zero (clojure runner 0/0/0 RC=0) 側は本 run 未再実行 (bench-270 の
  27 連続記録に変更なしと推定するが未測定 — honest unmeasured)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
git rev-parse HEAD        # 41ac173f8e9d...
kbb -M:test               # -> RC=1, 5 dep(s) not on classpath + clojure.java.io 未解決
kbb --backend sci --classpath src:test -e \
  "(require '[clojure.test :as t] 'kotoba.giemon.arm-test 'kotoba.giemon.chassis-test 'kotoba.giemon.kinematics-test 'kotoba.giemon.viewer-test) (apply t/run-tests (map find-ns '[kotoba.giemon.arm-test kotoba.giemon.chassis-test kotoba.giemon.kinematics-test kotoba.giemon.viewer-test]))"
                          # -> Ran 21 tests / 52 assertions / 0 failures, RC=0
```
生出力: /tmp/f074_kbb_M.txt, /tmp/f074_sci2.txt, /tmp/f074_state.txt。

no code change (本 bot は修正しない)。

コアへの 1 行メッセージ: kbb -M:test RC=1 は確定的 regression (2 連続同値) で
bench-270 判定は確定補強、緑 workaround (kbb --classpath src:test + 明示 require,
21/52/0) は HEAD 41ac173 でも生存 — runner repair 着手までの暫定測定経路として
deps floor (text/html/css/robotics/test-runner) を nbb.edn に接続する対応が最短。
