# bench-215 — 実測完走 (負荷 ~2.3×, execution時 spike) — measured

状態: Load gate (15min ≥ 2×ncpu=20) を超える帯 (≈2.3×) だったが、deps warm で両スイートが
短時間応答し /tmp redirect + read_file workaround (bench-202〜207・214 と同手) により test
出力実測取得・完走確認。基準値一致、回帰なし measured assert。

## 判定

- verdict: **measured**
- HOST LOAD (実行前時計測): 19.91/21.41/22.73 (1-min/5-min/15-min)。15-min ≈**2.3× ncpu**
  (hw.ncpu=10)。bench 中に報告順 (rob件後 48.35, gie件後 59.50) と spike 上振れも見たが
  両スイートとも短時間完走 (exit 0)。
- Load gate (~2× ncpu = 20) 超過帯にも関わらず /tmp redirect workaround で両スイート
  完走 → measured。

## test スイート (robotics / giemon)

- kotoba-lang/robotics: **14 tests / 50 assertions / 0 failures / 0 errors, exit 0**
- kotoba-lang/giemon: **46 tests / 115 assertions / 0 failures / 0 errors, exit 0**
- 基準値 (bench-066 確定: robotics 14/50/0、giemon 46/115/0) と**完全一致**。

## seeded 再現 (L1+)

- not applicable — sim-loop は L0 で seeded job 無し。

## git / ソース状態

- robotics: `9459ca0` — 基準値 9459ca0 と一致 (tracked diff 空、`git status --porcelain` 空)
- giemon: `d0d3cb4` — 基準値 d0d3cb4 と一致 (tracked diff 空、`?? sim-loop/` のみ)
- ソース変化なし。

## 回帰

- **回帰なし (measured assert)** — 基準値 14/50/0 / 46/115/0 と完全一致。HEAD 両方不変・
  tracked diff 空。

## falsify 状況

- 最新 falsify-060 (H61): **refuted** — FK guard repair 依然未配線。HEAD 不変・tracked diff
  空 (?? sim-loop/ のみ) で repair 未着手 → NEXT (FK guard repair) 再発行継続。
- HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空のため新規 falsify 発生なし。

## 再現コマンド

- `cd .../kotoba-lang/robotics && clojure -M:test` → 基準 14/50/0 (本日 exit 0)
- `cd .../kotoba-lang/giemon && clojure -M:test` → 基準 46/115/0 (本日 exit 0)
- seeded L1+ 再現: sim-loop が L0 のため対象 job 無し。

## メモ

- 開始時 15-min ≈2.3× (22.73)。spike (1-min 48.35→59.50) も両スイート短時間完走。
  bench-214 (≈2.3×, measured) と同帯で、bench-208〜213 の skip 帯を脱し measured 継続。
  deps warm + /tmp redirect workaround が有効。HEAD 不変・tracked diff 空を併せ
  回帰なし measured assert 成立。