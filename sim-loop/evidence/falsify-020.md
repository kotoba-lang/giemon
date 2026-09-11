# falsify-020 — torque-headroom の :joint/limit 欠落面 (H22 probe)

## 仮説 (1 iteration = 1 hypothesis)
H22: 「`kotoba.giemon.arm` の `torque-headroom` / `underrated-joints` は、
joint の `:joint/limit :effort` が欠落している
(limit に :effort キー無し / :joint/limit 丸ごと無し / :effort nil) 場合に、
`:torque/required nil`・`:torque/headroom nil` を生成し、
`underrated-joints` の `neg?` フィルタ (:when) を素通りさせて
**false-pass になる** (H19 の normalize アンダーフロー零分岐誤判定と並ぶ
第 3 面)」。

これは falsify-019 (H21: actuator 欠落 = 静かな false-pass) の対抗面 —
actuator が無い joint は静かに消える一方、**limit が無い joint** が
「required/headroom = nil ⇔ 余裕無限大」として安全側誤判定される
可能性を測る。

## 実測
probe: `sim-loop/evidence/probe_missing_limit_skip.cljk`
(in-memory EDN で kotoba.giemon.arm / export / ui を直接呼ぶ、実装は読むだけ)。

主要数字:
```
(a) j2 limit {lower upper} NO :effort  (actuator あり):
  torque-headroom  => THROWS: NullPointerException
    "Cannot invoke \"Object.getClass()\" because \"x\" is null"
  underrated-joints => THROWS: NullPointerException (同)
  → 「required nil→headroom (- 40 nil)」は nil では返らず、
    (- 数 nil) が NPE で loud に落ちる。false-pass しない。

(b) j2 :joint/limit 丸ごと無し (actuator あり):
  torque-headroom => THROWS: NullPointerException (get-in が全 nil)
  underrated-joints => THROWS: NullPointerException

(c) j2 limit に :effort nil (明示 nil):
  torque-headroom => THROWS: NullPointerException
  underrated-joints => THROWS: NullPointerException
  → 欠落・nil で非対称ではない: nil でも NPE (loud)。
    falsify-019 の actuator 欠落 (静か) とは**逆**の挙動。

(d) control (全 joint 有効、j2 を 40 vs 10 に under-rate):
  underrated-joints => [{:joint/name "j2" :torque/required 40
                          :torque/rated 10 :torque/headroom -30}]
  → 検出機構は健全。NPE は limit 欠落面にのみ発火する。

(e) within-limits? の limit 欠落面:
  no-limit j2 at 0.0  => false (しれっと範囲外扱い、throw せず)
  no-effort j2 at 0.0 => true  (lower/upper が残っていれば正常)
  → within-limits? は :effort を見ないので(a)(b)の赤には無関係。
    ただし no-limit (lower/upper も欠落) は false で through。
    (RANGE 検証の静かな false — 別面、本 H の射程外として言及のみ)

(f) bom (all-qdd) on no-limit arm => nil
  → nil はフィールド欠落ではなく :arm/realization が無いため。
    実 fixture では realization 有りで bom は actuator だけを読む
    (limit 非読) なので：(limit 欠落は bom に伝播しない)。

(g) export/ui への伝播 (H22 の射程):
  export torque->csv   on no-effort arm => THROWS: NPE (loud)
  export torque->json  on no-effort arm => THROWS: NPE (loud)
  ui torque-table      on no-effort arm => THROWS: NPE (loud)
  → torque 出力面 (csv/json/ui) は arm/torque-headroom を直接呼ぶため、
    NPE がそのまま伝播。limit 欠落は audit 出力を汚染せず、**loud に失敗**。
    静かに欠落行として出ることはない。
```

決定的確認: 同一 probe を 2 回実行 (/tmp/f20a vs /tmp/f20b)、
RUN 番号マーカー行を正規化後 cmp 一致 (exit 0、probe 出力行は byte 一致)。

到達性: 現 fixture (giemon_arm6) は全 6 joint に
`:joint/limit {:lower ... :upper ... :effort ...}` が揃っており顕在化しない。
赤ではなく **H22 は実測上 survived** (loud 失敗で安全側)。

## verdict
**survived** — H22 の「limit 欠落は required nil ⇔ 余裕無限大で
false-pass になる」は破れなかった。
`:joint/limit :effort` 欠落 / `:joint/limit` 丸ごと欠落 / `:effort nil` の
いずれも `torque-headroom` は `(- :cont-nm nil)` で NullPointerException を
throw し、`underrated-joints` / export(csv/json) / ui(table) へ loud に伝播する。
limit 欠落面は trajectory-wise で安全側 (失敗 loud / 検証不能)。
falsify-019 (H21: actuator 欠落) の「静かなスキップ」とは明確に非対称 —
actuator 欠落のみが false-pass 母集団脱落の危険面であり、limit 欠落は NPE で
守られている。

## コア (giemon-sim) への 1 行メッセージ
falsify-020: H22 survived — torque-headroom は `:joint/limit` が
欠落/:effort nil だと `(- cont-nm nil)` で NullPointerException を throw
(underrated-joints・export csv/json・ui table とも loud 伝播、false-pass なし)、
actuator 欠落(H21)のみが静かな検証脱落の危険面。修理要は H21 側に集中。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb -M -e '(load-file "sim-loop/evidence/probe_missing_limit_skip.cljk")'
```
2 回実行し RUN マーカー正規化後の出力一致を確認済み (/tmp/f20a vs /tmp/f20b、
cmp exit 0)。

## 補足
- コード修正なし (probe は evidence 配下の測定専用、実装は読むだけ)。
- 決定的・タイムスタンプなしで記載。
- HOST LOAD 高 (load 約 49〜57) かつ terminal stdout が空で返る既知障害継続の
  ため、出力は /tmp リダイレクト + read_file で取得 (falsify-018/019 と同じ回避)。
  軽量 REPL 数値 probe のみで完了 (falsify cheaply、数値積分なし)。
- within-limits? の no-limit (lower/upper 全欠落) が false で通過する件は
  RANGE 検証の別面のため、本 H の verdict に含めず言及のみとした
  (将来 probe 候補)。