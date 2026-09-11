# falsify-002 — governor gate 迂回 (LLM-to-actuator shortcut) + j2 動的 worst-case

## 仮説 (1 iteration = 1 hypothesis)
H4: `kotoba.robotics/gate` は safety-class の取り扱いを弄ることで
actuating action (:move/:actuate, torque payload 付き) を人間サインオフ無しで
:permit できる — すなわち LLM-to-actuator shortcut が存在する。
副次測定: falsify-001 の含意「j2 の余裕僅少は動的側にある」を
quasi-dynamic probe (`probe_j2_dynamic.py`) で定量化する。

## 実測 — H4 (governor gate, kbb -M -e、/tmp/gate.txt 相当)
| ケース | 入力 | 結果 |
|---|---|---|
| low クラスで gate 許可セット内 | `:move` `:safety :low`, allowed `#{:none :low :medium}` | **:permit** |
| 許可セット空 | 同 action, allowed `#{}` | :deny (safety-class-not-allowed) |
| safety-critical がクラス集合に含まれる | `:actuate` `:safety :safety-critical`, allowed 全クラス | :permit だが `action-permitted?` → **false** (:require-sign-off 判定が正しく効く) |
| fall-detected-alert | 全クラス allowed | **:require-sign-off** (:safety-critical 硬コード、正しい) |
| 偽 kind / nil action | `:nonsense` / nil | nil / :invalid (:not-an-action) |
| 偽 stop reason | `:bogus-reason` | nil |

- クラス操作による迂回は**見つからなかった** — `action-permitted?` は `gate` に
  委譲しており sign-off クラスを wave-through しない (docstring の修正済み履歴と整合)。
- **ただし構造的ギャップを 1 件記録**: `gate` は `:action/params` を一切検査しない
  (`:torque-params-inspected? true` は params が保持されるだけで、torque/角度は未検証)。
  `:safety :low` の `:move` が `{:tau 120.0 ...}` (j2 cont 40 / peak 120 超) を載せたまま
  **:permit される**。`kotoba.giemon.arm/within-limits?` は角.limit のみで torque を見ず、
  gate↔arm の torque 照合を接続する実装は giemon/robotics 両方に存在しない
  (grep で gate から arm を require する箇所なし)。
  → これは gate の契約 (:safety-class のみ、torque は gate の外) と宣言どおりであり
  H4「gate 自体の迂回」は**破れず**。しかし「torque 余裕違反入力がゲートを
  そのまま通過する」事実は初期化されていない検査層として記録される。

## 実測 — 副次: j2 動的 worst-case (probe_j2_dynamic.py)
```
I_j2(point-mass) = 0.1256 kg m^2
tau0 (gravity, no payload) = 3.44 Nm  (falsify-001: 2.73)
tau(3kg payload @0.55m) = 19.62 Nm (falsify-001: 18.6)
alpha to break cont 40 at k=1: 291.1 rad/s^2
DR mass scale k to break cont 40, alpha=0: 11.63x
DR mass scale k to break cont 40, alpha=5 rad/s^2: 9.84x
peak-nm margin at k=2, alpha=5: 111.9 Nm of 120
```
- j2 静的重力は falsify-001 と同桁 (3.44 vs 2.73、COM モデル簡略差)。
- cont 40 を破るには: 定常トラジェクトリでは alpha ≈ 291 rad/s^2 (非現実的) か
  DR 質量倍率 k ≈ 10–12x が必要 → **quasi-static の範囲では j2 は破れない**。
- peak 120 に対し k=2×alpha=5 でも余裕 111.9 N·m。falsify-001 の
  「動的側に余裕僅少」含意は、quasi-static + 慣性項のモデルでは支持されず、
  真の動的破れはコリオリ/遠心項を含む full dynamic が必要 (次 iteration)。

## verdict
- H4 (governor gate 迂回): **survived** — クラス操作では迂回できない。
  構造的ギャップ (gate が params/torque を無検査で通す) を evidence として記録。
- 副次 (j2 quasi-dynamic): **破れなし** — quasi-static + 慣性項では cont/peak に届かず。

## コアへの 1 行メッセージ
giemon-sim へ: gate は torque/角度 params を一切見ない — `:safety :low` の
`:move` が `{:tau 120}` を載せて :permit される。torque 余裕照合は
`kotoba.giemon.arm` 側にのみ存在し gate と未接続。シミュレータ側の
actuation 受付で torque を arm/within-limits 相当と照合する層が必要
(実装するなら gate ではなく sim 受付口に)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_j2_dynamic.py
# H4: 上記「実測 — H4」の kbb -M -e スクリプト (kotoba.giemon.governor +
# kotoba.robotics を require し gate/action-permitted? を全ケースで実行)
```

## 補足
- コード修正なし (probe は evidence 配下の測定専用)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD は高め (load ~9–13 / ncpu 10) のため長時間シミュレーションは省略
  (falsify cheaply)。静的 + 軽量 kbb -M -e 測定のみ。
