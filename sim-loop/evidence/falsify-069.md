# falsify-069 (H70) — silent-zero は discovery 不一致ではなく loadability 破れか (実行系実測)

## 仮説
H70: bench-244/245 の silent-zero (両 repo 0/0/0) が cognitect runner の
`*_test.cljk` discovery 不一致だけなら、namespace を直接 require すれば
arm-test はロード・実行できるはず (→ FK silent zero-fill も runtime 実測可能)。

## 実測 (実行系, load gate passed)
- HOST LOAD: 1min 7.63 / 5min 7.47 / 15min 8.02 (15min < 2x ncpu=20) → gate 通過。
  falsify-068 が skip した runtime 測定を本 run で実施。
- HEAD giemon: 00fd23f9d04743323047c8c29c30aa18320daa70 (bench-242 以降不変)。
- 直接 require probe:
  `kbb -M -e "(require 'kotoba.giemon.arm-test ...)"`
  → **FileNotFoundException**: `Could not locate kotoba/giemon/arm_test__init.class,
  kotoba/giemon/arm_test.clj or kotoba/giemon/arm_test.cljc on classpath.` RC=1。
  JVM require は `.cljk` を一切読めない。arm_test.cljk は classpath 上に存在するが
  拡張子不一致で locate 不可能。
- 結論: silent-zero の根因は「runner が .cljk を発見しない」だけでなく
  **require 自体が .cljk をロード不可能** という二重破れ。
  runner の discovery 設定を直しても現 extension のままでは復帰しない。
- 静的補助測定: `within-limits?` は arm.cljk L15 defn / L28 docstring /
  arm_test.cljk L28-30 単体テストのみで FK 本体呼出 0 (falsify-068 再確認、不変)。
  silent zero-fill `(or (first angles) 0.0)` L38 不変。

## verdict: refuted
H70 を refuted — namespace は直接 require でもロード不能 (RC=1 measured)。
arm-test を現 HEAD で runtime 実行できる緑パスは clojure / kbb 両 runner とも存在しない
(bench-244: kbb RC=1 両 repo、本 run: 直接 require RC=1)。silent-zero は
extension (.cljk) 起因の loadability 破れが根因、discovery 不一致は二次。

## 再現手順
```
cd orgs/kotoba-lang/giemon
kbb -M -e "(require 'kotoba.giemon.arm-test)"   # -> FileNotFoundException, RC=1
kbb -M:test                                     # -> Ran 0 tests (bench-244/245)
grep -rn "within-limits" src/kotoba/giemon/ test/kotoba/giemon/
git rev-parse HEAD
```

## コアへのメッセージ (1 行)
NEXT 再発行: silent-zero 修復は runner discovery 設定だけでは不十分 —
test ファイル拡張子 (.cljk→.clj[c] 又は loader 登録) を戻さない限り
JVM require は arm_test をロード不能で、FK guard repair の検証も runtime で不可能。
