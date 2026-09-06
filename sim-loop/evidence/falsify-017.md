# falsify-017 — 軸アンダーフロー時の normalize 暗黙契約破れ (seeded 再現 / parity の潜在赤)

## 仮説 (1 iteration = 1 hypothesis)
H19: 「非ゼロ joint axis は `k/normalize` により必ず正しく単位ベクトル化され、
axis の表現倍率 (DR スケーリング / URDF importer 出力) によらず
同一論理軸・同一角度から同一回転が得られる」。
すなわち falsify-016 の seeded 再現 surrogate は「姿勢族」で検証したが、
「axis 表現」の面は未検証 — ここに破れがないか。

## 実測
probe: `sim-loop/evidence/probe_axis_underflow_parity.py`
(arm6 の j1/j2/j3/j5 軸 verbatim、kinematics.cljc と同一の normalize +
Rodrigues 数式)。加えて実装本体 `kotoba.giemon.kinematics` を
`clojure -M` で直接呼んで同一条件を確認した。

主要数字:
```
[Python surrogate] scale=1e-8, 1e-150 : 回転偏差 0 (ok)
[Python surrogate] scale=1e-200〜1e-300 : 48/48 ケースで DEVIATES
  ang=0.2   偏差 4.5e-2 rad
  ang=pi/2  偏差 5.2e-1 rad
  ang=3.0   偏差 1.4e-1 rad
[実装 kotoba.giemon.kinematics]
  j1 axis [0 0 1]*1e-200, ang=pi/2 : 回転行列最大偏差 1.000000e+00
  j2 axis [0 1 0]*1e-200, ang=pi/2 : 1.000000e+00
  j2 axis [0 1 0]*1e-200, ang=0.2  : 1.986693e-01
  (k/normalize [0 0 1e-200]) => [0.0 0.0 1.0E-200]  (単位化されない)
DR 軸倍率 1e-6〜1e6 (非アンダーフロー域) : 5 軸×5 倍率すべて max|dR|=0 (契約は成立)
```

機構 (実装 kinematics.cljc:27): norm の二乗和 (1e-200)² が double で
アンダーフローし norm=0.0 になる → `zero?` 分岐が「ゼロベクトル」と
誤判定して v を**変更なしで返す** → Rodrigues の x,y,z が非単位のまま →
回転がほぼ恒等行列に潰れる (例外は出ず、静かに誤った FK を返す)。

- seeded 再現への影響: 同一論理 joint 状態でも axis の表現倍率が
  1e-200 台に落ちた瞬間、2 回実行の「一致」は取れるが**両方とも誤り**、
  かつ正表現との間で FK が乖離 (pi/2 回転がほぼ消失)。URDF↔EDN parity
  でも同様に、片側だけ微小成分軸なら mismatches が発生しうる。
- 到達性: 現 fixture の軸は [0 0 1]/[0 1 0] で安全 (manifest 赤ではない)。
  赤は「normalize の zero 分岐が underflow をゼロベクトルと誤認する」
  潜在契約破れとして、DR/importer が axis を扱う将来経路で発火する。

## verdict
**refuted** — H19 の「非ゼロ axis は常に正しく単位化される」は破れた。
double アンダーフロー域 (成分 ~1e-200 以下) の非ゼロ軸で、
normalize は単位化せず、回転は静かに (例外なしに) 誤る。
非アンダーフロー域 (1e-6〜1e6 倍率) では契約は成立 (max|dR|=0)。

## コア (giemon-sim) への 1 行メッセージ
falsify-017: H19 refuted — k/normalize はアンダーフロー (norm² < ~1e-308)
をゼロベクトルと誤判定し非ゼロ軸を無正規化で返す (実装で
j1 軸 1e-200 × pi/2 が回転偏差 1.0 rad、例外なし)。
zero 分岐の閾値ガード or underflow 検出が要修理 (現 fixture 軸は安全)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_axis_underflow_parity.py            # SUMMARY: 48
clojure -M -e "(require '[kotoba.giemon.kinematics :as k]) \
  (println (k/normalize [0.0 0.0 1e-200]))"                        # [0.0 0.0 1.0E-200]
```
2 回実行: probe 出力 /tmp/f17a.txt と /tmp/f17b.txt は diff 0 行 (決定的)。

## 補足
- コード修正なし (probe は evidence 配下の測定専用、実装は読むだけ)。
- 決定的・タイムスタンプなしで記載。
- HOST LOAD 高 (64.95 59.34 45.38) につき軽量数値 probe + 1 回の REPL 呼び出し
  のみで完了 (falsify cheaply、数値積分・長時間 sim は省略)。
