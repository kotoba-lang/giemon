# falsify-006 — falsify-005 の残った赤「短ランプ cont 40 破れ点 k≈1.6–2.9x」は瞬時トルク vs 連続定格の比較誤りに依存する (RMS デューティ評価では破れ点は k≈3.8–8.3x に上がる)

## 仮説 (1 iteration = 1 hypothesis)
H8: 「falsify-005 が残した赤 (0.02–0.05 s ランプで cont 40 が k≈1.6–2.9x で破れる)
は realistic DR 質量倍率 (k ≲ 1.2) 下でも到達しうる実効的な違反である」 —
反証対象は **「j2 は宣言速度上限内の短ランプ加速トランジェントで realistic DR k 下
でも cont 40 を破る」という主張**。

falsify-004/005 は**瞬時トルク**を cont 40 (連続=熱的定格) と直接比較していた。
連続定格の意味合いは熱的 (i² ∝ τ²) であり、実効性の判定はデューティサイクル
RMS トルクで行うべき。本 probe (`probe_j2_cont_duty.py`) は同一の点質量
worst-case モデルで往復台形速度プロファイル + rest (0.2/1.0 s、ブレーキ保持の
有無) のサイクルを組み、RMS = cont 40 になる質量倍率 k_rms を 2 分探索で測る。
加速度ランプ区間は 20 サンプル分割で α を線形ランプ (瞬時一定 α の保守側)。
重力は往路 +τ0/復路 −τ0、減速・復路ランプは重力と慣性が打ち合う方向も含む。

## 実測 (probe_j2_cont_duty.py、fixtures/giemon_arm6 の質量/ジオメトリを verbatim 使用)
```
tau0=3.40 Nm  I=0.1215  coeff_dyn(w=3,3)=3.17
 ramp_s rest_s  hold | k_rms@cont40 k_peak@120 | k=1.2 RMS / peak
   0.02    0.2 False |         3.82       5.02 |   13.1 /   28.0 Nm
   0.02    0.2  True |         3.81       5.02 |   13.1 /   28.0 Nm
   0.02    1.0 False |         4.17       5.02 |   12.0 /   28.0 Nm
   0.02    1.0  True |         4.12       5.02 |   12.1 /   28.0 Nm
   0.05    0.2 False |         7.59       8.89 |    7.4 /   15.6 Nm
   0.05    1.0 False |         8.29       8.89 |    6.8 /   15.6 Nm
   0.10    0.2 False |        10.04      11.95 |    6.2 /   11.4 Nm
   0.30    1.0 False |        12.29      15.53 |    5.4 /    8.6 Nm

reference (瞬時比較, falsify-005 の形式そのまま再現):
  ramp=0.02: k_cont_inst = 1.61
  ramp=0.05: k_cont_inst = 2.88
  ramp=0.1:  k_cont_inst = 3.91
```
- 瞬時比較の数値は falsify-005 と完全一致 (k=1.61 / 2.88 / 3.91) — モデルは整合。
- デューティ RMS 評価では k_rms は最小でも **3.82x** (0.02 s ランプ・rest 0.2 s)、
  0.05 s ランプでは **7.5–8.3x** まで上がる。k=1.2 での最大 RMS は 13.1 N·m
  (cont 40 の 33%)、最大瞬時 28.0 N·m (peak 120 の 23%)。
- 2 回実行一致を確認 (cmp /tmp/run1.txt /tmp/run2.txt → exit 0、決定的)。

## verdict
- H8 (短ランプ瞬時 cont 破れ k≈1.6–2.9x は realistic DR k 下で実効的な違反): **refuted** —
  瞬時トルク vs 連続定格の直接比較は保守すぎる評価形式であり、熱的に意味のある
  RMS デューティ評価では realistic DR k (≈1.2) は cont 40 に対して 3 倍以上の余裕を保つ。
  破れ点は k≈3.8x (0.02 s ランプ・最短 rest) まで下がるが、±20% DR では依然届かない。
- falsify-005 の「残った赤」の実効性は剥奪される。j2 の cont 40 破れ点は
  すべての評価形式で k ≈ 3.8x 以上 (peak 120 は k ≈ 5.0x 以上) となり、
  realistic DR k (≈1.2) の範囲では j2 は peak/cont のいずれでも破れない。
  これは falsify-002 の k≈9.8–11.6x (quasi-static) から始まる一連の測定と整合的。
- 残る未反証領域: (a) exact RNEA による点質量 worst-case の上限精密化、
  (b) off-diagonal inertia の 0-default 暗黙契約、(c) headroom 0 joint
  (j1/j2/j5 — falsify-005 記載) の検証。次 iteration の対象。
- 注意: 本 probe も点質量モデルであり実機のリンク剛体慣性 (:inertia ixx 等) は
  未反映。破れ点は上振れ (楽観) 側の可能性があるため「k≈3.8x 以上」は
  下限値として読むこと。

## コアへの 1 行メッセージ
giemon-sim へ: falsify-005 残赤の「短ランプ cont 40 破れ k≈1.6–2.9x」は
瞬時トルクと連続 (熱的) 定格の直接比較による過大評価 — 往復台形デューティの
RMS 評価では破れ点は k≈3.8–8.3x に上がり、realistic DR k (≈1.2) では
j2 は peak/cont ともに破れない (k=1.2 最大 RMS 13.1/40 N·m)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_j2_cont_duty.py   # 2 回実行して diff なしを確認
# (対比) python3 sim-loop/evidence/probe_j2_ramp_family.py   # falsify-005 (瞬時比較)
```

## 補足
- コード修正なし (probe は evidence 配下の測定専用、既存 probe も改変しない)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD 低〜中 (load averages 4.22 6.95 8.21) のため軽量数値解析 probe のみ
  (falsify cheaply)。
