# bench-10 (日次連番 10)

日時なし (決定的記録方針)。

## HOST LOAD
uptime load averages: 15.10 18.55 21.26 / コア 10 → 負荷高水準。

## テスト実行 (`kbb -M:test`)

- orgs/kotoba-lang/robotics: `Ran 14 tests containing 50 assertions. 0 failures, 0 errors.` (exit 0)
- orgs/kotoba-lang/giemon: `Ran 46 tests containing 115 assertions. 0 failures, 0 errors.` (exit 0)

### 回帰判定
bench-4〜9 と同一数字 (robotics 14/50 + giemon 46/115, 0 failures 0 errors)。
**回帰なし** (7 連続で同一数字を確認)。

## seeded 再現実行
対象不在のため **not-run**。再確認: giemon/src 配下の .clj/.cljc ファイルで `seed` を含むもの 0 件
(search_files `seed` on src → total_count 0)。学習ジョブ (L1 以降) が未実装のため seeded 再現は不可。
重い追加実験は **skipped (load)** (load 約 15-21 / コア 10)。

## 再現コマンド
```
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon && kbb -M:test
```

## 結論
- テスト: robotics 14/50, giemon 46/115, failures 0, errors 0
- 再現 verdict: not-run (seeded 対象不在)
- 回帰: なし
- NEXT は不変: falsify-1 の修理 (fixtures/giemon_arm6/giemon_arm6.edn の
  :arm/chain / :arm/realization / :arm/base のダブルエンコード解消)
  + 副として falsify-6 の `arm/bom` nil 時 fail-closed 化。
