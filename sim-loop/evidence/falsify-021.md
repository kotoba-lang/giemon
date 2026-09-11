# falsify-021 — `:joint/limit :velocity` 消費面 (H23 probe)

## 仮説 (1 iteration = 1 hypothesis)
H23: 「giemon_arm6 の `:joint/limit :velocity` は angular (rad/s) として解釈され、
joint の速度制限 (変化率) が FK・gate・surrogate の安全検証の『別の安全面』として
どこかで消費される。velocity 値の欠落 / 型混在 / 範囲外はその面に何らかの
決定的な影響 (許可変化・例外・false-pass) を及ぼす」。

これは falsify-020 (H22: `:joint/limit :effort` 欠落面) の対抗面 —
effort は torque-headroom / underrated-joints / bom で単一消費源として読まれる一方、
同 limit に同居する `:velocity` 成分が「位置 FK と torque 検証のどちらにも
読まれないまま残る」別の安全面になっている可能性を測る。

## 実測
probe: `sim-loop/evidence/probe_velocity_limit_consumption.cljk`
(実 fixture giemon_arm6.edn を reconstitute-arm で復元し、j2 の
`:joint/limit` を 4 種 {velocity=3(実値) / velocity 欠落 / velocity="high"(型混在) /
velocity=1000(範囲外)} に差し替え、全公開決定関数の出力を pr-str で byte 比較。
実装は読むだけ、コード修正なし)。

主要数字:
```
実 fixture: 全 6 joint に :joint/limit :velocity あり
  j1=3 j2=3 j3=3 j4=4 j5=4 j6=5  (URDF <limit velocity=.../> と一致)

V0(velocity=3)   / V1(欠落) / V2("high") / V3(1000):
  within-limits?  j2 at 2.2 => true / true / true / true
  within-limits?  j2 at 0.0 => true / true / true / true
  FK j2 の upper=2.2 姿勢 :xf/pos => 完全一致 (4 変種で byte 同一)
  FK end-effector :xf/pos    => 完全一致
  torque-headroom             => 完全一致 (6 行、headroom 0/0/10/6/0/2.3)
  underrated-joints           => () 完全一致
  bom :all-qdd モデル列        => 完全一致

V1-idx-vs-V0 = true, V2-idx-vs-V0 = true, V3-idx-vs-V0 = true
  → :joint/limit :velocity の値を {3, 欠落, "high", 1000} と振っても
    FK / within-limits? / torque-headroom / underrated / bom の
    全出力が byte 不変 (velocity はどこからも消費されない = inert)。

src ソース byte 検査 (cljc 全 8 ファイル):
  arm / kinematics / governor / export / ui / viewer / giemon => "velocity" 不含有
  chassis => true (車両ドライブ twist 文書文字列のみ、joint limit とは無関係)
```

決定的確認: 同一 probe を 2 回実行 (/tmp/v21a vs /tmp/v21b)、RUN マーカー行正規化後、
probe 出力部 (先頭 12 行) を cmp → exit 0 (byte 一致)。測定値は
`falsify-021_measured.txt` に保存。

到達性: 現 fixture (giemon_arm6) は 6 joint すべてに `:velocity` 値あり + parity 一致。
しかし**消費する関数が存在しない**ため、実 fixture をどう編集しても
FK / gate / surrogate / torque の決定は velocity に無関係 (到達面自体が無い)。

## verdict: **refuted**
「`:joint/limit :velocity` が angular (rad/s) として解釈され安全検証の
別面として消費される」という仮説は破れた。velocity は
FK (`forward-kinematics` は joint 角度のみ、速度入力面なし)・
`within-limits?` (lower/upper のみ)・`torque-headroom` (effort + cont-nm のみ)・
`bom` (actuator のみ)・gate (rob 安全クラスのみ) のどこにも読まれない —
**速度制限を強制する面は存在しない**。値の欠落/型混在/範囲外も出力を
一切変えない (H22 の effort 欠落 = NPE loud とは非対称で、velocity は
例外も false-pass も起こさず静かに無視される)。

安全面の帰結: 速度制限 (rad/s) は宣言データとしては EDN/URDF 両方に
存在して parity は守られるが、**実行経路で強制されない潜在赤**。
ただし現 arm API は joint 角度 (位置) しか受け付けず速度入力面自体が無いため、
現 fixture・現関数経路では利用不能 (H19/H20/H21 と同型の潜在契約破れ)。
gate の `:action/:params` は無検査でも (falsify-010〜015) giemon 側に
速度を消費する関数が無いため、速度超過はどの経路でも検出もされなければ
許可もされない — 純然たる「不在の安全面」。

## コア (giemon-sim) への 1 行メッセージ
falsify-021: H23 refuted — `:joint/limit :velocity` は FK/within-limits?/
torque-headroom/bom/gate のどこにも読まれない (src 8 cljc 中 chassis 文書のみ言及)、
値 {3/欠落/"high"/1000} で全出力 byte 不変。速度制限の強制面が存在しない
潜在赤 (現 API に速度入力面なし、effort 欠落の NPE loud とは非対称)。
速度安全面を扱う場合は FK/線形ソルバ側に速度消費層の導入要否を判断のこと。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb -M -e '(load-file "sim-loop/evidence/probe_velocity_limit_consumption.cljk")'
```
2 回実行し RUN マーカー正規化後の出力一致を確認済み (/tmp/v21a vs /tmp/v21b、
probe 出力部 cmp exit 0)。

## 補足
- コード修正なし (probe は evidence 配下の測定専用、実装は読むだけ)。
- 決定的・タイムスタンプなしで記載。
- HOST LOAD 中 (実行時 load 約 8.6〜11.4) かつ terminal stdout が空で返る
  既知障害継続のため、出力は /tmp リダイレクト + read_file で取得 (既知回避)。
  REPL 数値 probe のみで完了 (falsify cheaply、数値積分なし)。
- NEXT 候補 (H24): falsify-020(e) で言及した `within-limits?` の
  `:joint/limit` 丸ごと欠落 (lower/upper 共に無し) が false で静かに通る
  RANGE 検証の別面を、input 空間列挙 probe で決定的に測る。