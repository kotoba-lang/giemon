# falsify-007 — headroom 0 の残り 2 本 (j1/j5) は realistic DR k 下で破れないか (falsify-001〜006 は j2 のみ測定)

## 仮説 (1 iteration = 1 hypothesis)
H9: 「headroom 0 joint (j1/j2/j5) は realistic DR 質量倍率 (k ≲ 1.2) 下では
peak/cont のいずれも破れない」 — falsify-001 が headroom 0 ×3 (j1/j2/j5) を
記録して以来、j2 のみが falsify-002〜006 で測定され、j1/j5 は未測定のまま。
反証対象は **「j1/j5 も j2 と同様に realistic DR k で破れない」という安全主張**。
j5 は cont 10 N·m と絶対余裕が最も小さく、j1 は鉛直軸で様相が異なるため、
j2 の結論の外挿は未検証だった。

モデル (probe_j1_j5_headroom.py、fixtures/giemon_arm6 の質量/ジオメトリを
verbatim 使用、falsify-006 と同一の往復台形 RMS デューティ評価):
- j1 (軸 z・鉛直): 重力トルク 0。動的負荷は遠心 (w1²·I_z) +
  j2 スイングとのコリオリ様結合 (2·w1·w2·I_z、保守上界)。
  I_z = Σ m·r² (アーム水平折りたたみ worst-case、全リンク distal)。
- j5 (軸 y・手首ピッチ): 重力 = m6·g·r6 (アーム水平 worst-case) +
  慣性 I5·α + 遠心 (w1²·I5) + コリオリ様 (2·w5·w6·I5、保守上界)。

## 実測 (probe_j1_j5_headroom.py)
```
j1: I_z=0.1215 kg m^2  coeff_dyn(w1=3, w2=3)=2.19 Nm  cont=40 peak=120
  alpha=  3.0: k_rms@cont40=200.00 (未達)  k_peak@120=47.36  k=1.2 RMS=2.1 / peak=2.6 Nm
  alpha= 10.0: k_rms@cont40= 66.14         k_peak@120=35.91  k=1.2 RMS=2.2 / peak=3.6 Nm
  alpha= 30.0: k_rms@cont40= 21.15         k_peak@120=21.24  k=1.2 RMS=3.1 / peak=6.3 Nm

j5: tau0=0.65 Nm  I5=0.03630  coeff_dyn=1.779 Nm  cont=10 peak=23.7 (GO-M8010-6)
  alpha=  8.0: k_rms@cont10= 15.14        k_peak@23.7= 8.77  k=1.2 RMS=1.9 / peak=2.9 Nm
  alpha= 20.0: k_rms@cont10= 13.37        k_peak@23.7= 7.61  k=1.2 RMS=2.0 / peak=3.4 Nm
  alpha= 40.0: k_rms@cont10=  9.89        k_peak@23.7= 6.23  k=1.2 RMS=2.1 / peak=4.2 Nm

static: j1 重力トルク about z = 0.00 Nm (鉛直軸); j5 静的 = 0.65 / 10.0 Nm
```
- 2 回実行一致を確認 (cmp → exit 0、決定的)。
- j1: 鉛直軸のため重力負荷がなく、k=1.2 での最大瞬時 6.3 N·m (peak 120 の 5%)。
  破れ点は最小でも k≈21x (α=30 の急ランプ時)。
- j5: 3 本の headroom-0 joint 中で最も厳しい (cont 10 N·m に対し破れ点
  k≈9.9x、peak 23.7 に対し k≈6.2x @0.1 s ランプ) が、k=1.2 では
  最大 RMS 2.1 / 10 N·m (21%)、最大瞬時 4.2 / 23.7 N·m (18%) と十分な余裕。
- j5 のコリオリ様項 (2·w5·w6·I5 = 1.45 N·m) は静的重力 (0.65) の 2 倍超だが、
  cont 10 N·m に対しては依然小さい。宣言速度上限 (w5=4 rad/s) 内の測定。

## verdict
- H9 (headroom-0 joint は realistic DR k 下で破れない): **survived** —
  j1/j5 のいずれも k=1.2 では peak/cont ともに破れない。
  破れ点の最も低いのは j5 (k≈6.2x peak / k≈9.9x cont @0.1 s ランプ) だが
  realistic DR k (≈1.2) の 5 倍以上の余裕。j2 についても falsify-006 で
  k≈3.8x 以上が確認済みのため、headroom-0 3 本全体で H9 は成立。
- falsify-001 の「headroom 0 = DR に対してマージン皆無」は静的評価に基づく
  指摘として正しいが、宣言速度上限内のデューティ動作では
  realistic DR k で実効的な破れには至らない (j5 が律速だが k≈6x)。
- 残る未反証領域: (a) exact RNEA による上限精密化 (本 probe も点質量モデル、
  リンク剛体慣性 :inertia ixx 等は未反映 — 破れ点は下限値)、
  (b) off-diagonal inertia の 0-default 暗黙契約、(c) 宣言速度上限**外**
  の速度ペアを許す DR 速度ランダム化を実装する場合の j2 破れ点
  (falsify-003: k≈1.4–3.8x — DR 設計が速度をランダム化しない限り不問)。
- 注意: j5 の評価は GO-M8010-6 (cont 10 / peak 23.7) 前提。EDN の note にある
  とおり AK70-10 (cont 8.3) への差し替えなら余裕はさらに 17% 減るが、
  破れ点 k は比例減のみで k≈5x 台に留まる。

## コアへの 1 行メッセージ
giemon-sim へ: headroom-0 の j1/j5 も realistic DR k (≈1.2) では破れない
(j5 が律速: peak 破れ点 k≈6.2x / cont RMS 破れ点 k≈9.9x @0.1 s ランプ、
k=1.2 最大 RMS 2.1/10 N·m)。headroom-0 3 本の実効的破れは DR 質量スケール
では生じない — DR 設計で注意すべきは j2 + 速度上限外ランダム化の組合せのみ。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_j1_j5_headroom.py   # 2 回実行して diff なしを確認
# (対比) python3 sim-loop/evidence/probe_j2_cont_duty.py   # falsify-006 (j2)
```

## 補足
- コード修正なし (probe は evidence 配下の測定専用、既存 probe も改変しない)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD 中 (load averages 19.77 24.09 26.40 / ncpu 10) のため軽量数値解析
  probe のみで長時間シミュレーションは省略 (falsify cheaply)。
