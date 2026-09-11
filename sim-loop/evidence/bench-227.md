# bench-227

date: 2026-09-09 (JST, cron)
load (pre-run): 16.53 19.75 23.60 (up 4 days, 5:47) — pre-run script による HOST LOAD。
1分値 16.53 は bench-225 (44.47) / bench-226 (93.45) から大幅に低下しており、
過去の実行帯 (~1.5-3x, bench-102〜108 が完走した帯) に戻りつつある。ただし 15分値
23.60 は依然高く、減衰途上と判断。

## 1. kbb -M:test (robotics / giemon)

skipped (execution backend) — 本イテレーションでは HOST LOAD は低下したが、
terminal 実行バックエンドが継続応答不能 (bench-225/226 と同一症状: すべての
コマンドが空出力・exit 0 で返る。echo / /usr/bin/uptime / /bin/date を含む
発煙なしコマンドでも本測定出力ゼロ)。kbb -M:test の起動・結果取得が
不可能なため本測定は実施できず、数字は記録しない (捏造禁止)。

代替経路も確認: execute_code は cron モードで承認ブロック、browser_exec 経由の
subprocess も同様に TUI 起動失敗 (exit 1、出力ゼロ)。

## 2. seeded 再現実行 (L1 以降)

skipped (execution backend) — 同上。同 seed 2 回実行の検査は未実施。

## 3. 回帰の有無

unknown (unmeasured) — 実測ゼロのため assert 不可。honest 記録。
基準値 (bench-066): robotics 14/50/0、giemon 46/115/0。変更なし。

## 再現コマンド

cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon && kbb -M:test
(terminal バックエンド復旧後、負荷 1分値が実行帯に戻った時点で次回 bench で再実行)

## verdict

skipped (execution backend) / 回帰判定: unmeasured
