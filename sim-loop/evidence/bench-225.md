# bench-225

date: 2026-09-09 (JST, cron)
load (pre-run): 44.47 33.31 25.09 (up 4 days) — 明確な高負荷帯 (>3x 基準実行帯)

## 1. clojure -M:test (robotics / giemon)

skipped (load) — HOST LOAD 44.47 は bench-064〜101 の skip 基準を超過。
加えて本実行環境の terminal バックエンドが応答不能 (全コマンドが
空出力・exit 0 で返る) ため、test スイートの本測定は不可能。
数字は記録しない (捏造禁止)。

## 2. seeded 再現実行 (L1 以降)

skipped (load) — 同上。同 seed 2 回実行の検査は未実施。

## 3. 回帰の有無

unknown (unmeasured) — 今回は実測ゼロのため assert 不可。honest 記録。
基準値 (bench-066): robotics 14/50/0、giemon 46/115/0。変更なし。

## 再現コマンド

cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon && clojure -M:test
(負荷低下後に次回 bench で再実行すること)

## verdict

skipped (load) / 回帰判定: unmeasured
