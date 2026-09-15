# falsify-070 (H71)

仮説: bench-244 の結論「緑 runner は現状存在しない」は完全には成り立たない —
`kbb -M:test` の silent-zero (0/0/0 RC=0) は discovery+loadability 二重破れだが、
kbb (ADR-2609111700 正規 runtime) + 明示 namespace require 経路なら .cljk をロードし
実測緑を回復できる。

## 実測 (giemon HEAD 00fd23f9d047, HOST LOAD 15min ≈17.4 ≈1.7× ncpu=10 → Load gate 内・実施)

1. `kbb --backend sci -e "(require 'kotoba.giemon.arm-test)"` (classpath 無し) →
   RC=1 "Could not find namespace" (bench-244 の kbb RC=1 と同値 — classpath 指定が条件)。
2. `kbb --backend sci --classpath src:test -e "(require 'kotoba.giemon.arm-test)"` → **RC=0**。
3. 9 test namespace 個別 require 実測:
   - RC=0: arm-test / chassis-test / kinematics-test / viewer-test (4/9)
   - RC=1: arm-edn-test (L23 `catch Exception` — host interop 記法) /
     chassis-edn-test / export-test / ui-test (依存 `kotoba.lang.text` 未解決) /
     governor-test (依存 `kotoba.robotics` 未解決) (5/9)
4. loadable 4 ns を `clojure.test/run-tests` で実測:
   **`Ran 21 tests containing 52 assertions. 0 failures, 0 errors.` RC=0**
   (`kbb -M:test` の 0/0/0 と対照 — silent-zero は runner/discovery 側の破れで、
   suite 自体は生存)。

## verdict: **refuted** —「緑 runner は存在しない」は過剰主張。
   kbb + classpath + 明示 require で緑測定は可能 (21/52/0 measured)。ただし
   基準値 46/115 の完全回復は未達: 残差は discovery ではなく
   (a) deps floor (io.github.kotoba-lang/text, robotics が kbb classpath 未接続)、
   (b) host interop (`catch Exception` は ClojureScript/kbb で解析不可)。
   bench-244 の root-cause 属性「runner が *_test.cljk をマッチしない」と整合し、
   runner repair は kbb -M:test 側の修正のみならず kbb 経路を第 2 測定経路と
   できる事を示す。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb --backend sci --classpath src:test /tmp/f070_run.cljs
# require arm/chassis/kinematics/viewer -test → run-tests
# → "Ran 21 tests containing 52 assertions. 0 failures, 0 errors." RC=0
```

生出力: /tmp/f070_run_out.txt, /tmp/f070_ns_rc.txt, /tmp/f070_ns_kotoba.giemon.*.txt。
no code change (本 bot は修正しない)。

コアへの 1 行メッセージ: runner repair 時、kbb --classpath src:test + 明示 require は
既に緑測定可能 (21/52/0)。残り 5 ns の失敗は deps floor 未接続と host interop
(`catch Exception`) が原因で、discovery 修正だけでは 46/115 に届かない。
