# bench-213 — skipped (load) — unmeasured

状態: HOST LOAD 超過により重い実験 (test スイート・seeded 再現) を省略。honest unmeasured。

## 判定

- verdict: **unmeasured / skipped (load)**
- HOST LOAD (execution時実測): up 3 days 22h33m、6 users。15-min **43.14** ≈ **4.3× ncpu**
  (hw.ncpu=10)。(1-min 19.50 / 5-min 29.24 を報告順に 15min 基準で 43.14)
- Load gate (~2× ncpu = 20) を超過 (≈4.3×)。下降傾向 (1-min ≈2.0×) だが 15-min
  基準では gate 超過継続。重い `kbb -M:test` は skip → honest unmeasured。

## test スイート (robotics / giemon)

- kotoba-lang/robotics: 未実行 (skipped — load)
- kotoba-lang/giemon: 未実行 (skipped — load)

## seeded 再現 (L1+)

- not executed — sim-loop は L0 で seeded job 無し。本日も skip。

## git / ソース状態

- robotics: `9459ca0` (short) — 基準値 9459ca0 と一致 (tracked diff 空、`git status --porcelain` 空)
- giemon: `d0d3cb4` (short) — 基準値 d0d3cb4 と一致 (tracked diff 空、`?? sim-loop/` のみ)
- ソース変化なし。

## 回帰

- **assert しない** — unmeasured のため honest。基準値 (bench-066 確定: robotics 14/50/0、
  giemon 46/115/0) 据え置き。HEAD 両方は不変・tracked diff 空 (変化無し) であることのみ確認。

## falsify 状況

- 最新 falsify-060 (H61): **refuted** — FK guard repair 依然未配線。`within-limits?` は
  arm.cljc L15-20 def / arm_test.cljc L28-30 単体 / docstring のみで、FK 経路
  (forward-kinematics L22-41 / end-effector L43-46) 内呼出 0 回、L38 silent zero-fill
  (`angle (or (first angles) 0.0)`) 不変、governor refs 0。HEAD 不変・tracked diff 空で
  repair 未着手 → NEXT (FK guard repair) 再発行継続。
- HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空のため新規 falsify 発生なし。

## 再現コマンド

- (load 回復後の日次で): `cd .../kotoba-lang/robotics && kbb -M:test` → 基準 14/50/0、
  `cd .../kotoba-lang/giemon && kbb -M:test` → 基準 46/115/0、seeded L1+ 再現 (対象 job あれば)。

## メモ

- 負荷帯 ≈4.3× ncpu (15-min)。bench-207 (≈3.6×, measured)・208 (≈5.1×, skipped)・209
  (≈4.2×, skipped)・210 (≈4.9×, skipped)・211 (≈14.6×, skipped)・212 (≈6.2×, skipped) に続き
  高負荷が継続。ただし本日は 1-min ≈2.0× まで下降しており負荷は回復傾向。1-min が
  gate (~2×) まで下がってきたため、次回以降は measured に復帰する可能性がある。
  低負荷時間帯への cron 再配置を引き続き検討 (要ユーザ判断)。