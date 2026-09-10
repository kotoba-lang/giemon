# bench-208 — skipped (load) — unmeasured

状態: HOST LOAD 超過により重い実験 (test スイート・seeded 再現) を省略。honest unmeasured。

## 判定

- verdict: **unmeasured / skipped (load)**
- HOST LOAD (pre-run): up 3 days 21h、6 users。15-min 50.62 ≈ **5.1× ncpu** (hw.ncpu=10)
  (執行時実測 15-min 48.57 ≈ 4.9×、1-min 35.15 / 5-min 48.76)
- Load gate (~2× ncpu = 20) を大きく超過。bench-207 (measured ≈3.6×) よりさらに高負荷帯。
  重い `clojure -M:test` 実行は skip (実行中 spike が数倍に増幅し backend 応答喪失リスク) → honest unmeasured。

## test スイート (robotics / giemon)

- kotoba-lang/robotics: 未実行 (skipped — load)
- kotoba-lang/giemon: 未実行 (skipped — load)

## seeded 再現 (L1+)

- not executed — sim-loop は L0 で seeded job 無し。本日も skip。

## git / ソース状態

- robotics: `9459ca0d5b3126472e23de6a77f725a9a3480770` — 基準値 9459ca0 と一致
- giemon: `d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe` — 基準値 d0d3cb4 と一致
- tracked diff 空、untracked は `?? sim-loop/` のみ。ソース変化なし。

## 回帰

- **assert しない** — unmeasured のため honest。基準値 (bench-066 確定: robotics 14/50/0、giemon 46/115/0)
  据え置き。HEAD 両方は不変・tracked diff 空 (変化無し) であることのみ確認。

## falsify 状況

- HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空のため新規 falsify 発生なし。
  falsify-034〜037 (H35〜H38) の残存 (FK guard repair 未実装 / URDF probe 陳腐化) は変わらず。

## 再現コマンド

- (load 回復後の日次で): `cd .../kotoba-lang/robotics && clojure -M:test` → 基準 14/50/0、
  `cd .../kotoba-lang/giemon && clojure -M:test` → 基準 46/115/0、seeded L1+ 再現 (対象 job あれば)。

## メモ

- 負荷帯が bench-207 (≈3.6×, measured) を上回る ≈4.9-5.1×。skill gate (~2×) 超過。
  数日連続で高負荷が続く場合は、低負荷時間帯への cron 再配置を検討 (要ユーザ判断)。