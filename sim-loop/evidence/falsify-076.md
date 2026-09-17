# falsify-076 (H77) — FK guard repair / governor 負テスト は現 HEAD で着手済みか

## 仮説

H77: HEAD 41ac173 系列の後に core 側で修理が着手された (arm.cljk の FK 経路が
`within-limits?` を呼び、arm_test L20-22 の zero-fill 期待値が変わっている /
governor_test に不正 kind/safety の負テストが追加されている)。

## 実測 (純静的読取)

- terminal 実行 backend 応答不能 (echo を含む全コマンド空出力 — bench-225/226/227 と同一症状)
  + HOST LOAD 15min ≈107.12 ≈10.7× ncpu=10 で Load gate 大幅超過につき
  kbb -M:test / 暫定 kbb sci 経路 / seeded 再現は一律省略、test 計数 unmeasured
  (honest 据え置き、数字捏造ゼロ)。判定材料は read_file による現 blob 直読のみ。
- src/kotoba/giemon/arm.cljk (121 行, 現 blob 直読):
  - `within-limits?` は L15-20 defn のみ。FK 本体 `forward-kinematics`
    (L22-41) / `end-effector` (L43-46) 内部からの呼出 **0 回**。
  - L38 silent zero-fill `(angle (or (first angles) 0.0))` **不変**。
  - docstring L27-29「Check `within-limits?` first if that matters to the
    caller」自白不変 → FK 経路は越境 angles を silent 受理で pose を返す。
- test/kotoba/giemon/governor_test.cljk (47 行, 現 blob 直読): deftest 6 件
  全て正テスト。不正 kind / 不正 safety が nil で消える経路の負テスト **0 件**
  (rejected レコード化の痕跡なし) — falsify-071/072 の core 推奨は実装されていない。

## verdict: refuted

FK guard repair 未配線・governor 負テスト 0 件は現 blob でも不変 —
修理未着手を静的実測で再確定 (falsify-034 起の系列で計 33 連続 refuted)。
HEAD 再読は実行 backend 不能で本走はできず (41ac173 据え置き記録、変移は
否定も肯定もしない — honest)。test 計数 (clojure -M:test silent-zero 30 連続、
kbb 暫定経路 21/52/0) は unmeasured、bench-275/276 の実測記録に変更なしと推定。

## 再現手順

```
read_file src/kotoba/giemon/arm.cljk          # L15-20 defn のみ、L22-41 FK 内呼出 0、L38 zero-fill
read_file test/kotoba/giemon/governor_test.cljk  # deftest 6 件・負テスト 0
uptime                                        # 15min ≈107 ≈ 10.7× ncpu=10 → Load gate skip
```

## core への 1 行メッセージ

arm.cljk L22-41 に within-limits? 呼出 1 行 (または越境 throw) を入れて
arm_test L20-22 の期待値を fail に変え、governor_test に不正 kind/safety →
nil の rejected 負テスト 1 件を追加すれば両 OPEN 赤は即潰せる — runner 修復後の
re-baseline 前でも実装は可能。
