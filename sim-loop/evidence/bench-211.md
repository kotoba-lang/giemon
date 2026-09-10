# bench-211 — skipped (load) — unmeasured

状態: HOST LOAD 超過により重い実験 (test スイート・seeded 再現) を省略。honest unmeasured。

## 判定

- verdict: **unmeasured / skipped (load)**
- HOST LOAD (execution時実測): up 3 days 22h03m、6 users。15-min **146.34** ≈ **14.6× ncpu**
  (hw.ncpu=10)。(1-min 146.34 / 5-min 107.58 を報告順に 15min 基準で 146.34)
- Load gate (~2× ncpu = 20) を大幅超過 (≈14.6×)。本系列最大負荷帯。実行中 spike 増幅で
  backend 応答喪失リスクが極大 (素の `uptime`/`ls` すら 60s timeout で応答喪失を観測)。
  重い `clojure -M:test` は skip → honest unmeasured。

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
  repair 未着手 → NEXT (FK guard repair) 再発行継続。falsify-034/036/039〜056/058/059 と同根
  (falsify-057 は FK shortcut 仮説で別系)。
- HEAD giemon d0d3cb4 / robotics 9459ca0 不変・tracked diff 空のため新規 falsify 発生なし。

## 再現コマンド

- (load 回復後の日次で): `cd .../kotoba-lang/robotics && clojure -M:test` → 基準 14/50/0、
  `cd .../kotoba-lang/giemon && clojure -M:test` → 基準 46/115/0、seeded L1+ 再現 (対象 job あれば)。

## メモ

- 負荷帯 ≈14.6× ncpu (本系列最大)。bench-207 (≈3.6×, measured)・208 (≈5.1×, skipped)・
  209 (≈4.2×, skipped)・210 (≈4.9×, skipped) に続き、4〜14× の高負荷が数日にわたり継続・悪化。
  素の read/uptime が 60s timeout するほど backend が応答喪失気味。低負荷時間帯への cron
  再配置を強く検討 (要ユーザ判断)。