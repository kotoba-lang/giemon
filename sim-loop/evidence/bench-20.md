# bench-20 (cron, 決定的記録)

## テスト実行

- robotics: `kbb -M:test` → Ran 14 tests containing 50 assertions. 0 failures, 0 errors.
- giemon:   `kbb -M:test` → Ran 46 tests containing 115 assertions. 0 failures, 0 errors.

前回 (bench-4〜19) と同一数字: robotics 14/50 + giemon 46/115, 0 failures 0 errors。
回帰なし。

## seeded 再現実行

対象不在のため not-run (`grep -rl seed src` → 0 件、bench-14〜19 と同様)。
シミュレーション学習コードなし (src/kotoba/giemon/ は arm/chassis/export/governor/kinematics/ui/viewer のみ)。

## HOST LOAD

load 約 60-61 / 15分平均 約 54 (コア 10 相当比で高負荷)。軽量テストは維持し、重い追加実験は skipped (load)。

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon && kbb -M:test
grep -rl seed orgs/kotoba-lang/giemon/src   # → 0 件
```
