# bench-235

- load: 11.54 9.29 12.85 / hw.ncpu=10 → ~1.3x、heavy gate 未超過 → 実測実行
- robotics `kbb -M:test`: 14 tests / 50 assertions / 0 failures, 0 errors, RC=0 (基準値一致)
- giemon `kbb -M:test`: 46 tests / 115 assertions / 0 failures, 0 errors, RC=0 (基準値一致)
- robotics HEAD: 396fc33d0a6d51c52736231d333337e973e6fa98 (skill 記載の基準 HEAD 9459ca0 と異なる — テスト数は基準値一致のため回帰 assert せず、honest 記録として注記)
- giemon HEAD: d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe (基準一致)
- seeded 再現: not-applicable (sim-loop は L0、学習ジョブ無し)
- 回帰: なし
- falsify: falsify-037 (H38) refuted 済み、残存 open 無し
- コード変更: なし

再現コマンド:
```
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon && kbb -M:test
```
