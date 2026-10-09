# falsify-089 (H89) — runner-repair (clojure -M:test silent-zero 解消) は現 HEAD cd05afb で着地済みか (純静的読取・load gate 超過につき runner 実行は load-skip)

## 仮説
H89: NEXT が最優先修理として再発行している test-runner 修復 (clojure -M:test の
silent-zero 解消) は **現 HEAD (giemon cd05afb) で着地済み** であり、
test 拡張子の戻しまたは loader 登録が blob として存在する、と主張される。

## 実測 (本走・純静的読取のみ。全 terminal 出力は file redirect 取得・決定的)
- HOST LOAD (pre-run snapshot, 1/5/15-min): 113.97 / 125.77 / **132.58** / ncpu 10
  → **≈11–13x ≥ 2x gate**。load gate 超過につき deep/heavy 経路 (clojure -M:test・
  kbb・seeded 再現) は本走 **load-skip → unmeasured (honest)**。runner を実行しなかった。
- HEAD (git rev-parse HEAD 実測): `cd05afbbd0a575b04e20dcda5e5a2e8dec01c934`
  tree `c3c454d2` — log 先頭は `cd05afb 2026-09-26 Merge repo-bot :landed —
  sim-loop evidence bench-327 + maturity.md`。
- in-flight (git status --porcelain --untracked-files=all 実測):
  `M scripts/edn-datomize.bb` / `M sim-loop/status/_redcheck_tmp.txt` /
  `M sim-loop/status/maturity.md` + untracked `bench-328/331/332/336/337.md` +
  `.hermes-tmp.Ytfzs4`。**runner 修復系 (test 拡張子・deps.edn・loader 登録) の
  変更 blob は 0 着地**。
- test 拡張子 census (git ls-files 実測): `test/` 配下 **10 ファイルすべて `.cljk`**、
  `src/` 配下 8 ファイル `.cljk` — `.clj` への戻しは 0 (clojure runner が
  require できる拡張子が test tree に存在しない)。
- deps.edn `:test` alias (L27-31 実測): cognitect test-runner v0.5.1 + `:extra-paths ["test"]` —
  **`.cljk` loader 登録の追加なし** (falsify-069 確定の根因「JVM Clojure は .cljk を
  ロード不能」がそのまま残存)。deps.edn 内の cljk 言及は L13 の floor コメントのみ。
- runner green の新規証拠: 0。kbb 第2経路の緑 (robotics 57/624/0 ×2・giemon 46/115/0 ×2,
  bench-328/333) は既知・clojure 主経路 silent-zero は bench-244〜333 実測分 57 連続で未解消。

## verdict: **refuted**
- 主張「runner-repair は現 HEAD cd05afb で着地済み」を **refuted**。
- 根拠 (測定のみ): (1) test tree が 100% `.cljk` のまま — clojure runner から require 可能な
  test 拡張子が 0。(2) deps.edn `:test` alias に loader 登録追加なし (L27-31 不変)。
  (3) in-flight に修復系 blob 0。修復 3 本柱 (拡張子戻し / loader 登録 / 検収に
  falsify-079 型 意図的 fail RC=1 挿入) のいずれも HEAD cd05afb に存在しない。
- 副次: load ≈11–13x で runner 実測は load-skip unmeasured — green 再確認は
  load < 2x の次回 + 修復 commit 着地が前提。基準値 (kbb robotics 57/624/0・
  giemon 46/115/0) は据え置き、本走は回帰 assert せず。
- 手続き上の副次 (falsify-086 と同一再現性): 本走も terminal 直接 stdout が 3 件空
  (exit 0) — file redirect で正常取得。空出力 = 無しの証拠にならない旨再確認。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
git rev-parse HEAD                  # -> cd05afbbd0a575b04e20dcda5e5a2e8dec01c934
git rev-parse --short=8 'HEAD^{tree}'  # -> c3c454d2
git status --porcelain --untracked-files=all  # 修復系 blob 0 (M maturity 等 3 + ?? evidence 6)
git ls-files test | sed 's/.*\.//' | sort | uniq -c   # -> 10 cljk (clj 0)
git ls-files 'src/*' | sed 's/.*\.//' | sort | uniq -c  # -> 8 cljk
grep -n -A8 ':test' deps.edn        # -> cognitect runner のみ・cljk loader 登録なし
uptime && sysctl -n hw.ncpu         # 15-min 132.58 / 10 ≈ 13x (gate 2x 超過 -> load-skip)
```
no code change (本 bot は修正しない)。

## コアへの 1 行メッセージ
runner-repair は現 HEAD cd05afb (test tree 100% .cljk・deps.edn `:test` loader 登録なし・
修復 blob 0) で未着地 = silent-zero 57 連続継続 (H89 refuted)。load ≈13x につき本走は
静的のみ・runner 実測 load-skip。修復 commit 着地 + load < 2x 窓で clojure -M:test
再測定 (検収に falsify-079 型 RC=1 挿入を含める) が次の最優先。
