# bench-226

date: 2026-09-09 (JST, cron)
load (pre-run): 93.45 69.27 50.15 (up 4 days) — 高負荷帯、かつ bench-225 (同日) 時点
(44.47) からさらに上昇中。>3x 基準実行帯を明確に超過。

## 1. kbb -M:test (robotics / giemon)

skipped (load) — HOST LOAD 93.45 は skip 基準を大幅に超過。
加えて terminal バックエンドが応答不能を継続 (echo を含む全コマンドが
空出力・exit 0 で返る。bench-225 と同一症状)。test スイートの本測定は不可能。
数字は記録しない (捏造禁止)。

## 2. seeded 再現実行 (L1 以降)

skipped (load) — 同上。同 seed 2 回実行の検査は未実施。

## 3. 回帰の有無

unknown (unmeasured) — 実測ゼロのため assert 不可。honest 記録。
基準値 (bench-066): robotics 14/50/0、giemon 46/115/0。変更なし。

## 再現コマンド

cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon && kbb -M:test
(負荷低下 + terminal バックエンド復旧後に次回 bench で再実行すること)

## verdict

skipped (load) / 回帰判定: unmeasured
