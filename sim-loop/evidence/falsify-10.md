# falsify-10 — 非評価 joint (actuator 未割当) の torque 検査からの無音除外

日時: cron iteration (JST 2026-09-04, host load avg 約 24 / コア 10 → 軽量 REPL 測定のみ)

## 仮説

falsify-6 は `arm/bom` 全体 nil 時の fail-open だった。未反証の隣接面は **joint 単位の欠落**:
`chain-actuators` は `(:joint/actuator joint)` が無い joint を `keep` で黙って落とし、
`torque-headroom`/`underrated-joints` は BOM に無い joint を `:when a` で黙ってスキップする。
design requirement (`:joint/limit :effort`) を持つ joint に actuator が 1 つも割り当てられて
いない (= そもそも torque 評価不能) 状態でも、`underrated-joints` は違反 0 件を返し、
検証が「通って」しまうのではないか。返り値が `()` (truthy) なら nil チェックでも
検知できない (falsify-6 の「nil → 0 件」に対し「空リスト → 0 件」の亜種)。

## 実測

コード: `src/kotoba/giemon/arm.cljc` L48-64 (`chain-actuators` の `keep`+`when-let`)、
L104-121 (`torque-headroom` の `:when a` / `underrated-joints`)。
fixture: 2 段階 read (falsify-2 手順) で `:arm/chain` joint 6 を復元し
`{:arm/chain ...}` として arm に渡す (falsify-5 と同一手法)。

```
--- baseline (falsify-5 再測定)
:joint-count 6 :bom-count 6
headroom: j1=0, j2=0, j3=+10, j4=+6, j5=0, j6=+2.3000000000000007
:underrated ()                      ; falsify-5 と数値一致

--- 仮説入力: j1 だけ :joint/actuator を削除 (未割当 = 未評価 joint)
:joint-count 6 :bom-count 5         ; joint 6 なのに BOM 5 — 不整合は無検出
:underrated ()                      ; 違反 0 件
:headroom-joints [j2 j3 j4 j5 j6]   ; j1 が黙って消えた (design effort 40 の肩関節)

--- 対照 1: :cont-nm nil (不良レーティング)
=> NullPointerException (fail-closed: 例外で停止)

--- 対照 2: :cont-nm "35.0" (文字列レーティング)
=> ClassCastException (fail-closed: 例外で停止)

--- 呼び出し側から見た未割当 arm
:empty? true :nil? false            ; () は truthy — nil チェックでも検知不能
```

読み取り:
- joint 6 / BOM 5 という構造的不整合はどこからも検出されず、design effort 40 の
  joint j1 が評価対象から黙って消えて違反 0 件。
- 不良値 (nil/文字列の `:cont-nm`) は例外で fail-closed なのに対し、
  **欠落 (キーごと無い) だけは無音で通る** — fail-open は「欠落」に特化している。
- falsify-6 (bom 全体 nil → 0 件) の joint 単位版であり、返り値が truthy な `()` なので
  呼び出し側の nil ガードでも防げない。

## Verdict: refuted

torque 余裕検査の契約 (「割り当てアクチュエータが設計要件を満たすか」) に対し、
actuator 未割当 joint は「要件を満たす」とは評価されず、**評価されずに黙って除外** され、
未評価のまま 0 件違反として通過する。falsify-6/7/8/9 と同型の fail-open で、
迂回面は joint 単位の欠落入力にまで拡大 (修理は `arm/bom` の fail-closed 化に加え、
`joint-count` と BOM 件数の一致検査、または未割当 joint の明示報告が必要)。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '(require (quote [clojure.edn]) (quote [kotoba.giemon.arm :as arm]))
(def m (first (clojure.edn/read-string (slurp "fixtures/giemon_arm6/giemon_arm6.edn"))))
(def ch (clojure.edn/read-string (:arm/chain m)))
(def unrated {:arm/chain (mapv #(if (= (:joint/name %) "j1") (dissoc % :joint/actuator) %) ch)})
(println (arm/joint-count unrated) (count (arm/chain-actuators unrated)))
(prn (arm/underrated-joints unrated))'
;; => 6 5 / ()
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-10 実測 — actuator 未割当 joint は torque 検査から無音除外され
違反 0 件で通過 (joint-count 6 vs BOM 5 の不整合も無検出、返り値は truthy な `()`)。
falsify-6 の fail-closed 化修理時に「未評価 joint の無音スキップ」も同時に塞ぐこと
(件数不一致例外化 or 未割当 joint の明示列挙)。
