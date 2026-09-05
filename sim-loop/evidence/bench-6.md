# giemon sim-loop bench — bench-6

日時: 2026-09-03T19:47:00+0900 (JST)

## HOST LOAD

- load averages: **11.68 14.84 15.85** (uptime, 10 cores)。bench-5 時点 (12.82 15.49 16.12)
  から 1min はやや低下したが 5/15min は高水準のまま (コア数の約 1.2〜1.6 倍)。
  bench-5 と同方針: テスト実行 (軽量) は維持、重い実験類は省略。本回実行したのは
  テスト 2 件と学習ジョブ存在確認 (grep/ls) のみ。重い実験は skipped (load) ではないが
  seeded 再現が対象不在のため not-run (下記)。

## テスト実行 (clojure -M:test)

- robotics: **実行済み** — `Ran 14 tests containing 50 assertions. 0 failures, 0 errors.`
- giemon: **実行済み** — `Ran 46 tests containing 115 assertions. 0 failures, 0 errors.`
- 合計: **60 tests / 165 assertions / 0 failures / 0 errors**。

## 前回比 / 回帰の有無

- 比較基準: bench-5 (robotics 14/50, giemon 46/115)。
- robotics 14 tests / 50 assertions — **変化なし**。
- giemon 46 tests / 115 assertions — **変化なし**。
- **回帰なし** (数値一致, 0 failures / 0 errors のまま)。新規赤なし。
- 既存 OPEN 赤 (falsify-1 refuted: fixtures/giemon_arm6 EDN のダブルエンコード) に変化なし。
  NEXT (falsify-1 の修理) は本 bot の守備範囲外 (コード修正しない) のため未着手のまま。

## seeded 再現実行 (L1 以降)

- **not-run** — seeded 学習ジョブは未整備 (maturity: 再現性 score 0, 現在段階 L0)。
  giemon/src/kotoba/giemon/ 配下に arm / chassis / export / governor / kinematics / ui /
  viewer のみで学習パイプラインのソースは存在しない (ls で再確認済み)。
  同一 seed で 2 回実行して一致を検査すべき対象が存在しないため実行不可。
  負荷は本回テスト実行を阻害しなかった。

## 再現コマンド

```
uptime
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon  && clojure -M:test
ls orgs/kotoba-lang/giemon/src/kotoba/giemon/   # seeded 学習ジョブ不在の確認
```

(本記録では uptime / 2 つの clojure コマンド / ls を実行済み。出力は各節に記載。)

## 次回への引き継ぎ

- 比較基準は bench-4/bench-5/bench-6 と同一 (robotics 14/50, giemon 46/115)。減少・
  failure 増は回帰として赤記録すること。
- seeded 再現は maturity の再現性スコアが 0 の間は not-run と正直に記録する。
- 負荷が 1min でコア数の約 2 倍を明確に超えて続く場合は、テストは維持しつつ重い
  追加実験は「skipped (load)」と記録する方針を継続。
