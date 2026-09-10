# bench-201 — measured (実測完走, 負荷 ~4.2×)

判定: **measured** — HOST LOAD ~4.2× ncpu ( hw.ncpu=10) と Load gate (~2×) を大きく超える高負荷帯だったが、backend 応答で /tmp redirect + read_file workaround により test スイート実測完走 (robotics ・ giemon 両方、exit 0 両方)。per-project 出力ファイル (/tmp/b_rob.txt, /tmp/b_gie.txt) 完走 fixture あり。

## 環境
- HOST LOAD: 実行終了時 1-min 23.40 / 5-min 26.98 / 15-min 42.21 (→約 4.2×)、up: 3 days 18h、6 users
- Load gate (~2×) 大幅超過帯だが、bench-200 (~7.4×)、bench-199 (~4.4×) と同様に backend 応答で実測取得可能だったため skip せず measured 記録。

## テスト数字 (per-project)
- kotoba-lang/robotics: **14/50/0**、exit 0 — 基準値 ( bench-066 確定) と完全一致
- kotoba-lang/giemon: **46/115/0**、exit 0 — 基準値 ( bench-066 確定) と完全一致

## git HEAD
- robotics: `9459ca0` (基準値 9459ca0 と一致、ソース変化なし)
- giemon: `d0d3cb4` (基準値 d0d3cb4 と一致、ソース変化なし)
- tracked diff 空 (`?? sim-loop/` のみ untracked)

## seeded 再現 verdict
- not-applicable (sim-loop は L0、job なし;L1 以降の seeded 再現は対象外。今回も seeded job 実行なし。)

## 回帰
- **なし (measured assert)** — 両スイートが基準値 ( bench-066 確定 / bench-200 最新実測) と完全一致 (robotics 14/50/0、giemon 46/115/0、両者 exit 0)、HEAD 両方不変・tracked diff 空。回帰なし。

## falsify 状況
- 前回 (bench-200) 同様据え置き — 今回新規 falsy なし、新仮説判定なし (code 無変更で判定対象なし)。HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空 (`?? sim-loop/` のみ)、FK guard repair 未着手のまま継続。ステータス正本 ( status/maturity.md) の NEXT は none のまま、継続。

## 再現コマンド
- (実測完走): `cd .../kotoba-lang/robotics && clojure -M:test` → 14/50/0 (exit 0)、`cd .../kotoba-lang/giemon && clojure -M:test` → 46/115/0 (exit 0)

## 備考
- 基準値は bench-066 確定 (robotics 14/50/0、giemon 46/115/0)。前回 bench-200/199/198 に続き high-load 帯 (≈4.2×) でも backend 応答で measured 実測完走 (robotics と giemon 両方完走)。回帰なし。
- コード変更なし (`?? sim-loop/` のみ untracked)。probe 類は bench/falsify 多数 md から参照され EVIDENCE のため削除せず。