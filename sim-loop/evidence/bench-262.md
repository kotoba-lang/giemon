# bench-262 — falsify iteration (2026-09-15 11:05 JST)

## 仮説 (H74)
「cljk rename + kbb cutover HEAD での silent-zero は一時的なもので、現時点で
kbb -M:test が緑に復帰している」— runner 修復の有無を本日時点で再確認する。

## 実測 (負荷 gate 内)
- HOST LOAD 15min ≈15.38 (≈1.5× ncpu=10, Load gate 15min ≥ 2×ncpu=20 未満 → 実行許可)。
- HEAD giemon 00fd23f9d04743323047c8c29c30aa18320daa70 / robotics
  ad99366bc7bef949e86ee33b7e04d12525dffe46 — bench-244〜261 と同一 HEAD 不変。
  tracked diff 空 (?? sim-loop/ evidence + M status/maturity.md のみ)。
- `kbb -M:test` 両 suite 再実測: giemon「Ran 0 tests containing 0 assertions.
  0 failures, 0 errors.」RC=0 / robotics 同値 RC=0
  (fixture /tmp/b262_gie.txt, /tmp/b262_rob.txt)。
  基準値 robotics 23/558/0・giemon 46/115/0 から -100% 不変 —
  **silent-zero 持続 18 連続 (bench-244〜262 の measured)**。H74 refuted。
- 第2測定経路 (falsify-070) 再実測:
  `kbb --backend sci --classpath src:test -e "(require '[clojure.test :as t])…"`
  4 ns (arm/chassis/kinematics/viewer -test) →
  **Ran 21 tests containing 52 assertions. 0 failures, 0 errors. RC=0 (measured 緑)**
  (fixture /tmp/b262_kbb2.txt)。falsify-070 の 21/52/0 緑を再現 —
  再現手順: kbb --backend sci --classpath src:test + 明示 require + (t/run-tests …)。
  注意: `(clojure.test/run-tests …)` 直接参照は sci 解析エラー RC=1
  (fixture /tmp/b262_kbb_gie.txt, Unable to resolve symbol) — aliased `t/run-tests` が必須。

## 判定
- H74 refuted — silent-zero は未解決 (runner 修復未着手)。
- 回帰 assert なし (既知 runner defect の持続 re-measured、新規破れなし)。
- falsify-034 (FK guard repair 未配線) 据え置き。falsify-071/072 (governor silent-nil)
  据え置き (NEXT 推奨継続)。

## verdict: refuted (H74)

## 再現手順
```
cd orgs/kotoba-lang/giemon && kbb -M:test        # → 0/0/0 RC=0 (silent-zero)
cd orgs/kotoba-lang/robotics && kbb -M:test      # → 0/0/0 RC=0 (silent-zero)
cd orgs/kotoba-lang/giemon && kbb --backend sci --classpath src:test \
  -e "(require '[clojure.test :as t])(require 'kotoba.giemon.arm-test)…(t/run-tests …)"
  # → Ran 21 tests containing 52 assertions. 0 failures, 0 errors. RC=0
```

## コアへの 1 行メッセージ
test-runner 修復は未着手のまま silent-zero 18 連続 — `.cljk` 拡張子を戻すか
loader 登録を行い clojure / kbb 両 runner を緑化してください (NEXT 最優先のまま)。
END
