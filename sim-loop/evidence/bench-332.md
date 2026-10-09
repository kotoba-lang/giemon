# bench-332

判定: **skipped (load)** — 全経路 (clojure -M:test 両 suite / seeded 再現) skipped (load) unmeasured。

## 負荷
- 実行前 uptime 実測: 1-min 55.81 / 5-min 60.34 / 15-min 60.20 / ncpu 10 (sysctl 実測) ≈ **6.0×** (gate 15-min ≥ 2×ncpu=20 を大幅超過 → 実行省略)。
- 前走実測帯 55–61 前後で高負荷が持続 (uptime 2 回実測: 4:04 時点 61.02/61.37/60.46、4:06 時点 55.81/60.34/60.20 — いずれも gate 超過)。
- terminal stdout swallow (既知) につき全 live 測定は scratch redirect + read_file で実施。

## test スイート
- 未実施 (load gate 超過・honest)。clojure 主経路 silent-zero は本走未検証 (bench-244〜330 実測分 57 連続は据え置き)。
- 回帰 assert せず。基準値据え置き: robotics 57/624/0 (kbb 第2経路・bench-328 実測) / giemon 46/115/0 (kbb 緑 2 連続)。clojure 主経路は基準値未確立 (silent-zero 既知)。

## HEAD 観測 (git 実測・決定的)
- robotics 実 checkout (`/Users/junkawasaki/github/kotoba-lang/robotics`): **a1af59c** (bench-328/331 実測値と一致・不変)。
- giemon 実 checkout (`/Users/junkawasaki/github/kotoba-lang/giemon`): **cd05afb** (bench-328/331 実測値と一致・不変)。
- 本 checkout 未コミット in-flight 継続: `M scripts/edn-datomize.bb` / `M sim-loop/status/_redcheck_tmp.txt` / `M sim-loop/status/maturity.md` / untracked `evidence/.hermes-tmp.Ytfzs4` `bench-328.md` `bench-331.md` (git status 実測)。src/test 変更なし。
- 修復系 blob 着地の有無は本走未検査 (静的検査すら load 帯で省略 — cron 予算と負荷を優先し honest unmeasured)。

## seeded 再現
- **not-applicable**: sim-loop は L0・L1 以降の学習ジョブ未実装 (jobs/ runs/ 不在継続) につき対象外。verdict: not-applicable (本走での追加実行なし)。

## 再現コマンド
```
cd /Users/junkawasaki/github/kotoba-lang/robotics && clojure -M:test
cd /Users/junkawasaki/github/kotoba-lang/giemon  && clojure -M:test
```
(本走は実行せず。次回 load 15-min < 2×ncpu=20 で実施。)

## 備考
- falsify: 新規なし (H1〜H88 全決着・falsify-087 欠番)。
- NEXT 据え置き: test-runner 修復 (cljk rename 後の clojure 主経路 silent-zero 解消 + falsify-079 の意図的 fail 挿入 RC=1 検収) を HEAD 参照 a1af59c / cd05afb で再発行 (継続)。
- コード変更なし。
