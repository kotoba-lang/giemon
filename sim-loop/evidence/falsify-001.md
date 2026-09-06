# falsify-001 — URDF↔EDN パリティ + FK 独立照合 + torque 余裕表 (giemon_arm6 / caterpillar_facade)

## 仮説 (1 iteration = 1 hypothesis)
H: `fixtures/giemon_arm6` の parity oracle 主張
(`from_edn(edn) == parse_urdf(urdf)`、README.md L84 / fixture 冒頭コメント) は、
機械比較で数値不一致を1件でも見つけられるなら破れる。
副次仮説 H2: `kotoba.giemon.arm/forward-kinematics` は独立実装の FK と食い違う。
副次仮説 H3: 既定 BOM (all-qdd) に隠れた underrated joint がある。

## 実測
### 1. 静的パリティ (機械比較、眼視ではない)
- 比較フィールド: joint 6本 × {origin, axis, damping, lower, upper, effort, velocity}、
  link 7本 (base_link 含む) × {inertial.origin, mass, inertia(ixx,iyy,izz,ixy,ixz,iyz)}
- 結果: **mismatches 0** (両 fixture)。caterpillar_facade boom 4 joints も mismatches 0。
- 検証コマンド (本ファイル同梱の probe):
  ```
  python3 sim-loop/evidence/probe_parity_arm6.py     # arm6: mismatches 0 (exit 0)
  ```
  caterpillar 分は本 iteration の heredoc 実行版 (下記 evidence 測定値と同一ロジック)。
- 1件の表現ギャップ (数値不一致ではない): child link の EDN `:inertia` は
  `ixy/ixz/iyz` を省略、URDF は明示 `0`。0-default 前提で一致。
  loader が 0-default しない実装ならここが破れ点になる — コア側で要確認。

### 2. テスト一式
- `cd orgs/kotoba-lang/giemon && clojure -M:test`
- **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

### 3. 動的照合 (Clojure 実行、-e 測定)
- `arm/underrated-joints` (all-qdd) → `()` — 空で正しい (torque テストと整合)。
- `arm/bom` :all-qdd=6件, :harmonic-shoulder=6件, j2 override cont-nm=**72** ✓
- 未知 variant → nil ✓
- `arm/end-effector a [0.0 0.2 -0.3 0.0 0.5 0.0]` →
  `[0.035165560086391295 0.0 0.6104766433183229]`
  同一入力の 2 回実行 → **完全一致 (seeded 再現の破れなし、この計算の範囲で)**。

### 4. FK 独立照合 (Rodrigues + 行列合成、pure Python 別実装)
- 独立実装: `[0.035165560086, 0.0, 0.610476643318]`
- Clojure 実測: `[0.035165560086391295, 0.0, 0.6104766433183229]`
- **一致 (|Δ| < 1e-9)** → H2 refuted (FK は破れず)。

### 5. torque 余裕表 (fixture テキストから測定)
| joint | effort | cont-nm | headroom | model |
|---|---|---|---|---|
| j1 | 40 | 40 | 0.0 | RobStride 04 |
| j2 | 40 | 40 | 0.0 | RobStride 04 |
| j3 | 30 | 40 | 10.0 | Damiao DM-J10010-2EC |
| j4 | 14 | 20 | 6.0 | Damiao DM-J8009-2EC |
| j5 | 10 | 10 | 0.0 | Unitree GO-M8010-6 |
| j6 | 6 | 8.3 | 2.3 | CubeMars AK70-10 / GO-M8010-6 |

- under-rated: **0件** → H3 refuted。ただし **headroom 0 の joint が 3 本 (j1/j2/j5)**:
  ドメインランダム化 (質量増) や payload 増に対してマージン皆無。
  worst-case DR 振りを sim 側に入れるなら j1/j2/j5 が最初に破れる点。

## verdict
- H (URDF↔EDN パリティ): **survived** — 数値不一致 0。ただし off-diagonal inertia の
  EDN 側省略は「0-default 前提」の暗黙契約として記録 (破れ候補 No.1)。
- H2 (FK 独立照合): **refuted** (= 実装は正しい)。
- H3 (隠れた underrated): **refuted** (= 存在しない)。headroom-0 ×3 の事実は記録。

## コアへの 1 行メッセージ
giemon-sim へ: `arm_edn_test` が読むのは EDN のみ — URDF を実際に parse して
`from_edn == parse_urdf` を assert する parity テストは未実装 (grep で `parse_urdf`/
`from_edn` の Clojure 側実装なし)。静的比較では一致したが、自動検証は未成立のまま。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M:test                                    # 46 tests / 115 assertions / 0 failures
python3 sim-loop/evidence/probe_parity_arm6.py     # mismatches: 0, exit 0
clojure -M -e '(require (quote [kotoba.giemon.arm :as arm]) (quote [clojure.edn :as edn]) (quote [clojure.java.io :as io])) ...'
# (end-effector 測定 — 本ファイル「実測 3」のコード)
```

## 補足
- ホスト負荷: load ~12 / ncpu=10 の高負荷のため、シミュレータ長時間実行は行わず
  静的 + 軽量動的照合に留めた (falsify cheaply)。
- コード修正なし (probe スクリプトは evidence 配下の測定専用ツール)。
- 決定的記述のみ、タイムスタンプなし。

## 追加測定: 静的重力 worst-case (j2 水平姿勢, pure static)
- link 質量を fixture 値そのまま使った簡易静定: j2 にかかる重力トルク
  (無 payload) = **2.73 N·m** (cont 40 に対し小)。
- payload 0.5/1.0/1.5/2.0/3.0 kg を先端に載せた静的換算でも
  5.4–18.6 N·m で cont 40 に届かず → **静的には破れない**。
- 含意: j2 の「余裕僅少」は静的重力ではなく動的 (加速度/DR質量増幅) 側にある。
  DR worst-case は加速度項を振るべき (次 iteration の仮説候補)。
