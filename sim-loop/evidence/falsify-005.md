# falsify-005 — falsify-004 の「加速ランプで peak 120 が k≈1.04x で破れる」は probe 自身の次元誤り (I·α² vs I·α) に依存する

## 仮説 (1 iteration = 1 hypothesis)
H7: 「falsify-004 の破れ点 (宣言速度上限内の 0.1 s ランプで peak 120 が
k≈1.04x で破れる) は実効的な破れ点である」 — 反証対象は
**「j2 は宣言速度上限内・加速トランジェントでも realistic DR 質量倍率
(k ≲ 1.2, ±20%) で peak 120 を破れる」という falsify-004 の主張**。

falsify-004 の probe (`probe_j2_limit_vel.py` L31) は慣性トルクを
`inert = k*I*alpha*alpha` と計算していた。トルクの次元は N·m = kg·m²·rad/s²
であり、正しくは `inert = k*I*alpha` (I·α)。I·α² は rad を無次元としても
kg·m²·rad²/s⁴ となり N·m ではない。本 probe
(`probe_j2_ramp_family.py`) は同一の点質量 worst-case モデルで
2 形式 (squared / linear) を並列測定し、ランプ時間族
(0.02–2.0 s) 全体で peak/cont の破れ点 k を再計測する。

## 実測 (probe_j2_ramp_family.py、fixtures/giemon_arm6 の質量/ジオメトリを verbatim 使用)
```
tau0=3.40 Nm  I=0.1215  I_distal=0.1175 kg m^2  coeff_dyn(w=3,3)=3.17 (コリオリ+遠心)

 ramp_s   alpha | k_peak(I·α² 形式) k_peak(I·α 形式) | k_cont(I·α 形式)
   0.02   150.0 |       0.04            4.84        |      1.61
   0.05    60.0 |       0.27            8.65        |      2.88
   0.10    30.0 |       1.04           11.74        |      3.91
   0.15    20.0 |       2.17           13.33        |      4.44
   0.20    15.0 |       3.54           14.29        |      4.76
   0.30    10.0 |       6.41           15.40        |      5.13
   0.50     6.0 |      10.96           16.43        |      5.48
   1.00     3.0 |      15.65           17.29        |      5.76
   2.00     1.5 |      17.52           17.76        |      5.92

I·α (正しい形式) では k=1.2 は走査した全ランプ時間 (≥0.010 s) で peak 120 未達。

alpha=30 (0.1 s ランプ) の慣性項比較:
  inert(I·α² 形式) = 109.4 Nm   ← falsify-004 の total 115.9 の主成分
  inert(I·α  形式) =   3.6 Nm
  total(k=1, I·α 形式) = 10.2 Nm → peak 破れなし (falsify-004 記載の 115.9 は 11 倍過大)
```

- falsify-004 の「total 115.9 N·m (k=1)」「peak 120 が k≈1.04x で破れ」は
  すべて I·α² 誤りに起因する数値であり、正しい I·α 形式では
  **同一条件 (0.1 s ランプ) で k_peak ≈ 11.74x** になる。
- 正しい形式での実効的な cont 40 破れ点はランプ時間依存で
  k ≈ 1.61x (0.02 s ランプ) – 5.92x (2 s ランプ)。±20% DR (k=1.2) では
  0.02 s ランプでも peak は破れないが、**cont 40 は 0.02–0.05 s ランプ
  (α ≈ 60–150 rad/s²) で k ≈ 1.6–2.9x に下がる** — こちらは
  モデル形式によらない残った赤 (ただし 0.02 s ランプは実効性が要検証)。

## verdict
- H7 (falsify-004 の k≈1.04x は実効的な破れ点): **refuted** —
  falsify-004 の peak 破れは probe 自身の慣性トルク次元誤り
  (`I*alpha*alpha`、正しくは `I*alpha`) の帰結。宣言速度上限内の
  加速トランジェントで realistic DR k (≈1.2) が peak 120 を破れる
  主張は撤回される。j2 の破れ点は falsify-002/003 の
  k≈9.8–11.6x 帯に戻る (peak, 宣言範囲内)。
- falsify-004 の evidence 自体は修正しない (記録は累積。本ファイルが
  撤回を記録する)。maturity 軸 5/6 の根拠のうち
  「0.1 s ランプ worst-case で peak 120 が k≈1.04x」の記述は
  本 evidence により無効化される。
- 残った赤: cont 40 に対する短ランプ (0.02–0.05 s) での k≈1.6–2.9x 破れ点
  (モデル形式に依存しない)。ただし cont は連続定格であり短時間
  トランジェントでの即時違反ではない点は falsify-004 の注意と同様。

## コアへの 1 行メッセージ
giemon-sim へ: falsify-004 の k≈1.04x は probe の慣性トルク次元誤り
(I·α² → 正しくは I·α) による過大評価 — 宣言速度上限内の
peak 120 破れ点は k≈11.7x (0.1 s ランプ) まで戻り、
j2 は realistic DR k 下でトランジェント含め peak には破れない。
残る検証対象は cont 40 に対する短ランプ破れ点 (k≈1.6–2.9x) と
exact RNEA による上限精密化。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_j2_ramp_family.py
# (対比) python3 sim-loop/evidence/probe_j2_limit_vel.py   # falsify-004 (I·α² 誤りを含む)
```

## 補足
- コード修正なし (probe は evidence 配下の測定専用、既存 probe も改変しない)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD 中〜高 (load ~5–7 / ncpu 10) のため軽量数値解析 probe のみ
  (falsify cheaply)。
