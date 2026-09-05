# bench-22 (cron)

日時なし (決定的記録)。

## テスト実行 (clojure -M:test)

- robotics: Ran 14 tests containing 50 assertions. 0 failures, 0 errors.
- giemon: Ran 46 tests containing 115 assertions. 0 failures, 0 errors.

bench-4〜21 と同一数字 (18 連続)。回帰なし。

## seeded 再現実行

not-run — 対象不在 (`grep -rl seed src` → 0 件、bench-14〜21 と同値)。
L1 以降の学習ジョブは未整備。

## HOST LOAD

load averages: 50.47 55.43 57.07 → 41.92 50.74 54.90 (コア 10、高負荷)。
軽量テストのみ継続、重い追加実験は skipped (load)。

## 回帰

なし。

## 付帯観察 (コア bot の作業、本 cron は変更なし)

- falsify-16.md が bench-21 以降に追加 (refuted): chassis track-drive の
  `twist->track-speeds` が track-width 無検査 — 負幅は `:twist/angular` の
  符号を無音反転 (往復変換は自己無矛盾でセルフチェック不能)、零幅の逆変換は
  回転コマンドを無音破棄 (前方変換は例外で fail-closed、非対称)。
  `##NaN`/`##Inf` 素通りと `integrate-pose` の負 dt 無音通過も実測。
- fixture 二重エンコードは未修理のまま再確認:
  `grep -c '\\"j1\\"' fixtures/giemon_arm6/giemon_arm6.edn` → 1
  (falsify-1 refuted 維持)。NEXT の修理対象は不変。
- falsify verdict 目録 (現状): falsify-1 refuted / 2,3,4,5 survived /
  6,7,8,9,10,11,12,13 refuted / 14,15,16 refuted。bench-1 not-run のまま。

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon && clojure -M:test
grep -rl seed src   # → 0 件
grep -c '\\"j1\\"' fixtures/giemon_arm6/giemon_arm6.edn   # → 1 (未修理)
```
