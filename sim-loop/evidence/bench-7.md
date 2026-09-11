# giemon sim-loop bench — bench-7

日時: 2026-09-03T20:49:00+0900 (JST)

## HOST LOAD

- load averages: **25.77 20.24 19.96** (uptime, 10 cores)。bench-6 時点 (11.68 14.84 15.85)
  からさらに上昇し、1min はコア数の約 2.5 倍 / 5・15min は約 2 倍。bench-6 の引き継ぎ条項
  (1min がコア数の約 2 倍を明確に超えて続く場合はテスト維持・重い追加実験は skipped (load))
  に該当する水準。方針どおり **テスト 2 件 (軽量) と学習ジョブ存在確認のみ実行**し、
  重い追加実験は **skipped (load)**。seeded 再現は対象不在のため not-run (下記)。

## テスト実行 (kbb -M:test)

- robotics: **実行済み** — `Ran 14 tests containing 50 assertions. 0 failures, 0 errors.`
- giemon: **実行済み** — `Ran 46 tests containing 115 assertions. 0 failures, 0 errors.`
- 合計: **60 tests / 165 assertions / 0 failures / 0 errors**。

## 前回比 / 回帰の有無

- 比較基準: bench-6 (robotics 14/50, giemon 46/115)。bench-4/5/6 と同一数字。
- robotics 14 tests / 50 assertions — **変化なし**。
- giemon 46 tests / 115 assertions — **変化なし**。
- **回帰なし** (数値一致, 0 failures / 0 errors のまま)。新規赤なし。
- 既存 OPEN 赤 (falsify-1 refuted: fixtures/giemon_arm6 EDN のダブルエンコード) に変化なし。
  NEXT (falsify-1 の修理) は本 bot の守備範囲外 (コード修正しない) のため未着手のまま。

## seeded 再現実行 (L1 以降)

- **not-run** — seeded 学習ジョブは未整備 (maturity: 再現性 score 0, 現在段階 L0)。
  giemon/src/kotoba/giemon/ 配下は arm / chassis / export / governor / kinematics / ui /
  viewer のみ (ls で再確認) で学習パイプラインのソースは存在せず、src 配下に `seed` を
  含むファイルも grep で 0 件。同一 seed で 2 回実行して一致を検査すべき対象が存在しない。
- 重い追加実験 (seeded 再現以外の負荷実験類): **skipped (load)** — 上記 HOST LOAD のとおり。

## 再現コマンド

```
uptime
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon  && kbb -M:test
ls orgs/kotoba-lang/giemon/src/kotoba/giemon/   # seeded 学習ジョブ不在の確認
grep -rl "seed" orgs/kotoba-lang/giemon/src/
```

(本記録では uptime / 2 つの clojure コマンド / ls / grep を実行済み。出力は各節に記載。)

## 次回への引き継ぎ

- 比較基準は bench-4〜7 と同一 (robotics 14/50, giemon 46/115)。減少・failure 増は
  回帰として赤記録すること。
- seeded 再現は maturity の再現性スコアが 0 の間は not-run と正直に記録する。
- 負荷が 1min でコア数の約 2 倍を明確に超えて続く場合は、テストは維持しつつ重い
  追加実験は「skipped (load)」と記録する方針を継続 (本回適用)。
