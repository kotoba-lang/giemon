# falsify-16 — track-drive 逆運動学 `twist->track-speeds` が `track-width` を全く検査せず (負幅は無音、零幅は角度コマンドの無音破棄)

日時: cron iteration (JST 2026-09-04, host load avg 約 59-68 / コア 10 → 軽量 REPL 測定のみ)

## 仮説

falsify-14/15 が潰したのは arm/kinematics 側。未反証の隣接面は
`chassis.cljc` の track-drive 運動学 (DR 撹拌で track-width / track speeds
が破損する入力経路)。`track-speeds->twist` の `:twist/angular` は
`(/ (- right left) track-width)` — width が 0 ならゼロ除算例外だが、
`twist->track-speeds` (逆関数) は `(* angular track-width)` の積なので
width を一切検査していないのではないか:

1. 負の `track-width` は例外無しで通過し、`:twist/angular` の**符号が
   無音に反転**する (右回り/左回りの反転 — URDF/fixture の幾何破損が
   制御意図と逆向きの挙動として流れる)。
2. 零幅で `twist->track-speeds` を呼ぶと、回転コマンドが無音に捨てられ、
   直進用の track speeds が返る (`fwd` は例外で fail-closed、`inv` は
   fail-open — 同一契約の逆関数で非対称)。
3. `##NaN` width/speeds は falsify-14/15 と同型の非有限素通り。

## 実測

コード: `src/kotoba/giemon/chassis.cljk` (track-speeds->twist L28-35,
twist->track-speeds L37-44)。実行: `kbb -M /tmp/f16.clj` (giemon deps.edn)。

```
:fwd-zero-width  Divide by zero 例外 (fail-closed 正常)
:inv-zero-width 例外なしで {:track/left 1.0 :track/right 1.0}
  (回転コマンド angular=1.0 rad/s が無音に捨てられ直進 speeds を返す;
   回転 0 なら直進 1.0 が無音に正しく見える — 検知不能な縮退)
:fwd-neg-width  #:twist{:linear 1.5, :angular -2.0}
  (width=+0.5 では :angular +2.0 — 負幅で符号無音反転)
:neg-rt-identical true
  (負幅でも往復変換は自己無矛盾 — 往復セルフチェックでは検出不能)
:pose-w+  {:pose/x 1.5, :pose/y 0.0, :pose/theta 2.0}
:pose-w-  {:pose/x 1.5, :pose/y 0.0, :pose/theta -2.0}
  (同一 track speeds + 幅符号 1 文字違いで統合 pose の theta が +2.0 ↔ -2.0)
:fwd-nan-width  #:twist{:linear 1.5, :angular ##NaN}
:fwd-nan-speeds #:twist{:linear ##NaN, :angular ##NaN} (例外なし)
:fwd-inf-speeds #:twist{:linear ##Inf, :angular ##NaN} (例外なし)
:tr-nan         ##NaN (turning-radius が NaN を無音返却)
:ip-nan-pose    NaN pose が integrate-pose を例外無しで伝播 (falsify-14/15 同型)
:ip-neg-dt      dt=-1.0 は過去への積分として「正常動作」(符号検査なし —
  時間反転が無音通過、DR で dt の符号が破損しても検出されない)
```

読み取り:

- `twist->track-speeds` は `track-width` の **符号・有限性を一切検査しない**。
  負幅は角速度の向きを無音反転させ、かつ往復変換が自己無矛盾なため
  `fwd∘inv` セルフチェックでも検出不能 (`:neg-rt-identical true`)。
  幾何 (左右トレッド配置) の破損が制御出力 (統合 pose の theta ±2.0 rad) に
  直接流出する。
- 逆関数だけが零幅で fail-open: 回転コマンドを無音に捨てて直進 speeds を
  返す (前方変換は `Divide by zero` で fail-closed)。同一 track-width
  契約の正逆関数が非対称で、ピボット命令が直進として実行され得る。
- `##NaN`/`##Inf` は falsify-11/14/15 と同一クラスの非有限素通り
  (`turning-radius` `##NaN` → `##NaN` 返却、`integrate-pose` NaN 伝播)。
- 対照 (fail-closed): `fwd` の零幅は例外、`(== left right)` の直進 nil は
  仕様どおり正常。

## verdict: **refuted** (負幅の無音符号反転 + 逆関数零幅の回転コマンド無音破棄 + 非有限素通りの 3 面を実測)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb -M -e '(require (quote [kotoba.giemon.chassis :as ch]))
(prn :neg-width (ch/track-speeds->twist -0.5 1.0 2.0))
(prn :zero-width-inv (ch/twist->track-speeds 0.0 0.0 1.0))'
;; => :neg-width #:twist{:linear 1.5, :angular -2.0}
;;    :zero-width-inv #:track{:left 0.0, :right 0.0}  (回転命令が消える)
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-16 実測 — chassis track-drive の `twist->track-speeds`
は `track-width` を無検査で、負幅は `:twist/angular` の符号を無音反転
(往復変換は自己無矛盾でセルフチェック不能、統合 pose の theta ±2.0 rad
に直流出)、零幅の逆変換は回転コマンドを無音に捨てて直進 speeds を返す
(前方変換は例外で fail-closed、非対称)。修理: 両関数の track-width 入口で
`(pos? width)` かつ `Double/isFinite` 検査 (負/零/非有限は例外化) +
`integrate-pose` の `dt` 有限性検査 + speeds の `Double/isFinite` 検査
(falsify-11/14/15 の有限性検査と同一修理箇所)。
