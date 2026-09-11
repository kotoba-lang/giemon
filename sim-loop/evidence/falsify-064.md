# falsify-064 (H65) — FK guard repair 未配線 (26 連続 refuted)

- 仮説: 「FK guard repair は直近 iteration で実装・配線された」— 反証対象は
  kotoba.giemon.arm の FK 経路が joint limit 越境 angles を guard (`within-limits?`)
  なしで silent 受理するという未修繕主張 (NEXT: FK guard repair)。
- 実測 (純静的読取。git/grep/sed は /tmp redirect workaround で取得、数字捏造ゼロ):
  - HEAD giemon `d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe` 不変
    (falsify-062/063 と同一 commit)。`git status --porcelain`: `?? sim-loop/` のみ、
    tracked diff 空 — コード変更なし。
  - `within-limits?` 出現箇所 (arm.cljc): **2 行のみ** — L15 (defn 定義) と
    L28 (docstring 内言及 "Check `within-limits?` first")。FK 経路
    (`forward-kinematics` / `end-effector`) 本体内部からの呼出 **0 回**。
  - silent zero-fill `(angle (or (first angles) 0.0))` が loop 本体に**不変で残存**
    — 越境/欠損 angles を 0.0 で silent 受理し pose を返す。
  - docstring 自白不変: "an angle outside a joint's declared limit still produces a
    pose. Check `within-limits?` first if that matters to the caller."
  - arm_test.cljc「missing angles default to 0.0」緑 assertion (silent zero-fill
    固定期待値) 不変・期待値変更なし。
  - governor.cljc の arm/limit/torque/joint 参照行: **0 行**
    (gate 迂回 shortcut は falsify-057 で src 内不存在確定済み)。
- verdict: **refuted** — FK guard repair は依然未配線。越境 angles は silent 受理で
  pose 返却。falsify-034/036/039〜063 と同根 (falsify-057 は別系)・**26 連続 refuted**。
- HOST LOAD: 開始時 44.47/33.31/25.09 → 測定中 43.30/35.58/27.07
  (~4.3× ncpu=10) で load gate 超過 → 重い test 実行・seeded 再現は省略し
  unmeasured (honest 据え置き)。純テキスト照合ゆえ負荷の測定影響はゼロ。
- 再現手順:
  ```sh
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  git rev-parse HEAD    # d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe
  git status --porcelain   # ?? sim-loop/ のみ
  grep -n "within-limits?" src/kotoba/giemon/arm.cljk  # L15, L28 のみ
  sed -n '22,46p' src/kotoba/giemon/arm.cljk  # zero-fill 不変, guard 呼出 0 回
  sed -n '18,24p' test/kotoba/giemon/arm_test.cljk
  grep -cE "arm|limit|torque|joint" src/kotoba/giemon/governor.cljk  # 0
  ```
- コアへの 1 行: guard は 26 iterations 丸ごと未配線 — `within-limits?` を FK 経路に
  繋ぐか越境入力で fail-loud にする repair を実装しない限りこの赤は消えない。
