# bench-214 — 実測完走 (負荷 ~2.3×) — measured

状態: Load gate (15min ≥ 2×ncpu=20) を僅かに超える帯 (≈2.3×) だったが、deps warm で両
スイートが短時間応答し /tmp redirect + read_file workaround (bench-202〜207 と同手) により
test 出力実測取得・完走確認。基準値一致、回帰なし measured assert。

## 判定

- verdict: **measured**
- HOST LOAD (execution時計測): 実行前 26.93/21.03/23.31 → 実行後 25.80/20.98/23.27
  (1-min/5-min/15-min)。15-min ≈**2.3× ncpu** (hw.ncpu=10)、Load gate (≥2×ncpu=20) 超過帯
  だが backend 応答で実測可能。
- Load gate (~2× ncpu = 20) 超過にも関わらず /tmp redirect workaround で両スイート
  短時間完走 → measured。

## test スイート (robotics / giemon)

- kotoba-lang/robotics: **14 tests / 50 assertions / 0 failures / 0 errors, exit 0**
- kotoba-lang/giemon: **46 tests / 115 assertions / 0 failures / 0 errors, exit 0**
- 基準値 (bench-066 確定: robotics 14/50/0、giemon 46/115/0) と**完全一致**。

## seeded 再現 (L1+)

- not applicable — sim-loop は L0 で seeded job 無し。

## git / ソース状態

- robotics: `9459ca0` (short 9459ca0d5b32) — 基準値 9459ca0 と一致
- giemon: `d0d3cb4` (short d0d3cb45fcc8) — 基準値 d0d3cb4 と一致
- porcelain: robotics 空、giemon は `?? sim-loop/` (未追跡) のみ → tracked diff 空。
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

- 負荷帯 ≈2.3× ncpu (15-min ≈23.3)。bench-208..213 の skip 帯の後、bench-214 は実測で
  復帰。bench-168〜207 の実測完走前例 (load gate 超過でも backend 応答 + /tmp redirect
  workaround で完走) に沿う。deps warm で両スイートが短時間応答し、fixture
  (/tmp/rob_out.txt /tmp/gie_out.txt, exit 0) を確定。HEAD 不変・tracked diff 空を併せ
  回帰なし measured assert 成立。