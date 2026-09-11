# bench-16

## テスト実行 (軽量テストは負荷高でも実施)

- `cd orgs/kotoba-lang/robotics && kbb -M:test`
  → Ran 14 tests containing 50 assertions. 0 failures, 0 errors.
- `cd orgs/kotoba-lang/giemon && kbb -M:test`
  → Ran 46 tests containing 115 assertions. 0 failures, 0 errors.

前回比: bench-4〜15 と同一数字 (robotics 14/50 + giemon 46/115)。回帰なし。

## seeded 再現実行

- 対象不在: `grep -rl seed orgs/kotoba-lang/giemon/src` → 0 件
  (bench-14/15 と同様、src 配下に seed を含むファイルなし)
- verdict: not-run (対象不在)

## 重い実験

- skipped (load): load averages 約 61→52 / コア 10 (bench-5〜15 と同方針)

## 回帰

- なし (テスト数 / assertion 数とも前回と一致、failures/errors 0)

## 再現コマンド

```sh
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon && kbb -M:test
grep -rl seed orgs/kotoba-lang/giemon/src | wc -l   # 0 → 再現対象不在
uptime                                               # 負荷確認
```
