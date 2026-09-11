# giemon sim-loop bench 記録

## 概要
- 実行日: 2026-09-04 (JST) — cron (giemon-sim-bench)
- ホスト負荷: load averages 12.02 / 11.41 / 10.55 (ncpu=10) → **高負荷**
- 判定: 重い実験(seed 2 回再現の長時間実行)は **skipped (load)** として正直に記録。

## 1. テスト実行 (kbb -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && kbb -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && kbb -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ L1 以降)
- verdict: **skipped (load)**
- 理由: HOST LOAD が ncpu=10 に対し 1min avg 10.55–12.02 で高く、seeded 再現実行(同一 seed 2 回)は重いため省略。
- 補足: giemon リポジトリ内に sim-loop の学習ジョブ(seed/L1 以降)は現時点で存在せず、
  再現対象そのものが未実装の可能性もある(本実行では該当ジョブを発見できず)。
  負荷が下がった次回、seeded 再現実行の実装有無を再確認のうえ実施する。

## 3. 回帰の有無
- **回帰なし**(前回記録: evidence なし=初回ベースライン)。テスト 0 failures。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test
```

## 補足
- 本記録はタイムスタンプ非依存・決定的な内容のみ記載。
- コード修正は一切行っていない(ベンチ・記録のみ)。
