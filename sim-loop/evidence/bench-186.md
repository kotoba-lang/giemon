# bench-186 — measured

判定: **measured** (kbb -M:test 実測完走。HOST LOAD 高めだが両スイート応答・基準値一致 → 回帰なし)

## 環境
- HOST LOAD: 実行完了時 15-min ≈ 31.5 / 5-min ≈ 22.3 / 1-min ≈ 15.7 (hw.ncpu = 10 → ~3.2×)
- 負荷帯は gate (2×) 超過域だが、本実行は非応答域ではなく両スイート完走・基準値一致を実測できた
- up: 3 days 13h; 8 users

## テスト数字 (per-project)
- kotoba-lang/robotics: **14 tests / 50 assertions / 0 failures / 0 errors** (exit 0) — 基準値 14/50/0 と一致
- kotoba-lang/giemon: **46 tests / 115 assertions / 0 failures / 0 errors** (exit 0) — 基準値 46/115/0 と一致

## git HEAD
- robotics: `9459ca0` (基準値 9459ca0 と一致、変化なし)
- giemon: `d0d3cb4` (基準値 d0d3cb4 と一致、変化なし)

## seeded 再現 verdict
- not-applicable (sim-loop は L0、job なし。L1 以降の seeded 再現は対象外。今回も seeded job 実行なし)

## 回帰
- なし (両スイート基準値と一致・exit 0・HEAD 変化なし → 回帰兆候なし)
- sim-loop/ は untracked (`??`) のみでソース変更なし

## falsify 状況
- falsify-034/035/036/037 (H35〜H38) は既決済み (refuted)。新規 falsify なし (maturity NEXT = none)。

## 再現コマンド
- `cd .../kotoba-lang/robotics && kbb -M:test` → 14/50/0
- `cd .../kotoba-lang/giemon && kbb -M:test` → 46/115/0

## 備考
- bench-185 は load-skip (unmeasured) だったが、bench-186 は負荷がやや低下 (15-min ≈31.5) し実測可能域に戻った。
  基準値は bench-066 確定 (robotics 14/50/0、giemon 46/115/0)。
- コード変更なし (`?? sim-loop/` のみ untracked)。
