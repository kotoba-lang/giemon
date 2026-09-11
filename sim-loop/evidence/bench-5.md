# giemon sim-loop bench — bench-5

日時: 2026-09-03T19:18:00+0900 (JST)

## HOST LOAD

- load averages: **18.12 17.54 17.53** (uptime, 10 cores)。bench-4 時点 (13.25) から
  上昇して 1min がコア数の約 1.8 倍。重い実験類は省略したが、テスト実行自体は
  bench-3/bench-4 の引き継ぎ指示 (4 連続 skip 防止、毎回実行して前回比を取る) に従い
  実行した。テストは数百 ms〜秒程度の軽量実行であり負荷の追加影響は小さいと判断。

## テスト実行 (kbb -M:test)

- robotics: **実行済み** — `Ran 14 tests containing 50 assertions. 0 failures, 0 errors.`
- giemon: **実行済み** — `Ran 46 tests containing 115 assertions. 0 failures, 0 errors.`
- 合計: **60 tests / 165 assertions / 0 failures / 0 errors**。

## 前回比 / 回帰の有無

- 比較基準: bench-4 (robotics 14/50, giemon 46/115)。
- robotics 14 tests / 50 assertions — **変化なし**。
- giemon 46 tests / 115 assertions — **変化なし**。
- **回帰なし** (数値一致, 0 failures / 0 errors のまま)。新規赤なし。
- 既存 OPEN 赤 (falsify-1 refuted: fixtures/giemon_arm6 EDN のダブルエンコード) に変化なし。
  NEXT (falsify-1 の修理) は本 bot の守備範囲外 (コード修正しない) のため未着手のまま。

## seeded 再現実行 (L1 以降)

- **not-run** — seeded 学習ジョブは未整備 (maturity: 再現性 score 0, 現在段階 L0)。
  同一 seed で 2 回実行して一致を検査すべき対象が存在しないため実行不可。
  負荷本回は問題にならず (テストは実行済み)、対象不在が理由。

## 再現コマンド

```
uptime
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon  && kbb -M:test
```

(本記録では上記 2 つの clojure コマンドを実行済み。出力は「テスト実行」節に記載。)

## 次回への引き継ぎ

- 比較基準は bench-4/bench-5 と同一 (robotics 14/50, giemon 46/115)。減少・failure 増は
  回帰として赤記録すること。
- seeded 再現は maturity の再現性スコアが 0 の間は not-run と正直に記録する。
- 負荷が 1min でコア数の約 2 倍を明確に超えて続く場合は、テストは維持しつつ重い
  追加実験は「skipped (load)」と記録する方針を継続。
