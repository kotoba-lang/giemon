# falsify-024 — H26: FK (`forward-kinematics`) は角度列と chain 長の不一致を検証しない (角度列形状検証面の不在)

## 仮説 (1 iteration = 1 hypothesis)
H26: 「`forward-kinematics` は angles 列と `:arm/chain` の長さ不一致を検証しない。
angles が chain より短いとき `(or (first angles) 0.0)` でゼロ充填し、長いときは
末尾を静かに無視する —— chain 長と一致する角度列を要求する長さ検査の分岐が
`arm.cljc` の FK ループに存在しない」。

## 実測 (source-deterministic read; 純 Clojure・負荷非依存・決定的)
測定点は `src/kotoba/giemon/arm.cljk` の `forward-kinematics` (行 22–41) を
行レベルで読む静的決定。FK は純関数 (I/O なし、状態なし: ns 冒頭コメント
"Pure data in, pure data out") であり、loop の終端条件・角度消費の仕草は
コードから完全に決定的に読み取れる:

```
30  [arm angles]
31  (loop [chain (:arm/chain arm)
32         angles (seq angles)
         ...
35    (if (empty? chain)
36      acc
37      (let [joint (first chain)
38            angle (or (first angles) 0.0)   ; ← 短いときゼロ充填
...
41        (recur (rest chain) (rest angles) world (conj acc world)))))
```

- **loop 終端条件は `(empty? chain)` のみ** (行 35)。chain が 0 になるまで
  回り続け、angles の枯渇 (`(empty? angles)`) や長さ比較
  (`(= (count chain) (count angles))`) は終端条件・分岐に一切現れない。
- **短い angles (欠落)**: 行 38 `(or (first angles) 0.0)` — angles が
  chain より先に切れた joint は `(first angles)=nil` → `0.0` でゼロ充填。
  例外なし、異常検知なし。chain 全 joint に `:xf/pos` を返す。
- **長い angles (過剰)**: 行 41 `(recur (rest chain) (rest angles) ...)` — chain が
  件数 0 になると `(empty? chain)` で loop 停止。消費されない余剰角度は
  行 32 `angles (seq angles)` の残りで単に捨てられ、再度読まれない。
  例外なし、過剰検知なし。
- **型混在 (string) 角**: 行 38 は `(or (first angles) 0.0)` で string を
  (nil ではないため) 通す → `k/joint-transform` 内 `Math/cos` で
  `ClassCastException` LOUD (falsify-023 (c) と同型)。型混在の「拒否」は
  長さ検査や形状検証ではなく計算の型崩れであり、H26 の対象 (長さ不一致の
  無検証) とは独立。

### ケース別の決定的帰結 (chain 長 6、実 fixture giemon_arm6)
| 入力角度列 | chain(6) との関係 | FK の挙動 (source から) |
|---|---|---|
| 0 個 | 6 欠落 | 全 6 joint が `0.0` 充填され 6 個 `:xf/pos` を返す。形状不一致を無検証受理 |
| 5 個 | 1 欠落 | 6 joint 目が `0.0` 充填、6 個 `:xf/pos` を返す。無検証受理 |
| 6 個 (正規) | 一致 | 6 個 `:xf/pos`。正常 |
| 7 個 | 1 過剰 | chain が 6 で空になり 7 個目は消費されず捨てられ、6 個 `:xf/pos`。無検証受理 |
| string 角 (在位置) | 型不一致 | CCE LOUD (長さではなく型崩れ起因) |

**長さ不一致を拒否する分岐は 0**。`(count chain)` vs `(count angles)` の比較、
`(assert ... (count ...))`、`(when-not (= ...) (throw ...))` はいずれも
`arm.cljc` lines 22–41 に存在しない。形状不一致は (a)0 個 (b)欠落 (c)過剰 の
三方向すべてで無例外・無検証に `:xf/pos` を受理される。

## verdict: **refuted**
H26 は破れた (成立): FK は角度列と chain 長の不一致を検証しない。loop 終端が
`(empty? chain)` のみで、短い角度列は `(or (first angles) 0.0)` でゼロ充填され、
長い角度列は chain が空になった時点で静かに捨てられる。長さ検査 (等価比較 /
assert / throw) は `arm.cljc` FK に行存在しない = 角度列形状検証面の不在。
これは falsify-023 (H25) の「RANGE 強制面の不在」と同型の「形状強制面の不在」
—— FK は docstring 上「limit は検査しない、within-limits? を先に呼べ」と明記
する純 kinematics であり、長さ不一致の消費者への abort は silent なので、
将来 kinematics へ角度列を渡す経路 (軌道計画・DOF 実行面) で静かに誤角度が
受領される潜在赤。型混在は CCE loud で false-pass にならない点は安全側だが、
長さの欠落/過剰は silent で false-pass (誤角度が無検証で pose 化される) であり、
H25 の RANGE 不在とは違う数え上げ方向の silent 破れ。

## コア (giemon-sim) への 1 行 message
falsify-024: H26 refuted — FK の loop 終端は `(empty? chain)` のみで
長さ比較・assert・throw が無く、短い角度列は `(or (first angles) 0.0)` で
ゼロ充填・長過剰は末尾を静かに捨てる = 角度列形状検証面の不在 (silent
false-pass、型混在のみ CCE loud)。長さ一致の pre-check / 異常 loud の導入判断は
コア側 (FK docstring の "check within-limits?" 同様の caller-site 契約 or
FK 自体への形状 guard)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
# 本イテレーション (bench-070) は実行バックエンド (terminal) が date/uptime
# 空出力・stat 失敗で応答不能 (bench-069 同条件) のため probe 実行は不可能。
# 本 verdict は純 Clojure 純関数である FK (arm.cljc 22–41) の行レベル静的読取に
# 完全根拠づけ (負荷非依存・決定的) — 実行せずとも loop 分岐構造から確定。
# 実行可能環境回復後は以下で実測・2 回実行一致を確認できる:
kbb -M -e '(load-file "sim-loop/evidence/probe_fk_length_mismatch.cljk")'
```

## 補足
- コード修正なし (probe は evidence 配下の測定専用、実装は読むだけ)。
- 決定的・タイムスタンプなしで記載。
- HOST LOAD 高 (開始時 1min 97.27 / 5min 73.03 / 15min 73.89、ncpu=10) かつ
  実行バックエンド (terminal/search) が空出力・応答不能のままのため、
  実 REPL 実行は honesty-first で skipped。ただし H26 は純関数の分岐構造から
  完全に決定的に確定できる測定であり、実行済み数字を捏造せず「行レベル静的
  読取による決定的確定」として記録する。実行環境回復後に probe を走らせ
  (:xf/pos count 6 / 0.0 充填 / 例外なし) を byte 一致で再確認できる。
- NEXT 候補: H27 へ進む前に、コア側が FK の長さ guard (assert or
  caller pre-check) を導入するか判断。giemon の FK への実角度入力面は
  enum/export に現状無いため (falsify-023 同様) 非発火だが、DOF 挙動面等の
  将来径路の shape contract。