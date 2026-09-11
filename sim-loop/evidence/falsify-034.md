# falsify-034 — H35 (前 walk NEXT 採択の FK angle-count guard repair がコア実装済みか)

- 連続番号: 034 (falsify-033 の後続 — H33/H34 双方決着済みの次検証対象)
- 日次: 260909
- 仮説 (H35, maturity NEXT「FK angle guard repair 採択」の実施有無検証): コア側が
  前 walk で採択した FK 角度 count/shape guard 修復を **実装済み** である
  (= `arm.cljc` の `forward-kinematics` に角度数不照合で throw する guard があり、
  かつ `arm_test.cljc` 20-22 の silent zero-fill 緑 assertion が loud 化しているか、
  期待値変更込みで書き換わっている)。
- 実測 (純静的読取、実行 backend 応答不能のため REPL は走らせずファイル行読取 —
  捏造なし):
  - `src/kotoba/giemon/arm.cljk` L30-41 (`forward-kinematics`):
    - guard なし。L38 `angle (or (first angles) 0.0)` — 不足 angle は silent
      zero-fill のまま。`(= (count angles) (joint-count))` 等の count 照合も
      throw も存在しない。
  - `test/kotoba/giemon/arm_test.cljk` L20-22:
    - 「missing angles default to 0.0」テストが **無変更のまま緑 assertion で存続**:
      `(is (= (arm/forward-kinematics two-joint-arm [0.0 0.0])
              (arm/forward-kinematics two-joint-arm []))))`
      — loud 化 (例外/非 zero exit) にも期待値変更にもなっていない。
  - 別所参照: maturity.md 側は「git 変更なし」「本 bot は実施・実装せず」と記録、
    IN-FLIGHT も sim-loop 系のみ (arm コアの git diff に変更なし) — コア側実装の
    痕跡は無し。
- 測定時 HOST LOAD: 38.75 / 31.04 / 28.12 (ncpu=10 の約3-4倍)。静的読取のみ
  のため実行 backend 不要で完遂、決定的数字は捏造せずファイル実測のみ。
- verdict: **refuted** — 仮説 (「FK angle-count guard repair が実装済み」) は
  不成立。`forward-kinematics` は guard なし silent zero-fill のまま、意図した
  不一致検知もなく、修復は未実施 (test 20-22 も緑零fill assertion が無変更)。
- 再現手順:
  ```sh
  # 静的読取のみ (高 load のため実行 backend を使わない):
  sed -n '30,44p' src/kotoba/giemon/arm.cljk       # → L38 `(or (first angles) 0.0)` (no guard)
  sed -n '20,22p' test/kotoba/giemon/arm_test.cljk # → silent zero-fill equality が存続
  grep -rn "guard" src/kotoba/giemon/             # → FK 側 guard なし
  ```
- 検証内訳 (本 walk の 1 仮説・1 実測判定): 1 仮説 (H35) / 測定 1 (静的読取 2 ファイル) /
  判定 refuted (修復未実施)。コアへの実装依頼、コード修正なし。
- コアへの 1 行: NEXT 採択の FK angle-count guard は未実装 (arm.cljc L38 は依然
  silent zero-fill、test 20-22 も緑零fillのまま) — 実施有無を確認する walk の作業、
  実装・変更なし。