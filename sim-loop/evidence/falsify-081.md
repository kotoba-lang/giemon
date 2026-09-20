# falsify-081 (H82) — falsify-080 判定以降も HEAD は不変で修復未着地か (HEAD 直読込み純静的)

## 仮説

H82: falsify-080 (H81, 実行 backend 全滅で HEAD 再読不能だった走) 以降、giemon
HEAD が 41ac173f8e9dc599e8b9ab340a51f4135d5ade98 から変移し、FK guard repair
(`within-limits?` の FK 経路配線) または governor rejected レコード化・負テスト
が新 blob に着地している。

## 実測 (HEAD 直読込み純静的・決定的)

- 実行条件: host load 1/5/15-min 32.28/27.73/23.87 (15-min ≈ 2.8× ncpu=10、
  Load gate 超過) + terminal 実行 backend 応答不能 (`echo hello` を含む全コマンド
  空出力・bench-225/226/227/278 と同一症状の再燃)。test 計数・seeded 再現は
  実施不能 → unmeasured (honest)。
- **HEAD は .git/HEAD 直読で本走初めて再実測**: 41ac173f8e9dc599e8b9ab340a51f4135d5ade98
  (detached、falsify-078/079 の記録と同値・不変 — falsify-080 が「HEAD sha の
  実測再読は本走できず」と記した欠落を本走で補完)。
- `src/kotoba/giemon/arm.cljk` (121 行全文直読):
  - `within-limits?` は L15 defn / L27-28 docstring のみ。FK 本体
    `forward-kinematics` (L22-41) / `end-effector` (L43-46) 内呼出 0 回。
  - L38 `(or (first angles) 0.0)` silent zero-fill 不変。
- `test/kotoba/giemon/arm_test.cljk` (40 行全文直読): L20-22「missing angles
  default to 0.0」zero-fill 緑期待値無変更。
- `test/kotoba/giemon/governor_test.cljk` (47 行全文直読): deftest 6 件
  (kaigo-mission / kaigo-action-defaults / fall-detected-alert / ops-mission /
  ops-action-defaults / chemical-dispense-alert) 全て正テスト、不正 kind/safety
  負テスト 0 件・rejected レコード化の痕跡 0 件。

## verdict: refuted

「HEAD 変移 + 修復着地」仮説は不成立 — HEAD は 41ac173 で不変を本走で直接実測し、
blob 内容も falsify-080 と同値 (FK guard repair 未配線は falsify-034 起計
40 連続 refuted、governor 負テスト 0 件 / rejected レコード不在は
falsify-072/076/077/078/080 と同値)。コアへの 1 行メッセージ: runner repair
(NEXT) と FK guard repair・governor rejected レコード化は現 HEAD 41ac173 でも
未着手 — bench-244 起の silent-zero が続く限り全軸の測定経路が失活したまま。

## 再現手順

1. `git -C orgs/kotoba-lang/giemon rev-parse HEAD` → 41ac173f8e9d… を確認。
2. `grep -n 'within-limits?' src/kotoba/giemon/arm.cljk` → L15 (defn) / L28
   (docstring) の 2 箇所のみ、L22-41 / L43-46 内に呼出なしを確認。
3. `grep -nE 'rejected|append|record|:nope|:teleport' test/kotoba/giemon/governor_test.cljk`
   → 0 件を確認 (deftest 6 件全て正テスト)。
