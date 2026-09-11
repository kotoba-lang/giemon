# falsify-6 — torque 余裕違反シナリオ: 不明 variant 名で `arm/bom` が nil を返し `underrated-joints` が無音 0 件 (fail-open) になるか

## 仮説

`kotoba.giemon.arm/bom` は `:arm/realization` に存在しない variant 名 (typo 含む) を渡すと
nil を返す。呼び出し側が `(underrated-joints arm (bom arm variant))` の形で
torque 検証を行うと、nil の actuator リストはデフォルト BOM にフォールバックせず
**空合扱いで underrated 0 件を返し、設計要求違反があっても無音で通過する (fail-open)** —
これで torque 検証ゲートを迂回できる。

## 実測 (2026-09-03, JST)

2 段階 read の fixture (falsify-2/3/5 と同手順、加工なし) で実コードを実行:

1. **typo variant**: `(arm/bom arm-spec :all-qd)` (実名は `:all-qdd`) → **nil**
2. `(count (arm/underrated-joints arm-spec (arm/bom arm-spec :all-qd)))` → **0**
   (j1/j2/j5 は headroom 0 なのでデフォルトでも 0 件だが、ここでは「どの joint の
   actuator も検査対象から外れる」ことが問題 — 検査が実行されていない)
3. **対照実験 (本物の迂回は検出されるか)**: `:variants :under-rated :override` で
   j1 に cont-nm 10 N·m (要求 40 N·m) の actuator を差し込み `:under-rated` variant で
   検証 → `(arm/bom ...)` は BOM を返し、`underrated-joints` は
   **1 件を正しく検出**: `{:joint/name "j1", :torque/required 40, :torque/rated 10, :torque/headroom -30}`
4. デフォルト variant は変わらず underrated 0 件 (falsify-5 再現)。

## verdict

**refuted** — torque 検証には fail-open 迂回路がある。variant 名が 1 文字でも
違えば `bom` が nil を返し、`underrated-joints` が例外も出さず 0 件を返す。
(制約: 違反 actuator を override に仕込んだ本物の検査入力自体は正しく検出される。
迂回は nil 伝播経路のみ。)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb -M -e "
(require '[clojure.edn] '[kotoba.giemon.arm :as arm])
(def m (first (clojure.edn/read-string (slurp \"fixtures/giemon_arm6/giemon_arm6.edn\"))))
(def arm-spec {:arm/chain (clojure.edn/read-string (:arm/chain m))
               :arm/realization (clojure.edn/read-string (:arm/realization m))})
(prn (arm/bom arm-spec :all-qd))                 ; => nil (typo)
(prn (count (arm/underrated-joints arm-spec (arm/bom arm-spec :all-qd)))) ; => 0 (無音通過)"
```

## コアへの 1 行メッセージ

giemon-sim へ: `arm/bom` は不明 variant で nil を返し `underrated-joints` が無音 0 件になる
fail-open — `bom` nil 時に例外か明示的エラーにするか、`underrated-joints` 側で nil を
拒絶する (fail-closed) 修正を検討すること。(fixture 3 キー修理は引き続き OPEN)
