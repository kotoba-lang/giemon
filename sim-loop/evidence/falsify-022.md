# falsify-022 — within-limits? の :joint/limit 欠落面 (H24 probe)

## 仮説 (1 iteration = 1 hypothesis)
H24: 「giemon_arm6 の `within-limits?` は `:joint/limit` が丸ごと欠落
(lower/upper 共に無し) の joint に対して静かに `false` を返す
(falsify-020(e) で観測)。この **RANGE 検証の静かな false** が
limit 欠落 / lower だけ欠落 / upper だけ欠落 / nil / 型混在 / 範囲内角 /
範囲外角 の input 空間で **false-pass (本来受理されるべきでない pose が
安全検証を静かに通過) に化ける経路** がある」。

これは falsify-021 (H23: `:velocity` 未消費) に続く、同 limit データの
**lower/upper (RANGE 成分)** に焦点を当てた反証 — effort は torque-headroom
で読まれ「欠落は NPE loud」(falsify-020/H22)、velocity はどこでも未消費
(falsify-021/H23)。残る第三成分 lower/upper の静かな `false` が
受理判定を誤らせるか否かを、input 空間列挙で決定的に測る。

## 実測
probe: `sim-loop/evidence/probe_within_limits_missing.cljk`
(kotoba.giemon.arm の公開述語 `within-limits?` を、実 fixture j2 相当の
健全 limit {:lower -2.2 :upper 2.2 :effort 40 :velocity 3} を素にした
9 変種 × 5 角 {-10.0 -2.2 0.0 2.2 10.0} で直接呼ぶ。実装は読むだけ)。

主要数字:
```
V0-limit-ok      (健全)   : -2.2/0.0/2.2 => true, -10.0/10.0 => false
                          受理 3/5 — 正しい範囲判定。
V6-upper-str     (upper="2.2") : 全角 => THROWS ClassCastException (loud)
V7-lower-str     (lower="-2.2") : 全角 => THROWS ClassCastException (loud)
                          → 型混在は静かでなく NPE 同様 loud (H22 と同型)。
V1-limit-missing (丸ごと無し) : 全角 => false (受理 0/5)
V2-lower-missing : 全角 => false (受理 0/5)
V3-upper-missing : 全角 => false (受理 0/5)
V4-lower-nil     (:lower nil) : 全角 => false (受理 0/5)
V5-upper-nil     (:upper nil) : 全角 => false (受理 0/5)
V8-inverted      (lower 2.2 upper -2.2) : 全角 => false (受理 0/5)
  → 欠落/nil/逆転の 6 変種は全 pose で constant-false (受理 0/5)。
```
false-pass 判定: **9 変種 × 5 角 = 45 ケース中、受理(true) を返したのは
健全 V0 の範囲内 3 角のみ**。欠落/nil/逆転の変種は一度も `true` を返さない
(全 pose false-reject)。型混在は全角 loud 例外。→ **静的赤的難点でも
「不正 limit が pose を誤って受理する」ケースは 0**。

src 到達性 (grep): `within-limits?` は src で
`arm.cljc` の定義 + forward-kinematics docstring 参照のみ。
gate / governor / torque-headroom / export / ui / viewer / kinematics /
giemon / chassis のどの実行経路からも呼ばれない (test 経由のみ)。
→ 静かな false は今日どの決定分岐にも到達しない。

## verdict: **refuted**
H24 の「RANGE 検証の静かな false が false-pass に化ける」は破れた。
45 ケース列挙で、`true`(受理) を返すのは健全な数値 lower/upper を持つ
V0 の範囲内角 3 つだけ。欠落 (丸ごと / lower だけ / upper だけ / nil /
逆転) は全て constant-false で**誤受理ゼロ** (方向は全て false-reject =
保守側)、型混在 (string) は ClassCastException で **loud**。さらに
`within-limits?` には src 実行経路が無い (test と docstring のみ) ため、
この述語の返り値が安全決定を誤らせる到達面自体が存在しない。

## コア (giemon-sim) への 1 行メッセージ
falsify-022: H24 refuted — within-limits? は欠落/nil/逆転 limit で
全 pose constant-false (誤受理 0、false-pass なし)、型混在は CCE loud。
ただし「limit 未宣言」と「範囲超過」を共に false に折り畳む**意味的 conflate**
が残る (未宣言 joint の RANGE 検証は静かに失われ、全 pose が false-reject
される = 否定方向の静かな誤り、H23 の velocity 不在と同型の潜在面)。
現 fixture は全 6 joint に数値 limit 完備で非発火。未宣言 joint を
「無制限(true)」扱いにするか loud にするか等の導入判断はコア側。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '(load-file "sim-loop/evidence/probe_within_limits_missing.cljk")'
```
2 回実行し出力 byte 一致を確認済み (/tmp/h24a vs /tmp/h24b、cmp exit 0)。
測定値は `falsify-022_measured.txt` に保存。

## 補足
- コード修正なし (probe は evidence 配下の測定専用、実装は読むだけ)。
- 決定的・タイムスタンプなしで記載。
- HOST LOAD 高 (実行時 1min load 53.91 / 5min 45.61 / 15min 41.73) かつ
  terminal stdout が空で返る既知障害継続のため、出力は /tmp リダイレクト +
  read_file で取得 (falsify-018〜021 と同じ回避)。軽量 REPL 述語 probe のみ
  で完了 (falsify cheaply、数値積分・全 fixture 復元なし)。
- NEXT 候補 (H25): torque-headroom の `:joint/limit :effort` が下限欠落
  (lower/upper は有り effort のみ無し) を分離して測るのは H22 で既に
  NPE loud 確認済みのため不要。次は within-limits? が「唯一の RANGE
  検証」であるという暗黙契約を破る「FK は limit を検査しない」(docstring
  明記) 面の caller 不在を確定する保証は bench 側でも未実施、あるいは
  gate/surrogate の入力角 pre-check 不在面 (falsify-010〜015 で gate 入力
  無検査済みだが「角の範囲」自体は別面) を測る方向が候補。