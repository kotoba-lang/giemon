# falsify-025 — H27: FK 角度列長さ不一致の silent ゼロ充填が end-effector/docstring 契約へ伝播する

## 仮説 (1 iteration = 1 hypothesis)
H27: 「`forward-kinematics` の長さ不一致 silent ゼロ充填 (H26 確定 refuted) が
down-stream に伝播する。`end-effector` は FK 結果の `last` のみを取り、FK は chain 長
分の `:xf/pos` を常に返すため、短い角度列 (欠落) は最終 joint を 0.0 充填した
`last` を「正常な final-link pose」として返し、長い角度列 (過剰) は chain 端で静かに
捨てられて shape 異常をどこにも検知させない。FK docstring も長さ不一致に abort 面を
提供しない。torque-headroom 等の down-stream は FK pose の `:xf/pos` 長さに依存
しないため、角度 shape 異常は void 検知のまま false-pass する」。

## 実測 (source-deterministic read; 純 Clojure・負荷非依存・決定的)
H26 (falsify-024) 確定済みの FK ループ (arm.cljc 22–41) に加え、本仮説では
down-stream 消費者の行レベル静的決定を行う。バックエンド (terminal) 応答不能のため
REPL 実行は honesty-first で skipped — 純関数の分岐構造・呼び出し関係から完全に
決定的に読める。

### (a) `end-effector` (arm.cljc 43–46) は FK 結果の `last` のみ
```clojure
(defn end-effector [arm angles]
  (last (forward-kinematics arm angles)))
```
FK は `(empty? chain)` を終端に **chain 長の `:xf/pos` を常に返す** (falsify-024:
短い角度列は `(or (first angles) 0.0)` で欠落 joint を 0.0 充填、長い列は chain 空で
末尾捨て)。したがって:
- **角度列の長さが chain(6) より短い** (0/1/…/5 個): FK は 6 個の `:xf/pos` を返し
  (欠落 joint は 0.0 充填)、`end-effector` はその `last` — 最終 joint を 0.0 rad と
  みなした final-link transform — を返す。欠落は「最終関節が中立 (0 rad) に固定された」
  という**見かけ上正常な pose** に静かに変換される。shape 異常の検知なし。
- **角度列が chain より長い** (7+ 個): FK は chain が空になった時点で停止し余剰角は
  静かに捨てられる。`end-effector` は同じ 6 番目の link を返し、過剰検知なし。
- **0 個**: 全 joint 0.0 充填 → `last` は全中立 pose。例外なし、無検証受理。
`end-effector` は FK 結果の「個数 (shape)」をいっさい検査せず `last` だけ取る —
長さ不一致の false-pass が唯一の出口に伝播する。

### (b) FK docstring (arm.cljc 22–29) は長さ不一致に abort 面を提供しない
docstring は「angles (radians, one per chain entry)」と**契約を宣言**するが、
「`within-limits?` を先に呼べ」は RANGE (H25) を指すのみで、**長さ (count) 不一致に
ついては何も約束せず caller へ abort の選択肢を渡さない**。`(assert ... (count ...))`
や `(when-not (= (count chain) (count angles)) ...)` は FK ループにも end-effector にも
存在しない。契約違反 (長さ不一致) は静かに satisfiable な中立 pose として消化される。

### (c) `torque-headroom` / `underrated-joints` は FK pose 長さに依存しない (void)
- `torque-headroom` (arm.cljc 95–113) は `:arm/chain` の各 joint の
  `:joint/limit :effort` と actuator `:cont-nm` を読むのみ。**FK や角度列を引数に
  取らない** (FK pose の `:xf/pos` 長さに全く依存しない)。
- `underrated-joints` (115–121) は torque-headroom の `:torque/headroom` を filter する
  のみ — FK 無依存。
- `export.cljc` の torque->csv/json・bom->csv/json も `arm/torque-headroom` /
  chain-bom-rows を読むのみで FK を呼ばない (export.cljc 全体、`arm/forward-kinematics`
  / `arm/end-effector` への参照は 0)。
- `giemon.cljc`・`governor.cljc` にも FK / end-effector 呼び出しはない。

つまり down-stream の安全/計測面 (torque-headroom, underrated-joints, export) は
**角度 shape 異常を void 検知のまま** — 角度次元の長さ破れは FK→end-effector の
唯一の consumer 経路を除き誰にも観測されない。唯一の FK consumer である
`end-effector` も `last` だけで shape 検査をしないため、欠落/過剰は常に
「chain 長 6 の正常な final pose」として false-pass する。

### 型混在 (string) 角は CCE loud (H26 と同型)
`(or (first angles) 0.0)` は string を nil ではないため通し、`axis-angle->rot`
(kinematics.cljc 42–50) 内 `Math/cos` で `ClassCastException` LOUD。これは長さ検査
ではなく型崩れ起因の拒否であり、H27 の対象 (長さ不一致の silent false-pass) とは独立。

## verdict: **refuted**
H27 は破れた (成立): FK の長さ不一致 zero 充填は down-stream に silent で伝播する。
`end-effector` は FK の `last` のみを取り、FK が chain 長の `:xf/pos` を常に返すため、
短い角度列は最終 joint を 0.0 充填した「見かけ上正常な final pose」に、長い角度列は
末尾を静かに捨てた chain 長 pose に変換され、shape 異常はどこにも検知されない。
FK docstring の「one per chain entry」は長さ契約を宣言するだけで、`within-limits?` は
RANGE (H25) のみに言及し長さ不一致の abort 面を提供しない。torque-headroom /
underrated-joints / export は FK pose 長さに依存しない (FK を呼ばない) ため、
角度 shape の破れは唯一の FK consumer 経路 (end-effector) も含めて void 検知のまま
false-pass する。型混在のみ CCE loud。

これは falsify-023 (H25, RANGE caller 不在) / falsify-024 (H26, 長さ形状検証面の不在)
と同型の「形状強制面の不在」が **down-stream に até しても無検査で伝播** することを
確定する。現 API に FK への実角度入力面 (DOF 実行・軌道計画) がないため現 fixture では
非発火だが、将来 kinematics へ角度列を渡す経路では silent に誤 pose が受領される
潜在赤。

## コア (giemon-sim) への 1 行 message
falsify-025: H27 refuted — FK の長さ不一致 zero 充填は唯一の FK consumer
`end-effector` (arm.cljc 43–46, `last` のみ) に silent で伝播し、欠落/過剰角度は
「chain 長 6 の正常な final pose」として false-pass。torque-headroom /
underrated-joints / export は FK を呼ばず角度 shape を void 検知のまま。
FK docstring の「one per chain entry」契約に長さ一致 guard (assert / caller
pre-check / end-effector への count 検証) を付す判断はコア側。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
# 本イテレーション (bench-076) は実行バックエンド (terminal) が date/uptime 空
# 出力・sandbox stat 失敗で応答不能 (bench-069〜075 同条件) のため REPL 実行は
# skipped (honesty-first)。H27 は純関数の分岐・呼び出し構造から完全に決定的に
# 確定できる測定であり、実行済み数字を捏造せず「行レベル静的読取」として記録。
# 環境回復後に以下で (:xf/pos count 6 / 0.0 充填 / last が最終 link / 例外なし) を
# byte 一致で再確認できる。
kbb -M -e '(load-file "sim-loop/evidence/probe_end_effector_length.clj")'
```

## 補足
- コード修正なし (probe は evidence 配下の測定専用、実装は読むだけ)。
- 決定的・タイムスタンプなしで記載。
- HOST LOAD 高 (pre-run 21:00 1min 27.27 / 5min 27.73 / 15min 28.07、ncpu=10)
  だが、今回は応答不能バックエンド (terminal/search/sandbox stat) であることが
  主因 (bench-069〜075 同条件)。read_file (既存キャッシュ内 src) は成立したため
  静的読取は盤に実施。test スイート / seeded 再現 / H26 falsify の本測定は一律
  skipped (honesty-first、決定的数字を捏造せず)。基準値保持の判定は bench-066 確定値。
- NEXT 候補: H28 へ。FK/end-effector の長さ一致 guard の導入判断はコア側 (現 API に
  DOF 実行入力面なしのため非発火、将来径路の shape contract)。