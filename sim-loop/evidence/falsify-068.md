# falsify-068 (H69) — FK guard repair 依然未配線か (新 HEAD 00fd23f 静的再確認)

## 仮説
H69: giemon HEAD が d0d3cb4 → 00fd23f9d047 に進行したため、新 HEAD で
`within-limits?` が FK 経路に配線され silent zero-fill が解消された可能性。

## 実測 (純静的読取, /tmp redirect + read_file workaround, /tmp/f69_probe.txt /tmp/f69b.txt /tmp/f69c.txt)
- HOST LOAD: 1min 25.75 / 5min 18.31 / 15min 22.37 (15min ≈ 2.6× ncpu=10) → Load gate
  (15min ≥ 2×ncpu=20) 超過につき test スイート / seeded 再現は省略、test 計数 unmeasured。
- HEAD giemon: 00fd23f9d04743323047c8c29c30aa18320daa70 (bench-242 観測と同一・不変)。
- git status: ` M sim-loop/status/maturity.md` + `??` sim-loop/evidence/* のみ・tracked diff 空。
- `within-limits` 全ヒット 5 行のみ:
  - src/kotoba/giemon/arm.cljk L15 (defn) / L28 (docstring)
  - test/kotoba/giemon/arm_test.cljk L28-30 (単体テストのみ)
  - FK 本体 (forward-kinematics L22 / end-effector L46) 内部からの呼出 **0 回**。
- silent zero-fill `(angle (or (first angles) 0.0))` は arm.cljk L38 不変。
- governor.cljk の limit/torque/within 参照 **0 行**。

## verdict: refuted
新 HEAD 00fd23f でも FK guard repair は未配線 — 越境 angles は silent 受理で pose 返却。
falsify-034/036/039〜067 と同根、**31 連続 refuted**。新規破れ・回帰なし (静的範囲)。

## 再現手順
```
grep -rn "within-limits" src/kotoba/giemon/ test/kotoba/giemon/
grep -n "or (first angles)" src/kotoba/giemon/arm.cljk
grep -c "limit\|torque\|within" src/kotoba/giemon/governor.cljk
git rev-parse HEAD   # 00fd23f9d047...
```

## コアへのメッセージ (1 行)
NEXT 再発行: arm.cljk forward-kinematics 本体に within-limits? を配線し、
越境 angle を拒否/クランプ/nil のいずれかで検証層に観測可能にせよ (arm_test L20-22
zero-fill 緑 assertion の期待値変更込み) — 31 連続未着手。
