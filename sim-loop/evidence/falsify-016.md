# falsify-016 — DR 初期姿勢 worst-case × seeded 再現の組合せ probe (maturity NEXT (d))

## 仮説 (1 iteration = 1 hypothesis)
H18: 「初期姿勢族 (レバー係数 f × j2 仰角 q2) の中に、
falsify-002〜007 が前提とした水平全延長姿勢 (f=1.0, q2=0) より
j2/j5 の DR 質量倍率破れ点 k を下げる姿勢が存在する。
すなわち以前の『realistic DR k (≈1.2) では headroom-0 3 本とも破れない』は
姿勢族で再測すると反証されうる」。
副仮説: 複数初期姿勢 q0 に対する同一入力 seeded 再現 (姿勢を変えた
SEED-PARITY) が破れる (2 回実行で end-effector が一致しない姿勢がある)。

## 実測 (probe_posture_family_seed.py)
fixtures/giemon_arm6 の質量/ジオメトリ verbatim の点質量 worst-case モデル
(falsify-006/007 と同一の往復台形 RMS デューティ形式)。
姿勢族: f ∈ {1.0, 0.8, 0.5, 0.3} × q2 ∈ {0°, 30°, 60°, 85°} の 16 ケース。
(f はリンク COM の水平レバー係数、q2 は重力レバー cos(q2) 係数。
j2 重力トルクは f と cos(q2) の両方に単調 — 解析的最大点は f=1.0, q2=0。)

主要数字 (k_rms = cont RMS 破れ点の質量倍率 / k_peak = peak 破れ点):
```
f=1.00 q2=0  : tau0_j2=3.40 Nm  k_rms_j2@40=10.40  k_peak_j2@120=17.48
               tau0_j5=0.647    k_rms_j5@10=10.04  k_peak_j5@23.7=11.69   <- 以前の probe の姿勢
f=1.00 q2=30 : k_rms_j2=11.54   k_peak_j2=18.72    k_rms_j5=12.90
f=0.80 q2=0  : k_rms_j2=13.64   k_peak_j2=24.30
f=0.50 q2=0  : k_rms_j2=23.11   k_peak_j2=46.74
f=0.30 q2=30 : k_rms_j5=133.04  k_peak_j5=153.79 (j5 の最大余裕)
f=0.30 q2=85 : k_rms_j2=200.00 (未達) k_peak_j2=299.51
SUMMARY: posture-cases 16, seed-parity-fails 0
worst-case (min) k_rms_j2 over posture family = 10.40 (f=1.0, q2=0)
j2 static worst posture: max tau0_j2 = 3.40 Nm at f=1.0 (単調性で確認)
```
- 姿勢族最小の破れ点は f=1.0, q2=0 (= 以前の probe が使った姿勢)。
  すなわち水平全延長が j2 重力レバーの解析的最大点であることを数値で確認し、
  これより厳しい初期姿勢は族内に存在しない。realistic DR k (≈1.2) に対し
  最悪姿勢でも cont で 8.7 倍 / peak で 14.6 倍の余裕。
- j5 も同様に f=1.0 側が最悪 (k_rms 10.04) で、q2=60° では重力が手首を
  逆方向に引くため半分のケースで k が上昇する。
- seeded 再現 surrogate (姿勢ごとの決定的順運動学 2 回実行一致):
  16/16 姿勢で SEED-PARITY true、fails 0。2 回実行の出力 diff 0 行 (決定的)。
- 2 回実行: python3 実行 2 回、出力 22 行×2 とも全行一致 (cmp 相当、exit 0)。

## verdict
**survived** — H18 は破れず。
(a) 初期姿勢族内に falsify-002〜007 の水平全延長より厳しい姿勢は存在しない
    (f=1.0, q2=0 が解析的にも数値的にも最大点 — f と cos(q2) の単調性から
    姿勢族による破れ点低下は原理的に起きないと確認)。
    headroom-0 3 本の「realistic DR k で破れない」(H9) は初期姿勢 DR
    ランダム化に対しても頑健。
(b) 姿勢を変えた同一入力 seeded 再現 surrogate も 16/16 で一致 (決定的)。
    ただしこれは決定的関数の 2 回実行一致であり学習ジョブ実装ではなく
    L0 評価は変化なし (bench-002〜044 と同じ性格)。

## コア (giemon-sim) への 1 行メッセージ
falsify-016: H18 survived — 初期姿勢族 (f×q2, 16 ケース) で j2/j5 の DR k
破れ点が最小になるのは falsify-002〜007 が使った水平全延長 f=1.0, q2=0
そのもの (k_rms_j2=10.40 / k_rms_j5=10.04、realistic DR k≈1.2 の 8 倍以上の
余裕)。DR 初期姿勢ランダム化で headroom-0 が破れる経路は点質量モデルの
範囲では存在しない。姿勢付き seeded 再現 surrogate も 16/16 決定的。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_posture_family_seed.py > /tmp/f16a.txt 2>&1
python3 sim-loop/evidence/probe_posture_family_seed.py > /tmp/f16b.txt 2>&1
diff /tmp/f16a.txt /tmp/f16b.txt   # 0 行差 (決定的)
```

## 補足
- コード修正なし (probe は evidence 配下の測定専用)。
- 決定的・タイムスタンプなしで記載。
- HOST LOAD 高 (33.44 38.28 49.99 / 5min) につき軽量数値解析 probe のみで
  数値積分・長時間 sim は省略 (falsify cheaply)。破れ点は点質量モデルの
  下限値 (exact RNEA 未実施) である点は falsify-007 と同じ既知限界。
