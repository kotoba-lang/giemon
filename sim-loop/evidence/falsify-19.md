# falsify-19 — 許可セットと `:action/safety` に同一の文字列 (非 keyword) が混入すると gate が無音 :permit、未知クラス文字列も検証されず通過

日時: cron iteration (JST 2026-09-04 14:2x, host load avg 約 43-54 / コア 10 → 軽量 REPL 測定のみ)

## 仮説

falsify-13 は gate 第 2 引数 (allowed-set) に **nil** が混入した場合を潰した。
未反証の隣接面は**非 keyword 値の文字列 face**: `rob/gate` は
`(set allowed-safety-classes)` 強制と `contains?` メンバーシップ以外に
値の型・正当性検査を一切持たない (robotics.cljc L124-129, pinned
1d1f93e)。`safety-classes` は `#{:none :low :medium :high :safety-critical}`
で keyword のみ (L26-29) だが、gate はこの集合を参照しない。ここで

1. 許可セットに文字列 `"low"` が混入し、action 側 `:action/safety` も
   文字列 `"low"` なら `:permit` に到達しないか
2. その際 `requires-sign-off?` (`human-sign-off-classes` は keyword
   `#{:high :safety-critical}` のみ) が文字列に対してどう振る舞うか —
   文字列 `"high"` がサインオフを迂回して permit まで行けないか
3. `safety-classes` に存在しない任意の文字列 (`"not-a-class"`) が
   両側一致すれば無音で通るか (gate は正規クラス集合を一切参照しない)

を測定する。action 側は rob/action 正規生成の `:action/safety :low` を
assoc で差し替えた半正規マップ (キー構造は正規) を使う。

## 実測

コード: robotics.cljc (gate L124-129 / requires-sign-off? L78-82 /
safety-classes L26-29)。実行: `kbb -M -e` (giemon deps.edn、
pinned robotics 1d1f93e3c9ac06ce475ebcfd4df1d908602792d5)。

```
(def raw (assoc (rob/action "op-s" "op-m-1" :actuate :low) :action/safety "low"))

:string-face       (rob/gate raw (conj #{:low :medium} "low"))
                   => {:gate/decision :permit, :gate/action "op-s"}      ← 赤
:permitted?        (rob/action-permitted? raw (conj #{:low :medium} "low"))
                   => true                                                ← 赤
:string-set-only   (rob/gate raw #{:low :medium})
                   => {:decision :deny, :reason :safety-class-not-allowed} (単独破損は fail-closed、falsify-13 と同型の組合せ条件)
:kw-action-str-set (rob/gate (rob/action "op-s2" "op-m-1" :actuate :low) #{"low" :medium})
                   => {:decision :deny, ...}                              (正規 keyword action は文字列セットに一致せず deny)
:never-validated   (rob/gate (assoc raw :action/safety "not-a-class") (conj #{:low :medium} "not-a-class"))
                   => {:gate/decision :permit, :gate/action "op-s"}      ← 赤: gate は safety-classes 正規集合を一切参照せず、
                                                                             未知クラス文字列も両側一致で permit
```

読み取り:
- gate は allowed-set と `:action/safety` の**型を検査しない**ため、
  両側に同一の非 keyword 値 (文字列) が入った構成では無音 `:permit` する。
  kind は actuating (`:actuate`) のまま — falsify-12 の kind×class 結合欠落と
  畳なって、文字列 safety の hardware actuate が gate を通る。
- `requires-sign-off?` は `human-sign-off-classes` (keyword のみ) への
  `contains?` なので文字列 `"high"` は false を返す — つまり上位クラスを
  文字列に落としてセット側も文字列化すれば **サインオフ要求自体を迂回
  できる構造** (今回実測は `:actuate :low` だが、`:safety "high"` 文字列 +
  `"high"` 含みセットなら L128 に引っかからず L129 の `:permit` に到達する
  ことが上記の同一コードパスから従う)。
- さらに gate は `safety-classes` 正規集合を一切参照しないため、
  存在しないクラス `"not-a-class"` でも両側一致で permit する。契約上
  「safety class メンバーシップで permit/deny を決める」は 5 つの正規
  クラスに対してのみ意味を持つはずで、これは無検査通過。
- 単独破損は fail-closed を維持 (文字列 action + keyword セット → deny、
  keyword action + 文字列セット → deny)。成立は falsify-13 と同じ
  **gate 入力 2 つの組合せ破損**で、nil face (falsify-13) の文字列版。
  rob/action は文字列 safety を生成不能 (`safety-classes` contains? で
  nil、fail-closed 済み) なので、action 側は assoc/生マップが必要。

## Verdict: refuted

`rob/gate` の allowed-set 除去検査 (falsify-13 修理案) は「nil のみ」
では不十分で、**非 keyword 値全般の除去 (または検出時例外) が必要**。
`(:action/safety a)` 側も keyword 以外 (nil 含む) を `:invalid` に落とす
検査がセットで必要。修理は falsify-13 と同一箇所 (gate L124-129) の
拡張: allowed-set の nil/非 keyword 除去 + safety 非 keyword の
`:invalid` 化 + (望むなら) gate 内の `safety-classes` 正規集合照合。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb -M -e '(require (quote [kotoba.robotics :as rob]))
(def raw (assoc (rob/action "op-s" "op-m-1" :actuate :low) :action/safety "low"))
(prn (rob/gate raw (conj #{:low :medium} "low")))'
;; => {:gate/decision :permit, :gate/action "op-s"}
```

## コアへの 1 行メッセージ

falsify-13 の修理案「allowed-set から nil を除去」では足りない — 非 keyword
値全般 (文字列 face 実測: 同一文字列の両側一致で `:actuate` が無音 permit、
未知クラス文字列も通過、サインオフ迂回の構造的余地あり) を gate 側で
型検査するまで未修理。
