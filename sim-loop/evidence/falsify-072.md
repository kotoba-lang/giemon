# falsify-072 (H73) — governor silent-nil 負テスト / rejected レコード化は実装済みか

## 仮説
H73: falsify-071 (H72) が core へ推奨した「`kotoba.robotics/action` の silent nil
返却を rejected レコード化し、不正 kind/safety の負テストを 1 件追加」は、
maturity.md NEXT に明記されて以降、core 側 (governor / governor_test) で
既に実装されている可能性。

## 実測 (純静的読取 — 実行 backend 応答不能につき clojure/kbb 実測は本 run 不可)

- 実行系: `terminal` backend 応答不能 (echo 空返し・6 連続 RC 表示なし)。HOST LOAD
  (pre-run script): 15min 14.35 ≈ 1.4× ncpu=10 → gate 内だが実測経路が物理不能。
  純静的読取のみで決着 (falsify-024〜030 流儀)。
- `test/kotoba/giemon/governor_test.cljk` 全 47 行読了:
  deftest 6 件 = kaigo-mission / kaigo-action-defaults /
  fall-detected-alert / ops-mission / ops-action-defaults /
  chemical-dispense-alert。**不正 kind (:teleport 等)・不正 safety
  (:none-of-the-above 等) を与える負テストは 0 件** (falsify-071 記載 L11-20
  :move のみ網羅から増えていない)。
- `src/kotoba/giemon/governor.cljk` 全 68 行読了: `kaigo-action` L25-27 /
  `ops-action` L58-60 は `rob/action` 透過のまま — rejected レコード化
  (ex-data / 拒否記録) の痕跡なし。`fall-detected-alert` /
  `chemical-dispense-alert` の :safety-critical ハードコードも不変。
- `kotoba/robotics` のローカルソース (robotics.cljk / robotics.cljc) は
  giemon repo / kotoba-lang repo いずれの探索パスにも不在 (deps floor 座標のみ) —
  robotics/action 本体の rejected 化は本 repo 静的範囲から観測不能。
- falsify-068 静的点と同様、HEAD 進行の確認は本 run の backend 不応で不可
  (bench-252〜 まで 00fd23f / ad99366 据え置き観測が最後)。

## verdict: **refuted** —「silent-nil 修正は実装済み」は成り立たない。
governor_test.cljk の負テスト 0 件・governor.cljk の透過は falsify-071 時点と
同値で不変。不正 kind/safety は引き続き silent nil で落ち、audit 痕跡なし。
(注: robotics 本体は deps 先で静的範囲外につき、rejected 化自体の有無は
本 repo からは観測不能 — 負テスト 0 件の点のみ決定的。)

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
cat test/kotoba/giemon/governor_test.cljk          # 負テスト 0 件
grep -n "ex-data\|rejected\|deny" src/kotoba/giemon/governor.cljk  # 0 行
# 実行 (backend 応答可能時):
#   (gov/kaigo-action "A" "M" :otete :teleport)  ; => nil (痕跡なし)
```

no code change (本 bot は修正しない)。

コアへの 1 行メッセージ: governor の silent-nil 経路は推奨後も未修正
(負テスト 0 件・透過不変) — runner repair と同時に rejected レコード化 +
負テスト 1 件を core 側へ (falsify-071 推奨の再発行)。
