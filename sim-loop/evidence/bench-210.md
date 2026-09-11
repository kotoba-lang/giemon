# bench-210 — skipped (load) — unmeasured

状態: HOST LOAD 超過により重い実験 (test スイート・seeded 再現) を省略。honest unmeasured。

## 判定

- verdict: **unmeasured / skipped (load)**
- HOST LOAD (execution時実測): up 3 days 21h、6 users。15-min 49.16 ≈ **4.9× ncpu** (hw.ncpu=10)
  (1-min 49.23 / 5-min 49.56)
- Load gate (~2× ncpu = 20) を大きく超過。bench-208 (≈5.1×, skipped)・bench-209 (≈4.2×, skipped) に
  続く高負荷帯 (実測完走帯は ~1.5-3×、最高 bench-207 ≈3.6×)。実行中 spike 増幅で backend 応答喪失の
  リスクを避け、重い `kbb -M:test` は skip → honest unmeasured。

## test スイート (robotics / giemon)

- kotoba-lang/robotics: 未実行 (skipped — load)
- kotoba-lang/giemon: 未実行 (skipped — load)

## seeded 再現 (L1+)

- not executed — sim-loop は L0 で seeded job 無し。本日も skip。

## git / ソース状態

- robotics: `9459ca0` (short) — 基準値 9459ca0 と一致 (tracked diff 空)
- giemon: `d0d3cb4` (short) — 基準値 d0d3cb4 と一致 (tracked diff 空)
- untracked は `?? sim-loop/` のみ。ソース変化なし。

## 回帰

- **assert しない** — unmeasured のため honest。基準値 (bench-066 確定: robotics 14/50/0、
  giemon 46/115/0) 据え置き。HEAD 両方は不変・tracked diff 空 (変化無し) であることのみ確認。

## falsify 状況

- HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空のため新規 falsify 発生なし。
  falsify-034〜037 (H35〜H38) の残存 (FK guard repair 未実装 / URDF probe 陳腐化) は変わらず。

## 再現コマンド

- (load 回復後の日次で): `cd .../kotoba-lang/robotics && kbb -M:test` → 基準 14/50/0、
  `cd .../kotoba-lang/giemon && kbb -M:test` → 基準 46/115/0、seeded L1+ 再現 (対象 job あれば)。

## メモ

- 負荷帯 ≈4.9× ncpu。bench-207 (≈3.6×, measured)・bench-208 (≈5.1×, skipped)・bench-209 (≈4.2×,
  skipped) にまたがって 4〜5× の高負荷が連日継続 (3 日目)。低負荷時間帯への cron 再配置を検討
  (要ユーザ判断)。