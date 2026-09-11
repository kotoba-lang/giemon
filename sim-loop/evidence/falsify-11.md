# falsify-11 — NaN / ±Inf レーティング・要件の neg? フィルタ無音通過

日時: cron iteration (JST 2026-09-04, host load avg 約 29 / コア 10 → 軽量 REPL 測定のみ)

## 仮説

falsify-6〜10 は「欠落 (nil / typo / 未割当)」の fail-open を実測した。
未反証の隣接面は **数値センチネル**:
`underrated-joints` は `(filter #(neg? (:torque/headroom %)) ...)` で判定しており
(`src/kotoba/giemon/arm.cljk` L120-121)、IEEE 例外値は例外も投げず比較も素通しする。
`:cont-nm` か `:joint/limit :effort` が `##NaN` なら headroom は `##NaN`、
`neg? ##NaN` は false → 「未満ではない」= 合格扱いで違反 0 件になるのではないか。
falsify-10 で nil/文字列の `:cont-nm` は ClassCastException/NPE で fail-closed だったのに対し、
NaN は**例外も違反検出も無い**第 3 の経路のはず。

## 実測

コード: `src/kotoba/giemon/arm.cljk` L95-121 (`torque-headroom` / `underrated-joints`)。
fixture: 2 段階 read (falsify-2 手順) で `:arm/chain` joint 6 を復元し
j1 の値だけ差し替えて arm に渡す (falsify-5/10 と同一手法)。

```
--- baseline (falsify-5/10 再測定)
:underrated ()                                  ; headroom j1/j2/j5=0, j3+10, j4+6, j6+2.3

--- A: j1 :cont-nm ##NaN (rated 40 → NaN に破損)
:underrated ()                                  ; 違反 0 件
j1 row: {:torque/required 40 :torque/rated ##NaN :torque/headroom ##NaN}

--- B: j1 :joint/limit :effort ##NaN (required 40 → NaN に破損)
:underrated ()                                  ; 違反 0 件
j1 row: {:torque/required ##NaN :torque/rated 40 :torque/headroom ##NaN}

--- C: j1 :joint/limit :effort ##-Inf (要件が「無限大」に破損)
:underrated ()                                  ; 違反 0 件
j1 row: {:torque/required ##-Inf :torque/rated 40 :torque/headroom ##Inf}
                                                ; 有限 40N·m が「無限要件を満たす」ことになる

--- 対照: j1 :cont-nm 30.0 (本物の過小評価)
:underrated ["j1"]                              ; 正しく検出される → フィルタ自体は機能中
```

読み取り:
- rated / required のどちらが NaN でも headroom は NaN になり、`neg?` は false を返す。
  違反リストは空で、torque 検査は「通過」する。nil (falsify-6) でも文字列 (falsify-10)
  でもない第 3 経路: **IEEE センチネルは例外にも違反検出にもならない**。
- `##-Inf` 要件は有限レーティングで headroom `##Inf` となり無音合格 —
  「設計要件の上限」契約が任意のレーティングで満たされる。
- 返り値は falsify-10 と同じ truthy な `()` なので nil/empty チェックでも検知不能。
- 到達経路: `##NaN` は合法 EDN リテラルで `clojure.edn/read-string` がそのまま読む。
  fixture 破損・外部 JSON 変換 (NaN を含む)・算術誤爆のいずれでも入り得る。

## Verdict: refuted

torque 余裕検査の契約 (「割り当てアクチュエータの連続レーティングが設計要件を下回る
joint を列挙する」) に対し、NaN / ±Inf の入力は下回りの評価すら行われず**無音で合格**する。
neg? 一本の比較ではセンチネルを分類できず、falsify-6/10 の fail-open 系に
「非有限数値の無検査採用」が加わる。修理は rated/required を読んだ直点で
`(Double/isFinite x)` 検査 (非有限は例外化) を入れ、neg? 比較に進ませないこと
(falsify-6/10 の件数一致検査と同一の fail-closed 化箇所で済む)。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '(require (quote [clojure.edn]) (quote [kotoba.giemon.arm :as arm]))
(def m (first (clojure.edn/read-string (slurp "fixtures/giemon_arm6/giemon_arm6.edn"))))
(def ch (clojure.edn/read-string (:arm/chain m)))
(defn set-j1 [f] {:arm/chain (mapv #(if (= (:joint/name %) "j1") (f %) %) ch)})
(prn (arm/underrated-joints (set-j1 #(assoc-in % [:joint/actuator :cont-nm] ##NaN))))
(prn (arm/underrated-joints (set-j1 #(assoc-in % [:joint/limit :effort] ##NaN))))
(prn (arm/underrated-joints (set-j1 #(assoc-in % [:joint/limit :effort] ##-Inf))))'
;; => () () ()   (対照: cont-nm 30.0 なら ["j1"] が検出)
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-11 実測 — `:cont-nm` / `:effort` の `##NaN`・`##-Inf` は
headroom をセンチネルにし `neg?` フィルタを無音通過して違反 0 件で合格
(例外にも違反にもならない第 3 経路)。torque 検査修理時に rated/required の
isFinite 検査 (非有限は例外化) を falsify-6/10 の fail-closed 化と同じ箇所に入れること。
