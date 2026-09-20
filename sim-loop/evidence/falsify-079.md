# falsify-079 (H80) — 暫定 kbb 測定経路の 27/67/0 は実測緑か (silent-green / silent-skip 破れの有無)

## 仮説
H80: falsify-075 が「governor_test (6 tests) を暫定経路に含められる — 未測定」として
据え置いた項目に対し、暫定経路 (kbb --backend sci --classpath src:test + robotics src
+ 明示 require) の緑値は (a) テストが実際に実行された数である (静的集計と一致)、
(b) failure を検出する (silent-green ではない) — の両方を成立させる。
成立しなければ暫定経路の 21/52/0 (および拡張 27/67/0) は「実測」として数えられない。

## 実測 (giemon HEAD 41ac173f8e9d…, HOST LOAD 15min 10.5–14.7 ≈ 1.1–1.5× ncpu=10 → Load gate 内・実施)

1. 静的集計 (grep -c): deftest — arm 5 / chassis 10 / kinematics 4 / viewer 2 /
   governor 6 (計 27)。`(is ` — arm 11 / chassis 25 / kinematics 9 / viewer 7 /
   governor 15 (計 67)。
2. 拡張実行: kbb --backend sci --classpath
   "src:test:$ROBOTICS_SRC:/tmp/f079_fake" /tmp/f079_ext.cljs (5 ns 明示 require +
   run-tests) →
   **`Ran 27 tests containing 67 assertions. 0 failures, 0 errors.` RC=0**
   — 静的集計 (27 / 67) と完全一致。governor_test 6/15 は falsify-075 以来未測定
   だった分が本走で初めて実測に乗った (falsify-070 の 21/52/0 + 6/15 = 27/67)。
3. silent-green 否定プローブ: /tmp/f079_fake/kotoba/giemon/zf079fail_test.cljk
   (deftest 1 件、`(is (= 1 2))` の意図的失敗) を同 classpath で run-tests →
   **`FAIL in (deliberate-failure) ... 1 failures, 0 errors.` RC=1** —
   同一経路は failure を検出して RC=1 を返す。緑は「飛ばされたから緑」ではない。

## verdict: **refuted** — H80 (暫定経路が silent-green / silent-skip を含む) は不成立。
- 暫定 kbb 経路の緑値は静的 deftest / is 集計と 1 対 1 で一致し、fail 検出能力も
  実測で確認された。27/67/0 は実測緑として数えてよい。
- 暫定測定経路の基準値を **giemon 27/67/0** (4 loadable ns + governor_test) に更新。
  残差 5 ns (arm-edn / chassis-edn / export / ui — deps floor と host interop) は
  falsify-070 のままで、46/115 完全回復には runner repair (NEXT) が要る。
- 併せてメモ: governor_test 15 assertions 中に nil 経路の負テストは実在しない
  (falsify-072/076 の「負テスト 0 件」をこの集計からも整合 — 15 件は :move 経路
  のみ)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
git rev-parse HEAD   # 41ac173f8e9dc599e8b9ab340a51f4135d5ade98
ROBO=/Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics/src
kbb --backend sci --classpath "src:test:$ROBO:/tmp/f079_fake" /tmp/f079_ext.cljs
# -> Ran 27 tests containing 67 assertions. 0 failures, 0 errors.  RC=0
kbb --backend sci --classpath "src:test:$ROBO:/tmp/f079_fake" /tmp/f079_fail.cljs
# -> FAIL in (deliberate-failure) ... 1 failures, 0 errors.          RC=1
```
生出力: /tmp/f079_ext_out.txt, /tmp/f079_fail_out2.txt, /tmp/f079_state.txt。
プローブ /tmp 配置のみ (repo tracked に触らない、falsify-031 の /tmp workaround 前例準拠)。

no code change (本 bot は修正しない)。

コアへの 1 行メッセージ: 暫定 kbb 経路は silent-green でないことを fail-probe で実証、
基準値を 27/67/0 (governor_test 込み) に更新してよい。次の runner repair の検収条件に
「fail 挿入で RC=1 になる」を 1 行足すこと (clojure / kbb -M:test 側は silent-zero RC=0
のままなので、これは本経路で確認済みの性質を新 runner に引き継ぐための検収)。
