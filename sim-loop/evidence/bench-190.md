# bench-190 — measured

判定: **measured** (clojure -M:test 実測完走。HOST LOAD は高め (15-min ≈ 2.9×) だが両スイートとも短時間で応答し、基準値 (bench-066 確定) と完全一致 → 回帰なし)

## 環境
- HOST LOAD: 実行完了時 15-min ≈ 28.94 / 5-min ≈ 20.01 / 1-min ≈ 19.70 (hw.ncpu = 10 → 15-min ≈ 2.9×)
- 負荷帯は下降傾向 (1-min < 5-min < 15-min)。precedent bench-186 (3.2× で measured 完走) と同水準の実測可能域と判断して実行。
- up: 3 days 14h; 6 users

## テスト数字 (per-project)
- kotoba-lang/robotics: **14 tests / 50 assertions / 0 failures** (exit 0)
- kotoba-lang/giemon: **46 tests / 115 assertions / 0 failures** (exit 0)
- 基準値 (bench-066): robotics 14/50/0、giemon 46/115/0 → **両方一致**

## git HEAD
- robotics: `9459ca0` (基準値 9459ca0 と一致、ソース変化なし)
- giemon: `d0d3cb4` (基準値 d0d3cb4 と一致、ソース変化なし)

## seeded 再現 verdict
- not-applicable (sim-loop は L0、job なし。L1 以降の seeded 再現は対象外。今回も seeded job 実行なし)

## 回帰
- **なし** (robotics 14/50/0、giemon 46/115/0、両方 exit 0、基準値と完全一致)
- HEAD は両方基準値と一致、`?? sim-loop/` のみ untracked でソース変更なし

## falsify 状況
- falsify-034/035/036/037 (H35〜H38) は既決済み (refuted)。新規 falsify なし (maturity NEXT = none)。これまでの falsify 状況に変化なし。

## 再現コマンド
- `cd .../kotoba-lang/robotics && clojure -M:test` → robotics 14/50/0 (今回 RC=0)
- `cd .../kotoba-lang/giemon && clojure -M:test` → giemon 46/115/0 (今回 RC=0)

## 備考
- 実行完了時点で 15-min 28.94 (2.9×)、5-min 20.01、1-min 19.70 と下降中。deps が warm (classpath/コンパイル済) のため両スイートとも短時間 (robotics ~6s, giemon ~5s) で完走した。
- bench-188 (3.8×)/bench-189 (4.5×) は unmeasured だったが、今回 2.9× と load が下がり実測復帰。負荷が再上昇しない限り次回以降も実測継続可能な見込み。
- コード変更なし (`?? sim-loop/` のみ untracked)。probe 類は bench/falsify 多数 md から参照され EVIDENCE のため削除せず。