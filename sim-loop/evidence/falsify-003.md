# falsify-003 — j2 full-dynamic worst-case: Coriolis/遠心項による DR 質量倍率での破れ

## 仮説 (1 iteration = 1 hypothesis)
H5: falsify-002 の結論「j2 は quasi-static + 慣性項の範囲では破れず、
真の動的破れはコリオリ/遠心項を含む full dynamic が必要」を検証する。
**H5 の反証対象は「j2 の cont 40 N·m は realistic DR 質量倍率 (k ≲ 5) 下でも
full dynamic を含めて破れない」という安全主張** — コリオリ/遠心項を含む
worst-case 簡易モデルで k の破れ点を測定し、realistic 速度域で破れが
出るなら主張は refuted (evidence として記録)。

## 実測 (probe_j2_coriolis.py、fixtures/giemon_arm6 の質量/ジオメトリを verbatim 使用)
```
tau0 = 3.40 Nm  I = 0.1215  I_distal = 0.1175 kg m^2
k=1 w2=5  w3=10 : total 29.9 Nm  (cont 未達)
k=2 w2=5  w3=10 : total 59.9 Nm  → cont 40 破れ
k=2 w2=10 w3=20 : total 219.0 Nm → peak 120 も破れ
k=5 w2=2  w3=5  : total 45.9 Nm  → cont 破れ
w2=3, w3=6  (realistic wrist 速度): k_break_cont = 3.83x
w2=5, w3=10                    : k_break_cont = 1.38x
```
- モデル: 重力 + j2 固有角加速度 + コリオリ (2·w2·w3·Σm r², distal of j3) +
  遠心 (w3² スイング水平 worst-case)。すべての項は DR 質量倍率 k に線形。
- falsify-002 の quasi-static probe では k_break ≈ 9.8–11.6x だったが、
  コリオリ/遠心項を入れると **w2=3/w3=6 で k≈3.8x、w2=5/w3=10 で k≈1.4x**
  に破れ点が下がる。DR の質量ランダム化範囲が ±20% 程度なら届かないが、
  質量スケールを含む DR (k にして 2x 以上) を許す設計では j2 cont が破れる。

## verdict
- H5 (j2 は realistic DR k 下でも full dynamic で破れない): **refuted** —
  コリオリ/遠心項により k≈1.4–3.8x で cont 40 が破れる (速度依存)。
  quasi-static のみの評価 (falsify-002) は j2 余裕を過大評価していた。
- なお本 probe は点質量・worst-case 整列の簡易モデルであり、exact RNEA による
  上限の精密化は次 iteration (giemon-sim 側の full dynamic 実装後に可能)。

## コアへの 1 行メッセージ
giemon-sim へ: DR の質量ランダム化範囲を設計する際、j2 cont 40 は
quasi-static 判定では安全に見えるが、コリオリ/遠心込みの worst-case では
質量スケール k≈1.4–3.8x (w2/w3 依存) で破れる — DR 質量範囲と actuator
速度上限の組でこの破れ点を再計算し、範囲に反映すること。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_j2_coriolis.py
# (前 iteration 対比) python3 sim-loop/evidence/probe_j2_dynamic.py
```

## 補足
- コード修正なし (probe は evidence 配下の測定専用)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD 高め (load ~5.6–11 / ncpu 10) のため数値解析 probe のみで
  長時間シミュレーションは省略 (falsify cheaply)。
