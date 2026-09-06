# falsify-004 — j2 破れ点を宣言速度上限内に閉じた場合の再測定 (falsify-003 の速度ペアは fixture の :velocity 上限外だった)

## 仮説 (1 iteration = 1 hypothesis)
H6: 「falsify-003 の破れ点 (コリオリ/遠心込みで k≈1.4–3.8x で cont 40 破れ) は
realistic DR 質量倍率下の実効的な破れ点である」 — 反証対象は
**「j2 は宣言された :joint/limit (:velocity 3 rad/s, cont 40 / peak 120)
の範囲内で realistic DR 質量倍率 (k ≲ 5) 下では破れない」という安全主張**。

falsify-003 の速度ペア (w2=3/w3=6, w2=5/w3=10) を fixture と照合すると、
w3=6 は j3 の :joint/limit :velocity 3 を超過、w2=5 は j2 の :velocity 3 を超過**していた。
つまり falsify-003 の k≈1.4–3.8x は宣言範囲外の速度での破れ点であり、
「宣言範囲内では安全」という主張はまだ反証されていない。本 probe
(`probe_j2_limit_vel.py`) は falsify-003 と同一の点質量 worst-case モデルで
速度を宣言上限 (w2=3, w3=3) に閉じ、加えて 0.1 s ランプ (alpha=30 rad/s^2) の
加速 worst-case を追加して破れ点を再測定する。

## 実測 (probe_j2_limit_vel.py、fixtures/giemon_arm6 の質量/ジオメトリを verbatim 使用)
```
tau0 = 3.40 Nm  I = 0.1215  I_distal = 0.1175 kg m^2
宣言上限: w2<=3.0 (j2), w3<=3.0 (j3), alpha_ramp=30.0 rad/s^2

-- 定常 (w2=3, w3=3) --
k=1.0: total=6.6    → 未達
k=5.0: total=32.9   → 未達
k=8.0: total=52.6   → cont 40 破れ
k_break_cont (定常) = 11.54x

-- 加速ランプ worst-case (alpha=30 rad/s^2, w2=3, w3=3) --
k=1.0: grav=3.4 inert=109.4 cor=2.1 cent=1.1 total=115.9 → cont 破れ
k=2.0: total=231.9 → peak 120 も破れ
k_break_cont (ランプ) = 0.33x   k_break_peak (ランプ) = 1.04x
```

- falsify-003 の速度ペアは宣言上限外: w2=3.0 (j2 内) / w3=6.0 (**j3 上限 3 超過**)、
  w2=5.0 (**j2 上限 3 超過**) / w3=10.0 (**j3 上限 3 超過**)。
- 宣言速度上限に閉じると、コリオリ/遠心による破れ点は k≈11.5x に戻る
  (falsify-002 の quasi-static k≈9.8–11.6x と同桁) — falsify-003 の k≈1.4–3.8x は
  宣言範囲外の速度に依存する数値であり、そのまま DR 設計根拠には使えない。
- **ただし加速度項が新たな破れ**: 宣言速度上限内でも 0.1 s で上限速度まで
  ランプする最悪ケースでは total 115.9 N·m (k=1、名目質量) で
  **連続トルク 40 を k=1 で破り、peak 120 は k≈1.04x で破れる**。
  DR 質量ランダム化が ±20% 程度でも k=1.2 → total 139 N·m で peak 破れ。

## verdict
- H6 (j2 は宣言速度上限内なら realistic DR k で破れない): **refuted** —
  ただし破れの主因はコリオリではなく**角加速度 (慣性) 項**:
  加速ランプ worst-case で peak 120 が k≈1.04x (ほぼ名目質量) で破れる。
  定常動作に閉じれば破れ点は k≈11.5x まで上がる (falsify-003 の k≈1.4–3.8x は
  宣言範囲外の速度ペアに依存しており撤回に値する)。
- 注意: cont 40 は連続定格であり短時間トランジェントで 115 N·m 自体は
  即時違反ではない — 本 probe の実質的赤は「トランジェント (ランプ) が
  peak 120 に達するのが k≈1.04x」の点。0.1 s ランプの仮定が支配的パラメータ
  (ramp 0.3 s なら alpha=10、inert≈12.2 N·m に低下し total は cont 未達) であり、破れ点は
  トラジェクトリの加速度プロファイルに強く依存する。

## コアへの 1 行メッセージ
giemon-sim へ: falsify-003 の速度ペア (w2=5/w3=10 等) は fixture の
:velocity 3 を超えており、宣言範囲内の破れ点はコリオリではなく加速度項が支配 —
宣言速度上限内でも 0.1 s ランプで peak 120 が k≈1.04x で破れるため、
DR 設計には質量範囲だけでなくトラジェクトリ加速度プロファイルの上限
(またはランプ時間) の明示が必要。falsify-003 の k≈1.4–3.8x は宣言範囲外
依存として DR 根拠から外すこと。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_j2_limit_vel.py
# (対比) python3 sim-loop/evidence/probe_j2_coriolis.py   # falsify-003 (宣言範囲外の速度ペア)
```

## 補足
- コード修正なし (probe は evidence 配下の測定専用)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD 高め (load ~5.2–7.9 / ncpu 10) のため数値解析 probe のみで
  長時間シミュレーションは省略 (falsify cheaply)。
