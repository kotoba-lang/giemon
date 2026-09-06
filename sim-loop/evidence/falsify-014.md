# falsify-014

## 仮説
H16 — gate/arm 受付口の torque 無検査は、これまで未測定の入力空間
(文字列化 torque、別名キー (torque/Nm/effort)、mission メタデータ経由、
バッチアクション内の 1 アクションに極端 torque) でも決定的に不変である。

## 実測 (本回: 測定成立 — 初回は ENV-BLOCKED/inconclusive だったため再試行)
probe: probe_gate_input_space_widening.py (実測 probe に差し替え済み)。
falsify-013 と同一の gate 呼び出し経路 (`rob/action` + `rob/gate`) で
14 ケースを列挙し、2 回実行で照合。

結果 (clojure -M -e、exit 0):
- A 文字列化 / 構造エッジ (5 ケース + clean baseline):
  "120" / "1e6" / 5 層深入れ tau 1e6 / vector 包み / quoted-map —
  すべて `:permit`、clean (tau 0.0) baseline と同一 decision、
  payload-carried true (params はそのまま保持)
- B 別名キー (4 ケース): torque / Nm / effort / トップレベル torque —
  すべて `:permit`、baseline と同一
- C mission メタデータ経由: `rob/mission` は :metadata {:tau 1e6} を
  契約に保持しない (mission-differs: false — メタデータはそもそも届かない)。
  同 mission-id action は `:permit`
- D バッチ 3 アクション (中央に極端 torque): 3 件すべて `:permit`、
  clean 隣接ケースと decision 同一
- E safety-critical :emit (3 ケース: str-1e6 / effort / numeric 1e6):
  すべて `:deny` (安全側維持、payload は :deny でも伝播)
- SUMMARY: GATE-WIDENING-CASES 14、GATE-WIDENING-DETERMINISM-FAILS 0、
  2 回実行 diff 0 行 (exit 0)

## verdict
**survived** — H16 は破れず。新規の 4 入力空間でも decision は payload 無相関・
決定的。gate の torque 無検査 (falsify-002/010/011/012/013 の赤「未接続の検査層」)
は文字列化・キーエイリアス・mission メタデータ・バッチ面に拡張決定的。
新規構造的注記 1 件: mission 契約に metadata スロット自体が存在せず、
mission レベルのペイロード搬送経路は設計上不在 (新しい赤ではなく不在の確認)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_gate_input_space_widening.py > /tmp/h16.clj
clojure -M -e "$(cat /tmp/h16.clj)" > /tmp/h16.txt 2>&1
clojure -M -e "$(cat /tmp/h16.clj)" > /tmp/h16b.txt 2>&1
diff /tmp/h16.txt /tmp/h16b.txt   # 0 行差
```

## コア (giemon-sim) への 1 行メッセージ
falsify-014: H16 survived — gate の torque 無検査は文字列化/別名キー/
mission メタデータ/バッチの全入力空間でも決定的 (14 ケース、decision 変化 0、
2 回実行 diff 0 行)。gate↔arm の torque 照合は依然未接続のまま。
